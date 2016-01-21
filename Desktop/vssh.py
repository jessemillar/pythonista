"""Find the IP address of a VirtualBox virtual machine and ssh into it."""

import os
import subprocess
import sys


def main():  # Define as a function to adhere to style guidelines
    """Where the magic happens."""

    try:
        sys.argv[1]
    except IndexError:
        print "Missing name of virtual machine"
        return

    try:
        sys.argv[2]  # Check if the user is supplying the virtual machine's name correctly
    except IndexError:  # If the name is correct, run the program
        virtualbox_exists = subprocess.Popen(["VBoxManage", "list", "vms"], stdout=subprocess.PIPE)
        grep_exists = subprocess.Popen(["grep", "-c", sys.argv[1]], stdin=virtualbox_exists.stdout, stdout=subprocess.PIPE)  # Returns a string ("0", "1") stating whether the virtual machine is running; I cast the string to an int later on

        if int(grep_exists.communicate()[0]) == 0:
            print "The specified virtual machine does not appear to exist."
            return

        virtualbox_up = subprocess.Popen(["VBoxManage", "list", "runningvms"], stdout=subprocess.PIPE)
        grep_up = subprocess.Popen(["grep", "-c", sys.argv[1]], stdin=virtualbox_up.stdout, stdout=subprocess.PIPE)  # Returns a string ("0", "1") stating whether the virtual machine is running; I cast the string to an int later on

        if int(grep_up.communicate()[0]) == 0:
            print "The specified virtual machine does not appear to be running (or is currently booting)."
            headless_input = raw_input("Do you want to start the machine in 'headless' mode? [Y/n] ")

            if len(headless_input) == 0 or headless_input == "Y" or headless_input == "y":  # If the user responds in the affirmative
                subprocess.Popen(["VBoxManage", "startvm", sys.argv[1], "--type", "headless"], stdout=subprocess.PIPE)
                print "Please wait for the machine to boot before trying to connect again."
                return
            else:
                return

        virtualbox_ip_cmd = [
            "vboxmanage", "guestproperty", "get", sys.argv[1], "/VirtualBox/GuestInfo/Net/0/V4/IP"
        ]

        virtualbox_ip = subprocess.Popen(virtualbox_ip_cmd, stdout=subprocess.PIPE)
        address = virtualbox_ip.communicate()[0].split()[1]

        os.system("ssh " + address)
    else:
        print "If your virtual machine's name contains spaces, please wrap it in quotes."
        return

main()  # Run the function so the module is useful in a CLI
