define firewall::allow_http {
  ufw::allow { "http from ${title}":
    port => 80,
    from => $title,
    ip   => 'any',
  }
}
