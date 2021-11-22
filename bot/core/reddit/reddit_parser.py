from argparse import ArgumentParser


def add_reddit_parser(subparser: ArgumentParser):
    reddit_parser = subparser.add_parser("reddit")
    reddit_subparsers = reddit_parser.add_subparsers(help='Type of content', dest="content")

    subreddit_parser = reddit_subparsers.add_parser("subreddit")
    subreddit_parser.add_argument("subreddit", type=str, default="front")
    subreddit_parser.add_argument("-s", "--sort", type=str, default="hot", choices=["hot", "new", "top"])
    subreddit_parser.add_argument("-t", "--time", type=str, default="day", choices=["hour", "day", "week", "month", "year", "all"])
    subreddit_parser.add_argument("-p", "--page", type=int, default=1)

    post_parser = reddit_subparsers.add_parser("post")
    post_parser.add_argument("post_id", type=str)

    comment_parser = reddit_subparsers.add_parser("comments")
    comment_parser.add_argument("post_id", type=str)
    comment_parser.add_argument("-s", "--sort", type=str, default="top", choices=["best", "new", "top", "controversial"])
    comment_parser.add_argument("-p", "--page", type=int, default=1)

