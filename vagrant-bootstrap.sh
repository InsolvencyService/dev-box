#!/bin/bash

set -eu

status () {
  echo "---> ${@}" >&2
}

usage () {
  echo "Usage: $(basename "$0") <role> [env] [rootdir]" >&2
  echo
  echo "    role      required - one of [localdev,app,db,ci]"
  echo "    env       optional - default: vagrant"
  echo "    rootdir   optional - default: /vagrant"
  echo
}

# Sudo doesn't run if we can't write to the terminal
preflight_sudo () {
  local cmd='[[ $(test -t 0) ]] && mesg n'
  local file='/root/.profile'
  if ! fgrep -q "$cmd" "$file"; then
    status "fixing up sudo"
    echo '[[ $(test -t 0) ]] && mesg n' >> /root/.profile
  fi
}

# We're based in the UK, so use UK mirrors
preflight_apt () {
  if ! fgrep -q 'http://gb' /etc/apt/sources.list; then
    status "configuring apt"
    sed -i 's|http://us|http://gb|' /etc/apt/sources.list
  fi
}

# Before we can run puppet we need some basic packages
PACKAGES="git-core ruby1.9.1 ruby1.9.1-dev build-essential"
preflight_packages () {
  if ! dpkg -s $PACKAGES >/dev/null 2>&1; then
    status "apt-get update"
    apt-get update -y -qq
    status "installing apt packages"
    apt-get install -y -qq $PACKAGES 2>&1
  fi

  echo 'gem: --quiet --no-rdoc --no-ri' > /root/.gemrc
  if ! gem list -i "bundler" >/dev/null; then
    status "installing bundler"
    gem install bundler 2>&1
  fi
}

cleanup () {
  local tmpdir=$1
  status "cleaning up"
  rm -rf "$tmpdir"
}

run_puppet () {
  local role=$1
  local env=$2
  local rootdir=$3

  # First we build the puppet tarball
  # This tarball is a totally self contained puppet
  # And it's run from within $rootdir or /vagrant/puppet by default
  status "running build in ${rootdir}"
  cd $rootdir
  ./tools/build -n

  # Now we extract it locally to the virtual machine
  status "extracting tarball"
  PUPPET_TMP=$(mktemp -d)
  trap "cleanup '$PUPPET_TMP'" EXIT
  cd "$PUPPET_TMP"
  tar xf $rootdir/puppet.tar

  # Finally we run puppet from the tarball.
  status "running puppet in ${env} environment"
  FACTER_role="$role" ./bin/puppet apply \
    --environment=${env} \
    --confdir=. \
    --modulepath=modules:vendor/modules \
    manifests/site.pp
}

main () {
  if [ "$#" -eq 0 ]; then
    usage
    exit 1
  fi

  local role=${1}
  local env=${2-"vagrant"}
  local rootdir=${3-"/vagrant/puppet"}
  status "Starting provisioning process"
  preflight_sudo
  preflight_apt
  preflight_packages
  run_puppet "$role" "$env" "$rootdir"
}

main "$@"
