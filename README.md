rps-alpha ![build status](https://travis-ci.org/InsolvencyService/rps-alpha.png?branch=master)
=========

Follow these steps to setup a Quickstart development environment for working with the RPS Alpha project.

## Quickstart Steps

### Windows Pre-reqs

- Install PyCharm Community Edition for Windows (http://www.jetbrains.com/pycharm/)
- Install Python 2.7.5 for Windows - Windows X86-64 MSI Installer (2.7.5) (http://www.python.org/download/releases/2.7.5/)
- Install Oracle Virtual Box for Windows (https://www.virtualbox.org/wiki/Downloads)
- Install git (http://git-scm.com/downloads)
  - if you are on Windows also install git-bash when asked.
  - when prompted to choose conversion setting pick check out as-is, commit unix style (the middle option)
- Install Vagrant (http://www.vagrantup.com/)

### Mac Pre-reqs

As above, use Mac version.

### Ubuntu pre-reqs

```
sudo aptitude install git
# Download vagrant deb package from http://downloads.vagrantup.com/
sudo dpkg -i vagrant.deb
```

### Post Install Tasks

- Configure SSH for GIT - Follow this guide (https://help.github.com/articles/generating-ssh-keys)
  - OK not to bother with a passphrase for alpha (leave blank), will need one for beta
- Clone the repository.
  - cd to your work in progress folder in git-bash
  - From git-bash: `git clone git@github.com:InsolvencyService/rps-alpha.git`

### Build box, run tests

- Open a new git-bash (windows)/terminal (mac) on and navigate to where you have downloaded or cloned this repo.
- Run `vagrant up`... Vagrant should create a new virtual machine and puppet should install all the needed deps.
- Run `vagrant ssh` to ssh into the newly created virtual machine
- Run `cd /vagrant` to see the files mirrored from your host machine to your VM
- To get the project to run, you'll need to do the following
  - `./create_venv.sh`
  - `workon rps`
  - `cd redundancy_payments_alpha/`
- You should now be able to run `./run_tests.sh` to run the tests or
  `./redundancy_payments_service` to run the server
- Once the server is running, you can access the webpage on http://localhost:8000/

### More info

- From within your vagrant box, cd to `/vagrant/manual`
- `pip install sphinx`
- Run `make html`
- Open docs in your browser from: `rps-alpha/manual/_build/html/index.html`
