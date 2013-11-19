class firewall::base {

  $trusted_ips = hiera('trusted_ips', [])
  validate_array($trusted_ips)

  firewall::allow_http { $trusted_ips: }
  firewall::allow_https { $trusted_ips: }
  firewall::allow_ssh { $trusted_ips: }

}
