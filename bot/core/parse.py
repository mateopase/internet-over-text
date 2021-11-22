import argparse

from .reddit import add_reddit_parser


class Parser(argparse.ArgumentParser):
    def print_usage(self, file):
        pass

    def print_help(self, file):
        pass

parser = Parser(description="Browser", prog="browse")
sites_parser = parser.add_subparsers(help="Sites", dest="site")
add_reddit_parser(sites_parser)
