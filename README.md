# [RSS Summarizer Dashboard](https://rss-summarizer-feed.onrender.com)

## Overview

This project is a simple dashboard for viewing RSS feeds.

RSS (Really Simple Syndication) is a semantic-web tool that keeps you updated by fetching the latest content from websites you're interested in. Instead of you visiting each website individually, RSS brings the new posts from these websites to you. It's like having a personal news feed for your favorite websites. 

My hope is more people will learn about RSS and keep innovating in the RSS community to keep it alive because it is seriously useful and it has been the backbone of information for interent search engines like Google, and it can have many practical applications for people to browse internet that doesn't involve using a traditional browser software -- ie. more ways and more direct ways to interface with information on the internet in the future.

These days, there are less and less RSS feeds being maintained by websites, and the quality of the some RSS feeds being maintained are going down as well -- that's more reasons why we need to widely adopt RSS.

On the other hand, you can still easily generate your own RSS feeds from any website using free RSS tools online, and that's always a plus, because there's many things you could do with your own customized RSS feed, think IoT!

With this project, I wanted to try compacting the RSS feed information being delivered to me even further just for fun, using GPT. The idea sounded better than in practice, but here it is, and some of the code can plucked by AI to be recycled in other coding projects.

## Features:
- test RSS feed URLs, and get summaries of their feeds.
- GPT will also assign a [Up-to-date]/[Deprecated] Rating.
- ask GPT to generate a summary for the feed based on its entries (won't always be useful)

## Ideas
- modify code to subscribe to many many RSS feeds
- modify code to rank RSS sources based on completeness, informativeness, etc.
- make a RSS summarizer bot that sends notifications when there's an update
- build and maintain a live database of valid RSS urls

## Project Structure
The repository is structured as follows:
- `src/app.py`: This is the entry point to the Dash UI.
- `rss_tools.py`: File containing necessary functions for working with RSS.
- `URLs/`: This directory contains a json file as well as a pdf file keeping a list of known URLs.

## Getting Started
To get started with this project on your computer: 
1. Clone the repository & set up environment
2. Generate GPT API key
3. Save the API key locally using shell
    - MacOS: `echo "export OPENAI_API_KEY='YOUR_API_KEY'" >> ~/.zshrc`
    - Windows: `setx OPENAI_API_KEY "YOUR_API_KEY"`
4. Installing packages: `pip install -r req.txt`
5. Launch the Dash application: `python feed.py`
6. Navigate to `http://127.0.0.1:8050/` to interact with the app

This project is also currently hosted at [https://rss-summarizer-feed.onrender.com](https://rss-summarizer-feed.onrender.com)

## Contributing
Contributions from the community are welcome! This started as a small weekend project, but if you find this project helpful and you're interested in contributing, please feel free to do so!

## Credit
This project is created by Weiqi Ji and licensed under the MIT license.

### Footnote:
This project is proud to be part of the RSS reader community!

Other existing choices are:

- (my favorite) RSS.app
- Feedly
- FeedReader
- The Old Reader
- Feed Demon
- InoReader
- RSS Owl
- NewsBlur
- Digg Reader
