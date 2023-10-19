Vagrant.configure("2") do |config|

  # Base box
  config.vm.box = "CumulusCommunity/cumulus-vx"
  config.vm.box_check_update = false
  config.vbguest.auto_update = false

  config.vm.define "leaf01" do |leaf01|
    # Internal network for swp* interfaces.
    leaf01.vm.network "private_network", virtualbox__intnet: "intnet-1", auto_config: false
    leaf01.vm.network "private_network", virtualbox__intnet: "intnet-3", auto_config: false
    leaf01.vm.network "private_network", virtualbox__intnet: "intnet-4", auto_config: false
    leaf01.vm.provider "virtualbox" do |vb|
        vb.memory = "2048"
        vb.cpus = 2
        vb.customize ['modifyvm', :id, '--nicpromisc2', 'allow-vms']
        vb.customize ['modifyvm', :id, '--nicpromisc3', 'allow-vms']
        vb.customize ['modifyvm', :id, '--nicpromisc4', 'allow-vms']
    end
  end

  config.vm.define "leaf02" do |leaf02|
    # Internal network for swp* interfaces.
    leaf02.vm.network "private_network", virtualbox__intnet: "intnet-2", auto_config: false
    leaf02.vm.network "private_network", virtualbox__intnet: "intnet-3", auto_config: false
    leaf02.vm.network "private_network", virtualbox__intnet: "intnet-4", auto_config: false
    leaf02.vm.provider "virtualbox" do |vb|
        vb.memory = "2048"
        vb.cpus = 2
        vb.customize ['modifyvm', :id, '--nicpromisc2', 'allow-vms']
        vb.customize ['modifyvm', :id, '--nicpromisc3', 'allow-vms']
        vb.customize ['modifyvm', :id, '--nicpromisc4', 'allow-vms']
    end
  end

  config.vm.define "spine01" do |spine01|
    # Internal network for swp* interfaces.
    spine01.vm.network "private_network", virtualbox__intnet: "intnet-1", auto_config: false
    spine01.vm.network "private_network", virtualbox__intnet: "intnet-2", auto_config: false
    spine01.vm.provider "virtualbox" do |vb|
        vb.memory = "2048"
        vb.cpus = 2
        vb.customize ['modifyvm', :id, '--nicpromisc2', 'allow-vms']
        vb.customize ['modifyvm', :id, '--nicpromisc3', 'allow-vms']
    end
  end

end

