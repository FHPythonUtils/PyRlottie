# $Env:VAGRANT_VAGRANTFILE='Vagrantfile_linux.rb'; vagrant up
# VAGRANT_VAGRANTFILE=Vagrantfile_linux.rb vagrant up

$script = <<-SCRIPT
sudo apt update -y && sudo apt upgrade -y
sudo apt install cmake gcc g++ libgif-dev -y
echo "deb [arch=arm64] http://ports.ubuntu.com/ focal main restricted
deb [arch=arm64] http://ports.ubuntu.com/ focal-updates main restricted
deb [arch=arm64] http://ports.ubuntu.com/ focal universe
deb [arch=arm64] http://ports.ubuntu.com/ focal-updates universe
deb [arch=arm64] http://ports.ubuntu.com/ focal multiverse
deb [arch=arm64] http://ports.ubuntu.com/ focal-updates multiverse
deb [arch=arm64] http://ports.ubuntu.com/ focal-backports main restricted universe multiverse
" > /etc/apt/sources.list.d/arm-cross-compile-sources.list
sudo dpkg --add-architecture arm64
sudo apt install gcc-aarch64-linux-gnu binutils-aarch64-linux-gnu g++-aarch64-linux-gnu libgif-dev:arm64 -y
SCRIPT

Vagrant.configure("2") do |config|
  config.vm.box = "generic/ubuntu2004"
  config.ssh.guest_port = 22
  config.vm.define "vagrant_linux", primary:true do |vagrant_linux|
  end
  #set the synced_folder up
  config.vm.provider :virtualbox do |vb|
    vb.customize ["modifyvm", :id, "--natdnshostresolver1", "on"]
    config.vm.synced_folder ".", "/src", type: "virtualbox", automount: true
  end
  config.vm.network :forwarded_port, guest: 22, host: 2200, id: "ssh"
  config.vm.provision "shell", inline: $script
end
