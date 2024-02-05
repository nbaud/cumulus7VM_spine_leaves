# cumulus7VM_spine_leaves
Deploy 7 VM (3 leaves and 2 spines using the latest Cumulus VX vagrant image and 2 regular Debians 11 connected to the leaves 1 and 3) for testing a spine and leaf architecture with VXLAN.

* Multiple ansible connections possible with prepared ssh access on different ports with sudo access.
* Shared directory available and configured for easy access.

Done using the latest version of vagrant (2.4.1) and the latest version of Virtual Box (7.0.14) with guest addition installed through Vagrant.

Requirements:

* Change the user you want to add in the Vagrantfile.
* Copy the ssh public key file for that user into the "shared" directory (create it) that must be located in the directory where the Vagrantfile is.
* Virtualbox version 7.0.14 installed
* Vagrant 2.4.1 installed

If the above is fine, you should be able to bring up and provision everything by just using "vagrant up" from the Vagrantfile directory.
