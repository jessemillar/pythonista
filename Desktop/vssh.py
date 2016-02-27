"""Find the IP address of a VirtualBox virtual machine and ssh into it.\
   Add or update /etc/hosts entries upon user interaction."""

import os
import subprocess
import sys


def check_exists(name):
    """Check if the virtual machine exists."""
    virtualbox_exists = subprocess.Popen(["VBoxManage", "list", "vms"], stdout=subprocess.PIPE)

    if name in virtualbox_exists.communicate()[0]:
        return True
    else:
        return False


def check_up(name):
    """Check if the virtual machine is currently powered on."""
    virtualbox_up = subprocess.Popen(["VBoxManage", "list", "runningvms"], stdout=subprocess.PIPE)

    if name in virtualbox_up.communicate()[0]:
        return True
    else:
        return False


def find_host(name):
    """Check if an entry already exists in /etc/hosts."""
    hosts = open("/etc/hosts", "r")
    for line in hosts:
        if name in line:
            return True

    return False


def host_outdated(address, name):
    """Check if the entry for the virtual machine in /etc/hosts is outdated."""
    hosts = open("/etc/hosts", "r")
    for line in hosts:
        if name in line:
            if address not in line:
                return True

    return False


def add_host(address, name):
    """Add an entry in /etc/hosts for the virtual machine."""
    hosts = open("/etc/hosts", "rt")
    hosts_contents = hosts.read() + "\n" + address + "\t" + name + "\n"
    temp_hosts = open("/tmp/etc_hosts.tmp", "wt")
    temp_hosts.write(hosts_contents)

    # Move the temp hosts file into place with sudo permissions
    os.system("sudo mv /tmp/etc_hosts.tmp /etc/hosts")


def update_host(address, name):
    """Update an entry in /etc/hosts to have the correct IP address."""
    hosts = open("/etc/hosts", "r")
    data = hosts.readlines()
    new_hosts = []

    for line in data:
        if name in line:
            new_hosts.append(address + "\t" + name + "\n")
        else:
            new_hosts.append(line)

    print new_hosts

    temp_hosts = open("/tmp/etc_hosts.tmp", "wt")
    temp_hosts.writelines(new_hosts)

    # Move the temp hosts file into place with sudo permissions
    os.system("sudo mv /tmp/etc_hosts.tmp /etc/hosts")


def main():  # Define as a function to adhere to style guidelines
    """Where the magic happens."""
    try:
        sys.argv[1]
    except IndexError:
        print "Missing name of virtual machine"
        return

    # Check if the user is supplying the virtual machine's name correctly
    try:
        sys.argv[2]
    # If the name is correct, run the program
    except IndexError:
        if not check_exists(sys.argv[1]):
            print "The specified virtual machine does not appear to exist."
            return

        if not check_up(sys.argv[1]):
            headless_input = raw_input("The specified virtual machine does not appear to be running. Would you like to start the machine in 'headless' mode? [Y/n] ")

            if len(headless_input) == 0 or headless_input == "Y" or headless_input == "y":  # If the user responds in the affirmative
                subprocess.Popen(["VBoxManage", "startvm", sys.argv[1], "--type", "headless"], stdout=subprocess.PIPE)
                print "Please wait for the machine to boot before trying to connect again."
                return
            else:
                return

        virtualbox_ip = subprocess.Popen(["VBoxManage", "guestproperty", "get", sys.argv[1], "/VirtualBox/GuestInfo/Net/0/V4/IP"], stdout=subprocess.PIPE)
        ip_response = virtualbox_ip.communicate()[0]
        if ip_response == "No value set!\n":
            print "Could not find the virtual machine's IP address. Are network settings configured correctly?"
            return

        if find_host(sys.argv[1]):
            if host_outdated(ip_response.split()[1], sys.argv[1]):
                hosts_input = raw_input("/etc/hosts has an outdated entry for this virtual machine. Would you like to update it? [Y/n] ")

                if len(hosts_input) == 0 or hosts_input == "Y" or hosts_input == "y":  # If the user responds in the affirmative
                    update_host(ip_response.split()[1], sys.argv[1])
        else:
            hosts_input = raw_input("/etc/hosts does not have an entry for this virtual machine. Would you like to add one? [Y/n] ")

            if len(hosts_input) == 0 or hosts_input == "Y" or hosts_input == "y":  # If the user responds in the affirmative
                add_host(ip_response.split()[1], sys.argv[1])

        os.system("ssh " + ip_response.split()[1])
    else:
        print "If your virtual machine's name contains spaces, please wrap it in quotes."
        return

main()  # Run the function so the module is useful in a CLI
