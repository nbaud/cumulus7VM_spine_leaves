# cumulus7VM_spine_leaves
Deploy 8 VM (3 leaves and 2 spines using the latest Cumulus VX vagrant image and 3 regular Debians 11 connected to the leaves 1 and 3) for testing a spine and leaf architecture with OSPF/PIM, BGP, EVPN and VXLAN, incrementally.

Provisioned with Vagrant:
* 3x leaves with cumulus VX
* 2x spines with cumulus VX
* 2x connected servers/clients VM with Debian
* All ssh ansible connections with prepared ssh access and inventory file ready for use.
* Shared directory available and configured for easy access to files and data.

Done using the latest version of vagrant (2.4.1) and the latest version of Virtual Box (7.0.14) with guest addition installed through Vagrant.

Requirements:

* Have a decent computer/laptop to be able to run 8 VM in total.
* Change the user you want to add in the Vagrantfile.
* Copy the relevant ssh public key file for that user into the "shared" directory (create it) that must be located in the directory where the Vagrantfile is.
* Virtualbox version 7.0.14 installed
* Vagrant 2.4.1 installed (please also run `vagrant plugin install vagrant-vbguest` for better compatibility with functions like file-sharing with Virtualbox)
* Python installed (if you want to use Ansible)
* Ansible installed (if you want to use Ansible)

If the above is fine, you should be able to bring up and provision everything by just using "vagrant up" from the Vagrantfile directory.

ssh with the current setup for checking on the machines manually (or through the ansible inventory file as well):

for instance for leaf01, use: ssh -p 2211 localhost
or for vm03: ssh -p 2233 localhost

Copy from the inventory file:

```yml
---
[leaves]
leaf01 ansible_host=127.0.0.1 ansible_port=2211
leaf02 ansible_host=127.0.0.1 ansible_port=2212
leaf03 ansible_host=127.0.0.1 ansible_port=2213

[spines]
spine01 ansible_host=127.0.0.1 ansible_port=2221
spine02 ansible_host=127.0.0.1 ansible_port=2222

[vms]
vm01 ansible_host=127.0.0.1 ansible_port=2231
vm02 ansible_host=127.0.0.1 ansible_port=2232
vm03 ansible_host=127.0.0.1 ansible_port=2233
```
