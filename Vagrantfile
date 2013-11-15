# -*- mode: ruby -*-
# vi: set ft=ruby :

VAGRANTFILE_API_VERSION = '2'

Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

    config.vm.box = 'precise64'
    config.vm.box_url = 'http://files.vagrantup.com/precise64.box'

    config.vm.define "development", primary: true do |development|
      development.vm.network "forwarded_port", guest: 8000, host: 8000
      development.vm.network "forwarded_port", guest: 8001, host: 8001
      development.vm.provision :shell,
                    path: "vagrant-bootstrap.sh",
                    args: "localdev localdev"
      development.ssh.forward_agent = true
      if Vagrant.has_plugin?('vagrant-cachier')
        config.cache.auto_detect = true
      end
    end

#    config.vm.define "jenkins" do |jenkins|
#      config.vm.network "private_network", ip: "10.0.0.10"
#      jenkins.vm.provision :shell,
#                    path: "vagrant-bootstrap.sh",
#                    args: "jenkins localdev"
#
#    end

end
