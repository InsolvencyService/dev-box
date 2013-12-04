from contextlib import contextmanager
from os import environ

from fabric.api import (
    abort,
    cd,
    env,
    fastprint,
    hide,
    local,
    prefix,
    put,
    roles,
    run,
    settings,
    show,
    sudo,
    task,
)

env.use_ssh_config = True

JENKINS_HOSTS = {
    'alpha': '192.168.2.2'
}


def fetch_artifact(puppet_env, job, artifact, dest, build_number='lastSuccessfulBuild'):
    root = JENKINS_HOSTS.get(puppet_env)
    user = environ["RPS_JENKINS_USER"]
    token = environ["RPS_JENKINS_TOKEN"]
    url = 'https://{root}/job/{job}/{build_number}/artifact/{artifact}'.format(
        **locals())
    cmd = "curl -k -u '{user}:{token}' '{url}' > {dest}".format(**locals())
    run(cmd)


@task
def build_puppet():
    local("../puppet/tools/build")


def ensure_bootstrapping_requirements():
    packages = ["ruby1.9.1", "ruby1.9.1-dev", "curl"]
    missing_packages = []
    for package in packages:
        status = run("dpkg -s {package}".format(**locals()), warn_only=True)
        if status.return_code != 0:
            missing_packages.append(package)
    if len(missing_packages) != 0:
        sudo("apt-get -yq update")
        for package in missing_packages:
            sudo("apt-get -yq install {package}".format(**locals()))


@task
def deploy_puppet(role, deploy_env="alpha"):
    ensure_bootstrapping_requirements()
    fetch_artifact(deploy_env, 'puppet', 'puppet/puppet.tar', '~/puppet.tar')
    fetch_artifact(deploy_env, 'puppet-secrets', 'puppet-secrets.tgz', '~/puppet-secrets.tgz')
    run_puppet(role, deploy_env)


@task
def deploy_local_puppet(role, deploy_env="alpha"):
    ensure_bootstrapping_requirements()
    put("../puppet/puppet.tar")
    put("../../puppet-secrets/puppet-secrets.tgz")
    run_puppet(role, deploy_env)


def run_puppet(role, deploy_env):
    run('mkdir puppet')
    try:
        with cd('puppet'):
            run('tar xf ~/puppet.tar')
            run('tar xf ~/puppet-secrets.tgz')
            run('sudo -i FACTER_role={role} '
                'sh -c "cd \'$PWD\'; ./bin/puppet apply '
                '--environment={deploy_env} '
                '--verbose '
                '--confdir=. '
                '--modulepath modules:vendor/modules '
                'manifests/site.pp"'.format(**locals()))
    finally:
        run('sudo rm -rf puppet puppet.tar puppet-secrets.tgz')


@contextmanager
def virtualenv(virtualenv_name):
    def ensure_virtualenv_exists(venv_name):
        virtualenvs = run("lsvirtualenv").split("\n")
        if venv_name not in virtualenvs:
            run("mkvirtualenv {venv_name}".format(**locals()))
            with prefix("workon {venv_name}".format(**locals())):
                run("pip install --upgrade pip==1.4.1")
                run("pip install --upgrade setuptools==1.3.2")

    with prefix("source /etc/bash_completion.d/virtualenvwrapper"):
        ensure_virtualenv_exists(virtualenv_name)
        with prefix("workon {virtualenv_name}".format(**locals())):
            yield


@task
def deploy_app_from_git(tag=None):
    git_url = "git+https://git@github.com/InsolvencyService/rps-alpha.git"
    if tag is not None:
        git_url += "@{tag}".format(**locals())
    git_url += "#egg=redundancy_payments_alpha"
    with virtualenv("rps"):
        run("pip install -e {git_url}".format(**locals()))
        run("ensure_clean_tables")
        run("load_user_testing_data")
    ensure_upstart()
    ensure_nginx()


def ensure_upstart():
    def stop_start_to_workaround_upstart_config_loading():
        sudo("stop redundancy-payments-service", warn_only=True)
        sudo("start redundancy-payments-service")
        sudo("stop insolvency-practitioner-app", warn_only=True)
        sudo("start insolvency-practitioner-app")
    put("redundancy-payments-service.upstart", "/etc/init/redundancy-payments-service.conf", use_sudo=True, mode=0644)
    sudo("chown root:root /etc/init/redundancy-payments-service.conf")
    put("insolvency-practitioner-app.upstart", "/etc/init/insolvency-practitioner-app.conf", use_sudo=True, mode=0644)
    sudo("chown root:root /etc/init/insolvency-practitioner-app.conf")
    stop_start_to_workaround_upstart_config_loading()


def ensure_nginx():
    sudo("rm /etc/nginx/conf.d/*")
    put("redundancy-payments-service.nginx", "/etc/nginx/conf.d/redundancy-payments-service.conf", use_sudo=True)
    sudo("/etc/init.d/nginx restart")
