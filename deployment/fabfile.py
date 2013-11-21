from os import environ

from fabric.api import (
    abort,
    cd,
    env,
    fastprint,
    hide,
    local,
    put,
    roles,
    run,
    settings,
    show,
    sudo,
    task,
)

dev_jump = "37.26.89.67"
dev1 = "37.26.89.67"

env.use_ssh_config = True

env.roledefs = {
    # Preview environment - For Alpha
    'ci': [dev1],
    'showcase': ["showcase-rps"]
}

def roles_for_host(host_query):
    return [role for role,hosts in env.roledefs.items() if host_query in hosts]

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
    sudo("apt-get -yq update")
    sudo("apt-get -yq install curl")
    run(cmd)

@task
def build_puppet():
    local("../puppet/tools/build")

@task
def bootstrap_jenkins(deploy_env):
    role = roles_for_host(env.host_string)[0]
    if role is not "ci":
        abort("Only CI boxes can be bootstrapped")
    else:
        put('../puppet/puppet.tgz', '/tmp/puppet.tgz')
        put('../../puppet-secrets/puppet-secrets.tgz', '/tmp/puppet-secrets.tgz')
        run('mkdir -p /tmp/puppet')
        with cd('/tmp/puppet'):
            run('tar xf /tmp/puppet.tgz')
            run('tar xf /tmp/puppet-secrets.tgz')
            run('sudo -i FACTER_role={role} '
                'sh -c "cd \'$PWD\'; ./bin/puppet apply '
                '--environment={deploy_env} '
                '--verbose '
                '--confdir=. '
                '--modulepath modules:vendor/modules '
                'manifests/site.pp"'.format(role=role, deploy_env=deploy_env))
    run('sudo rm -rf /tmp/puppet /tmp/puppet.tgz /tmp/puppet-secrets.tgz')

@task
def ensure_prepuppet_requirements():
    packages = ["ruby1.9.1", "ruby1.9.1-dev", "build-essential"]
    for package in packages:
        status = run("dpkg -s {package}".format(**locals()), warn_only=True)
        if status.return_code != 0:
            sudo("apt-get -yq install {package}".format(**locals()))

@task
def puppet(deploy_env="alpha"):
    ensure_prepuppet_requirements()
    role = roles_for_host(env.host_string)[0]
    if role is None:
        abort('No Puppet role defined, exiting.')
    fetch_artifact(deploy_env, 'puppet', 'puppet/puppet.tgz', '~/puppet.tgz')
    fetch_artifact(deploy_env, 'puppet-secrets', 'puppet-secrets.tgz', '~/puppet-secrets.tgz')
    run('mkdir puppet')
    with cd('puppet'):
        run('tar xf ~/puppet.tgz')
        run('tar xf ~/puppet-secrets.tgz')
        run('sudo -i FACTER_role={role} '
            'sh -c "cd \'$PWD\'; ./bin/puppet apply '
            '--environment={deploy_env} '
            '--verbose '
            '--confdir=. '
            '--modulepath modules:vendor/modules '
            'manifests/site.pp"'.format(role=role, deploy_env=deploy_env))
    run('sudo rm -rf puppet puppet.tgz puppet-secrets.tgz')
