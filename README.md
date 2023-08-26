# internet over text
I was traveling a lot in 2021, and back in those days, most flights didn't offer free wifi.
However, most of them offered free IP-based messaging, so iMessage, WhatsApp, and Facebook Messenger all worked.
The idea is: if I can build a CLI tool for accessing the internet, why can't I just put that behind an API and access it
through one of these messaging applications.

## Overview
This tool is really two parts:
1. A Facebook Messenger bot. It runs on Heroku (really, used to run on Heroku, RIP), and handles the webhooks for the
   messenger bot I set up. The webhooks we care about here are just received messages.
2. A Reddit API client that loads subreddits, posts, and comments based on the incoming message.

## On state
When you're browsing Reddit, you generally maintain some sort of state in your browser.
You know which subreddit you're on, then which post you're looking at, and so on.
I didn't want to bother building state into the bot itself.
If you retrieve a post XYZ from a subreddit via the CLI, and want to look at comments, you run the "comments" command on post XYZ.

This is tedious. The cool thing about FB Messenger is that, when a bot responds, it can respond with text and special buttons for the
user to tap. The buttons can be preloaded with text that gets sent back to the bot. In this case, the text is just a CLI command that does what the button says.

So, to solve this, when anything gets loaded, I also send along a bunch of buttons for important actions I'd like to be able to take.
For example, if I load a post, I also send the following buttons:
- Back -> takes you back to the subreddit post list
- Comments -> lets you read the first page of comments

Then when the comments are loaded, there are buttons that let you page through the comment pages.
When a subreddit is loaded, the buttons just represent each loaded post, so you can tap a button to load a post. Next and prev buttons are also available for paging.

Pretty neat, right?

# Future work
This bot is dead since heroku killed the free tier. I also just wanted to make it work, so there are a few half-dead features like SMS support floating around in there.

And the whole button functionality was implemented in a few nights of excitement, so once I got it working, I never cleaned it up.

It's okay though, most flights have free wifi nowadays. We live in the future.
