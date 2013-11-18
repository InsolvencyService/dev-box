define firewall::allow_dns {
  ufw::allow { "dns from ${title}":
    proto => 'udp',
    port  => 53,
    from  => $title,
    ip    => 'any',
  }
}
