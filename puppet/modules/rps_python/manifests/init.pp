class rps_python {
  class {'python':
    version    => 'system',
    dev        => true,
    gunicorn   => true,
    pip        => true,
    virtualenv => true,
  }

  package {'virtualenvwrapper':
    ensure  => 'present',
    require => Class['python']
  }

}
