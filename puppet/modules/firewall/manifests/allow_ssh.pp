define firewall::allow_ssh {
  ufw::allow { "ssh from ${title}":
    port => 22,
    from => $title,
    ip   => 'any',
  }
}
