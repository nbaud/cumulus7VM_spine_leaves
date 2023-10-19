Vagrant.configure("2") do |config|

  # Base box
  config.vm.box = "CumulusCommunity/cumulus-vx"
  config.vm.box_check_update = false
  config.vbguest.auto_update = false

  # Nodes configuration
  nodes = {
    "leaf01" => {
      "intnets" => ["intnet-1", "intnet-3", "intnet-4"]
    },
    "leaf02" => {
      "intnets" => ["intnet-2", "intnet-3", "intnet-4"]
    },
    "spine01" => {
      "intnets" => ["intnet-1", "intnet-2"]
    }
  }

  # Iterate through each node
  nodes.each do |node_name, node_data|
    config.vm.define node_name do |node|
      node.vm.hostname = node_name

      # Configure internal networks for swp* interfaces
      node_data["intnets"].each do |intnet|
        node.vm.network "private_network", virtualbox__intnet: intnet, auto_config: false
      end

      # VirtualBox configuration
      node.vm.provider "virtualbox" do |vb|
        vb.memory = "2048"
        vb.cpus = 2

        # Dynamic NIC customization based on intnets
        node_data["intnets"].each_with_index do |intnet, idx|
          vb.customize ['modifyvm', :id, "--nicpromisc#{idx+2}", 'allow-vms']
        end
      end

      # Basic setup provisioning
      node.vm.provision "shell", inline: <<-SHELL
        echo "#{node_name} #{node_name}" >> /etc/hosts
        mkdir -p /home/vagrant/.ssh
        chown -R vagrant:vagrant /home/vagrant/.ssh
        chmod 700 /home/vagrant/.ssh
        # Update apt repositories
        apt-get update
        # Setting up the locales otherwise ansible doesn't work fine from the get-go 
        sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen
        locale-gen en_US.UTF-8
        update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
      SHELL

      # Install VirtualBox Guest Additions provisioning
      node.vm.provision "shell", inline: <<-SHELL
        apt update
        apt install -y linux-headers-$(uname -r) build-essential
        apt install -y kernel-mft-dkms-5.10.0-cl-1-amd64
        VBOX_ISO="/vagrant/VBoxGuestAdditions_7.0.10.iso"
        mkdir -p /mnt/cdrom
        mount -o loop $VBOX_ISO /mnt/cdrom
        sh /mnt/cdrom/VBoxLinuxAdditions.run || {
          echo "Failed to install Guest Additions. Attempting quicksetup..."
          /sbin/rcvboxadd quicksetup all
        }
        umount /mnt/cdrom
      SHELL
    end
  end
end

