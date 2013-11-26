'''
magnetron

Usage:
    magnetron [options]

Options:
    --help -h   show this screen and exit

'''

import docopt


def main(argv=None):
    args = docopt.docopt(__doc__, argv=argv)


if __name__ == "__main__":
    main()
