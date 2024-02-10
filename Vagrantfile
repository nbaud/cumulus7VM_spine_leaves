#### Current version optimised for virtualbox 7.0.14 with guest addition

Vagrant.configure("2") do |config|


## Base box
  config.vm.box_check_update = false
  config.vbguest.auto_update = false

  # Nodes configuration
  nodes = {
    "leaf01" => { "intnets" => ["intnet-1", "intnet-2", "intnet-1-extra", "intnet-2-extra"], "box" => "CumulusCommunity/cumulus-vx", "ssh_id" => "11" },
    "leaf02" => { "intnets" => ["intnet-3", "intnet-4", "intnet-3-extra", "intnet-4-extra"], "box" => "CumulusCommunity/cumulus-vx", "ssh_id" => "12" },
    "leaf03" => { "intnets" => ["intnet-5", "intnet-6", "intnet-5-extra", "intnet-6-extra"], "box" => "CumulusCommunity/cumulus-vx", "ssh_id" => "13" },
    "spine01" => { "intnets" => ["intnet-1", "intnet-3", "intnet-5"], "box" => "CumulusCommunity/cumulus-vx", "ssh_id" => "21" },
    "spine02" => { "intnets" => ["intnet-2", "intnet-4", "intnet-6"], "box" => "CumulusCommunity/cumulus-vx", "ssh_id" => "22" },
    "vm01" => { "intnets" => ["intnet-1-extra", "intnet-2-extra"], "box" => "debian/bookworm64", "ssh_id" => "31" },
    "vm02" => { "intnets" => ["intnet-3-extra", "intnet-4-extra"], "box" => "debian/bookworm64", "ssh_id" => "32" },
    "vm03" => { "intnets" => ["intnet-5-extra", "intnet-6-extra"], "box" => "debian/bookworm64", "ssh_id" => "33" }
  }

  # Iterate through each node
  nodes.each do |node_name, node_data|
    config.vm.define node_name do |node|
      node.vm.box = node_data["box"]
      node.vm.hostname = node_name

      # Configure internal networks for swp* interfaces
      node_data["intnets"].each do |intnet|
        node.vm.network "private_network", virtualbox__intnet: intnet, auto_config: false
      end

      # SSH Configuration
      host_port = 2200 + node_data["ssh_id"].to_i
      node.vm.network "forwarded_port", guest: 22, host: host_port, id: "ssh", auto_correct: true

##### VirtualBox configuration
      node.vm.provider "virtualbox" do |vb|
        vb.name = node_name

        if ["vm01", "vm02", "vm03"].include?(node_name)
          vb.memory = "512"  # default RAM for basic VM
          vb.cpus = 1
        else
          vb.memory = "2048" # more for the cumulus
          vb.cpus = 2
        end
#####

##### Dynamic NIC customization based on intnets
        node_data["intnets"].each_with_index do |intnet, idx|
          vb.customize ['modifyvm', :id, "--nicpromisc#{idx+2}", 'allow-vms']
        end
      end
#####

##### Basic setup provisioning
      node.vm.provision "shell", inline: <<-SHELL
        echo "#{node_name} #{node_name}" >> /etc/hosts
        mkdir -p /home/vagrant/.ssh
        chown -R vagrant:vagrant /home/vagrant/.ssh
        chmod 700 /home/vagrant/.ssh
        # Update apt repositories
        apt update
        apt install apt-utils -y
        apt upgrade -y
        # Setting up the locales otherwise ansible doesn't work fine from the get-go 
        sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen
        locale-gen en_US.UTF-8
        update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
      SHELL
#####

####### IF YOU DON'T RUN (PLEASE JUST DO IT)
####### vagrant plugin install vagrant-vbguest
####### IN YOUR VAGRANTFILE DIRECTORY YOU WILL HAVE TO UNCOMMENT THE STUFF BELOW AND IT ADDS SOME EXTRA TIME FOR LAUNCHING VMS
# ##### Install VirtualBox Guest Additions provisioning and shared directory only for the cumulus
#       node.vm.provision "shell", inline: <<-SHELL
#         apt install apt-utils -y
#         apt install -y linux-headers-$(uname -r) build-essential
#         apt install -y kernel-mft-dkms-5.10.0-cl-1-amd64
#         /sbin/rcvboxadd setup
#         rcvboxadd reload
#         systemctl restart vboxadd.service
#         systemctl status vboxadd.service || {
#           echo "vboxadd.service status check failed. Please check the service manually."
#         }
#       SHELL
#######

      # Disable the default /vagrant shared folder
      node.vm.synced_folder ".", "/vagrant", disabled: true

      # Setup a custom shared folder; adjust the host path as needed
      node.vm.synced_folder "./shared", "/vagrant",
                            owner: "vagrant", group: "vagrant",
                            mount_options: ["dmode=775,fmode=664"]

      # Provisioning script to ensure the folder is correctly mounted
      # This will run every time the VM is started
      node.vm.provision "shell", inline: <<-SHELL
        if mountpoint -q /vagrant; then
          echo "/vagrant/ is already mounted."
        else
          echo "Mounting /vagrant/..."
          sudo mount -t vboxsf -o uid=$(id -u vagrant),gid=$(getent group vagrant | cut -d: -f3),dmode=775,fmode=664 vagrant /vagrant
        fi
      SHELL

      # Disable the default shared folder 
      node.vm.synced_folder ".", "/vagrant", disabled: true

      # Setup shared folder with explicit automount
      node.vm.synced_folder "#{Dir.pwd}/shared", "/vagrant",
        owner: "vagrant", group: "vagrant",
        mount_options: ["dmode=775,fmode=664"],
        automount: true,
        create: true
#######

####### This block creates a new user and copies the public key located in the shared directory  
      node.vm.provision "shell", inline: <<-SHELL
        # Variables
        NEW_USER="nico" # Change this to the desired new username
        SSH_KEY_PATH="/vagrant/id_ed25519.pub" # Adjust if your key's name/path is different
        # Check if the user exists; if not, create the user and setup SSH
        if ! id "$NEW_USER" &>/dev/null; then
          echo "Creating user $NEW_USER..."
          sudo useradd -m -s /bin/bash "$NEW_USER"
          sudo mkdir -p /home/"$NEW_USER"/.ssh
          sudo touch /home/"$NEW_USER"/.ssh/authorized_keys
          # Add the SSH key to authorized_keys
          echo "Adding SSH key to $NEW_USER's authorized_keys..."
          sudo sh -c "cat $SSH_KEY_PATH >> /home/$NEW_USER/.ssh/authorized_keys"
          sudo chown -R $NEW_USER:$NEW_USER /home/$NEW_USER/.ssh
          sudo chmod 700 /home/$NEW_USER/.ssh
          sudo chmod 600 /home/$NEW_USER/.ssh/authorized_keys
          # Add user to sudoers with no password requirement
          echo "$NEW_USER ALL=(ALL) NOPASSWD:ALL" | sudo tee /etc/sudoers.d/49-$NEW_USER > /dev/null
          sudo chmod 0440 /etc/sudoers.d/49-$NEW_USER
        fi
      SHELL
#######

    end
  end
end

