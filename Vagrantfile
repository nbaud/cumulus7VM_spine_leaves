Vagrant.configure("2") do |config|

  # Base box
  config.vm.box_check_update = false
  config.vbguest.auto_update = false

  # Nodes configuration
  nodes = {
    "leaf01" => {
      "intnets" => ["intnet-1", "intnet-2", "intnet-1-extra"],
      "box" => "CumulusCommunity/cumulus-vx"
    },
    "leaf02" => {
      "intnets" => ["intnet-3", "intnet-4"],
      "box" => "CumulusCommunity/cumulus-vx"
    },
    "leaf03" => {
      "intnets" => ["intnet-5", "intnet-6", "intnet-3-extra"],
      "box" => "CumulusCommunity/cumulus-vx"
    },
    "spine01" => {
      "intnets" => ["intnet-1", "intnet-3", "intnet-5"],
      "box" => "CumulusCommunity/cumulus-vx"
    },
    "spine02" => {
      "intnets" => ["intnet-2", "intnet-4", "intnet-6"],
      "box" => "CumulusCommunity/cumulus-vx"
    },
    "vm01" => {
      "intnets" => ["intnet-1-extra"],
      "box" => "debian/bullseye64"
    },
    "vm03" => {
      "intnets" => ["intnet-3-extra"],
      "box" => "debian/bullseye64"
    }
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

      # VirtualBox configuration
      node.vm.provider "virtualbox" do |vb|
        vb.name = node_name

        if ["vm01", "vm03"].include?(node_name)
          vb.memory = "512"  # default RAM
          vb.cpus = 1
        else
          vb.memory = "2048"
          vb.cpus = 2
        end

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
        apt update
        # Setting up the locales otherwise ansible doesn't work fine from the get-go 
        sed -i '/en_US.UTF-8/s/^# //g' /etc/locale.gen
        locale-gen en_US.UTF-8
        update-locale LANG=en_US.UTF-8 LC_ALL=en_US.UTF-8
      SHELL

      # Install VirtualBox Guest Additions provisioning for Cumulus VX
      if ["leaf01", "leaf02", "leaf03", "spine01", "spine02"].include?(node_name)
        node.vm.provision "shell", inline: <<-SHELL
          apt install apt-utils -y
          apt install -y linux-headers-$(uname -r) build-essential
          apt install -y kernel-mft-dkms-5.10.0-cl-1-amd64
          /sbin/rcvboxadd setup
          rcvboxadd reload
          systemctl restart vboxadd.service
          systemctl status vboxadd.service || {
            echo "vboxadd.service status check failed. Please check the service manually."
          }
        SHELL
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
      end

      # Install VirtualBox Guest Additions for Debian
      if ["vm01", "vm03"].include?(node_name)
        node.vm.provision "shell", inline: <<-SHELL
          apt update
          apt install apt-utils -y
          apt install -y linux-headers-$(uname -r) build-essential dkms
          VBOX_ISO="/vagrant/VBoxGuestAdditions_7.0.14.iso"
          mkdir -p /mnt/cdrom
          chmod 700 /mnt/cdrom
          mount -o loop $VBOX_ISO /mnt/cdrom
          sh /mnt/cdrom/VBoxLinuxAdditions.run || echo "Failed to install Guest Additions. If everything else seems fine, you may ignore this."
          umount /mnt/cdrom
        SHELL
      end

      # Disable the default shared folder 
      node.vm.synced_folder ".", "/vagrant", disabled: true

      # Setup shared folder with explicit automount
      node.vm.synced_folder "#{Dir.pwd}/shared", "/vagrant",
        owner: "vagrant", group: "vagrant",
        mount_options: ["dmode=775,fmode=664"],
        automount: true,
        create: true

    end
  end
end

