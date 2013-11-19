define firewall::allow_https {
  ufw::allow { "https from ${title}":
    port => 443,
    from => $title,
    ip   => 'any',
  }
}
