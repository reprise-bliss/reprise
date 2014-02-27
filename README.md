# Reprise

Reprise is an easy to use Debian repository and package management
tool - a simple, easy to setup, and daemon-less software with an
intuitive interface.

Reprise is meant to be run on the actual package server, not the client
machine uploading and managing packages. This way an unnecessarily
complicated client-server model is avoided. No daemon is running and
Reprise itself knows nothing about network communications.

## Feature overview

With Reprise you can easily manage as many Debian repositories as you like.
All you need to do is to install Reprise itself and provide SSH access to the
machine it runs on. For simplicity reasons the classical Debian stages like
`stable`, `testing`, `unstable` etc. are left out. Instead it is recommended
to create repositories with different names.

Repositories can be updated from one another by simply overwriting. So if you
are about to decide that the packages in your repository work properly together
use the update command to overwrite your old releases and put your new
development packages into a new repository.

Furthermore repositories can be pulled from other machines which might be
useful to deliver packages to Reprise instances which might run, for example,
on an EC2 instance.

## Installation

Because Reprise will write files to `/srv`, you should run all of its
commands __as root__.

First, create a default gpg key if you don't already have one:

    gpg --gen-key

This will take a long time, especially on virtual machines, which typically
don't have much entropy available.

Note: Reprise depends on `python3-docopt`, which you can find [in this PPA](https://launchpad.net/~stefano-palazzo/+archive/docopt).

To bootstrap Reprise you need to upload an initial package to a server and
install it using `gdebi` (*install gdebi-core, NOT the gdebi package*). From
then on you can use Reprise to host its own packages and this way update
itself. Once Reprise is installed, you can initialize the server:

    reprise init

## Usage

See: `reprise --help` or `man reprise`

### SSH alias

It's easy to use Reprise from the local command line with a simple shell
alias. Just define:

    alias rp='ssh <user>@<host> reprise'

Type `rp` and the Reprise help will be displayed. Use the `rp` command like
a local program and all commands will be sent to the server via SSH.

### Uploading Packages

Uploading packages is simply done via `scp`. Copy the Debian package into
`/srv/Reprise/incomming` like:

    scp <package> <user>@<host>:/srv/reprise/incomming/

Afterwards run `reprise include <repository> <package>` to make the package
available in your repository.

### The apt source line

To benefit from your new repository as usual an apt source needs to be added.
The corresponding line can be generated with `reprise source <repository>`.
Since it is impossible to auto detect the FQDN of the server running Reprise
you still need to set the proper host name in the source line.

You might have also realized that SSH is used in the source line. This
means that every computer that wants to access packages needs SSH
access to the machine which runs Reprise. This is a simple way to
provide security against unwanted access to the hosted packages. If
public access via HTTP is wanted a regular web server needs to be set up.

## Hacking

The test suite is located in `reprise/tests/`. You can run the tests by
typing `make test` (or `make coverage` to also ensure full code coverage).

Reprise also comes with a Vagrantfile and Puppet manifest, letting you set
up a testing environment using [Vagrant](http://vagrantup.com):

    vagrant up
    vagrant ssh
    make test
    make deb
