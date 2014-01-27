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
alias reprise='PYTHONPATH=/home/vagrant/reprise/ python3 -m reprise'
cd /home/vagrant/reprise
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
      /vagrant/reprise/tests/private.key",
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

# set up local ssh keys

exec { "ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa":
  creates => "/home/vagrant/.ssh/id_rsa.pub",
  user => "vagrant",
  environment => ["HOME=/home/vagrant/"],
}

exec { "cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys && \
      ssh-keyscan -t rsa localhost >> ~/.ssh/known_hosts":
  user => "vagrant",
  environment => ["HOME=/home/vagrant/"],
  unless => "grep vagrant@reprise /home/vagrant/.ssh/authorized_keys",
  require => Exec["ssh-keygen -t rsa -N '' -f ~/.ssh/id_rsa"],
}
