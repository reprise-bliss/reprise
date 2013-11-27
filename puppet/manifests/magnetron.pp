Exec {
  path => "/bin:/usr/bin:/sbin:/usr/sbin",
  user => "root",
  logoutput => on_failure,
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
package { "python-dev": }
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

# import gpg test keys

exec { "import private key":
  command => "gpg --allow-secret-key-import --import \
      /vagrant/magnetron/tests/private.key",
  unless => "gpg --list-secret-keys | grep 3F479202",
  user => "vagrant",
  environment => ["HOME=/home/vagrant/"],
}

exec { "gpg --export -a > /home/vagrant/public.gpg":
  creates => "/home/vagrant/public.gpg",
  user => "vagrant",
  environment => ["HOME=/home/vagrant/"],
  require => Exec["import private key"],
}

# install coverage

exec { "easy_install3 coverage":
    creates => "/usr/local/bin/coverage3",
    require => [
        Package["python-dev"],
        Package["python3"],
        Package["python3-setuptools"],
    ]
}
