class firewall(
  $allow = {},
  $deny = {},
  $limit = {}
) {

  include ufw

  file { '/etc/default/ufw':
    source => 'puppet:///modules/firewall/defaults',
    notify => Exec['reload ufw'],
  }

  exec { 'reload ufw':
    command     => '/usr/sbin/ufw reload',
    refreshonly => true,
  }

  # Collect all virtual ufw rules
  Ufw::Allow <| |>
  Ufw::Deny <| |>
  Ufw::Limit <| |>

  include firewall::base

  # Instantiate additional firewall rules
  validate_hash($allow)
  create_resources('ufw::allow', $allow)
  validate_hash($deny)
  create_resources('ufw::deny', $deny)
  validate_hash($limit)
  create_resources('ufw::limit', $limit)

}
