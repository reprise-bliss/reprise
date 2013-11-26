Exec {
  path => "/bin:/usr/bin:/sbin:/usr/sbin",
  user => "root",
}

Package {
  ensure => "latest",
  require => Exec["update"],
}

exec { "update":
  command => "apt-get update && touch /root/.updated",
  creates => "/root/.updated",
}

file { "/home/vagrant/.bash_login":
  content => "cd /home/vagrant/magnetron",
}
