class rps_nginx {
  class { 'nginx':}

  file {'/etc/nginx/htpasswd':
    content => hiera('htpasswd_file', ''),
    owner   => 'www-data',
    mode    => '0600',
    require => Class['nginx']
  }
}
