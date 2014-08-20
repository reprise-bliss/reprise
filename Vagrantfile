# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "trusty64"
  config.vm.box_url = "http://jenkins.devbliss.com/vagrant/trusty64.box"
  config.vm.host_name = "reprise"
  config.vm.define :reprise do |config|
    config.vm.synced_folder ".", "/home/vagrant/reprise"
    config.vm.provision :puppet do |puppet|
      puppet.manifests_path = "puppet/manifests"
      puppet.manifest_file  = "reprise.pp"
    end
  end
end
