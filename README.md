# Magnetron

Magnetron is a non-enterprise-ready Debian repository and package management
tool - a simple to setup deamon-less software with an intuitive interface.

Magnetron is mend to be run locally. All magnetron commands take place on the
machine where it is installed. This way an unnecessary complicated server
client model is avoided. No deamon is running and magnetron itself knows
nothing about network communication.

## Feature overview

With magnetron you can easily manage as much Debian repositories as you like.
All you need to do is to install magnetron itself and provide SSH access to the
machine it runs on. For simplicity reasons the classical Debian stages like
`stable`, `testing`, `unstable` etc. are left out. Instead it is recommended
to create repositories with different names.

Repositories can be updated from one another by simply overwriting. So if you
are about to decide that the packages in your repository work properly together
use the update command to overwrite your old releases and put your new
development packages into a new repository.

Furthermore repositories can be pulled from other machines which might be
useful to deliver packages to magnetron instances which might run for example
on an EC2 instance.

## Installation

To bootstrap magnetron you need to upload an initial package to a server and
install it using `gdebi` (*install gdebi-core, NOT the gdebi package*). From
then on you can use magnetron to host it's own packages and this way update
itself.

## Usage

See: `magnetron --help` or `man magnetron`

### SSH alias

It's easy to use magnetron from the local command line with a simple shell
alias. Just define:

    alias mt='ssh <user>@<host> "magnetron"'

Type `mt` and the magnetron help will be displayed. Use the `mt` command like
a local program and all commands will be sent to the server via SSH.

### Uploading Packages

Uploading packages is simply done via `scp`. Copy the Debian package into
`/srv/magnetron/incomming` like:

    scp <package> <user>@<host>:/srv/magnetron/incomming/

Afterwards run `magnetron include <repository> <package>` to make the package
available in your repository.

### The apt source line

To benefit from your new repository as usual a apt source needs to be added.
The corresponding line can be generated with `magnetron source <repository>`.
Since it is impossible to auto detect the FQDN of the server running magnetron
you still need to set the proper host name in the source line.

You also might realize that SSH is used in the source line too. This means that
every computer which wants to access packages needs SSH access to the machine
which runs magnetron. This is a simple way to provide security against unwanted
access to the hosted packages. If public access via HTTP is wanted a regular
web server needs to be set up.
