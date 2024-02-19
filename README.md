# [RSS Summarizer Dashboard](https://rss-summarizer-feed.onrender.com)

## Overview
(Sorry I delayed a week on this project)

This project is a super simple dashboard for getting RSS feeds as even shorter summaries!

*RSS is very very cool and we need to make more use of it.*

With the help from Chat GPT, users get a short summary of all the latest updates from a feed on top of the feed itself, potentially making RSS even more useful.

RSS (Really Simple Syndication) is a semantic-web tool that keeps you updated by fetching the latest content from websites you're interested in. Instead of you visiting each website individually, RSS brings the new posts from these websites to you. It's like having a personal news feed for your favorite websites.

## Features
- **RSS Feed**: Submit the URL to generate RSS feed on the dashboard. (please check URLs forlder for list of URLs and *guide for creating or getting more feed URLs)
- **User-Friendly Interface**: Simplicity
- **AI Summary**: Stay informed in a glace


## Project Structure
The repository is structured as follows:
- `feed.py`: This is the entry point to the Dash UI.
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
(might take a while to load if the server has been inactive for this free deployment)

## Contributing
Contributions from the community are welcome and encouraged! Please feel free to checkout, add pull requests, or create issues for the repo as you see fit. Feel free to build on top of it on your own as well and I'd be happy to see it!

## Credit
This project is created by Weiqi Ji.

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

### Demonstrated Skills (for recruiters):
- Python Expert Level
- Software Development
