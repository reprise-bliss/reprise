# -*- mode: ruby -*-
# vi: set ft=ruby :
Vagrant.configure("2") do |config|
  config.vm.box = "raring64"
  config.vm.box_url = "http://cloud-images.ubuntu.com/raring/current/raring-server-cloudimg-vagrant-amd64-disk1.box"
  config.vm.host_name = "magnetron"
  config.vm.define :magnetron do |config|
    config.vm.synced_folder ".", "/home/vagrant/magnetron"
    config.vm.provision :puppet do |puppet|
      puppet.manifests_path = "puppet/manifests"
      puppet.manifest_file  = "magnetron.pp"
    end
  end
end
