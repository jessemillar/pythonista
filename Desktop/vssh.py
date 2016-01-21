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
        sys.argv[2]
    except IndexError:
        virtualbox_cmd = [
            'vboxmanage',
            'guestproperty',
            'get',
            sys.argv[1],
            '/VirtualBox/GuestInfo/Net/0/V4/IP'
        ]

        virtualbox_process = subprocess.Popen(virtualbox_cmd, stdout=subprocess.PIPE)
        address = virtualbox_process.communicate()[0].split()[1]

        os.system('ssh ' + address)
    else:
        print "If your virtual machine's name contains a space, please wrap it in quotes."
        return

main()  # Run the function so the module is useful in a CLI
