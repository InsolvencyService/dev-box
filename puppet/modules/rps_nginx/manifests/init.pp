class rps_nginx {
  package { 'nginx':
    ensure => true
  }

  File {
    owner => 'root',
    group => 'root',
    mode  => '0644',
  }

  file {'/etc/nginx/htpasswd':
    content => hiera('htpasswd_file', ''),
    owner   => 'www-data',
    mode    => '0600',
    require => Package['nginx']
  }

  file { '/etc/nginx':
    ensure => directory,
  }

  file { '/etc/nginx/conf.d':
    ensure => directory,
    require => File['/etc/nginx']
  }

  file {'/etc/nginx/nginx.conf':
    ensure  => file,
    content => template('rps_nginx/nginx.conf'),
    require => [Package['nginx'], File['/etc/nginx']]
  }
  file {'/etc/nginx/conf.d/proxy.conf':
    ensure  => file,
    content => template('rps_nginx/proxy.conf'),
    require => [Package['nginx'], File['/etc/nginx/conf.d']]
  }
}
