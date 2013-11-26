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
  content => "export LC_ALL=C
alias magnetron='PYTHONPATH=/home/vagrant/magnetron/ python3 -m magnetron'
cd /home/vagrant/magnetron
",
}

# basic dependencies

package { "python3": }
package { "python3-setuptools": }
package { "dpkg-dev": }
package { "debhelper": }
package { "lintian": }
package { "reprepro": }
package { "pep8": }


# install docopt

exec { "apt-add-repository ppa:stefano-palazzo/docopt":
  creates => "/etc/apt/sources.list.d/stefano-palazzo-docopt-raring.list",
  notify => Exec["update docopt"],
}
exec { "update docopt":
  command => "apt-get update",
  onlyif => "test -z \"$(apt-cache search python3-docopt)\"",
}
package { "python3-docopt":
  require => Exec["update docopt"],
}
