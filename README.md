Web Scrapping Bot
=============

Web Scrapping Bot is a Telegram bot designed to help users find the most relevant links from a specified website based on their queries. It leverages web scraping, transliteration, and fuzzy matching techniques to deliver accurate and efficient results.

## Table of Contents
1. [Features](#features)
2. [Installation](#installation)
3. [Configuration](#configuration)
4. [Usage](#usage)
5. [Code Overview](#code-overview)
6. [Logging](#logging)
7. [Troubleshooting](#troubleshooting)
8. [Contributing](#contributing)
9. [License](#license)
10. [Author](#author)

## Features


-   **Telegram Bot Integration**: Responds to user queries on Telegram.
-   **Web Scraping**: Uses Selenium and BeautifulSoup to scrape and parse website content.
-   **Transliteration**: Converts Hindi text to and from Devanagari script to handle various transliteration variants.
-   **Fuzzy Matching**: Identifies the most relevant links by matching query keywords with link text and URLs.
-   **Cooldown Mechanism**: Implements a cooldown period between user queries to prevent spamming.
-   **Caching**: Stores previously fetched links to improve response times for repeated queries.

## Installation

Ensure you have the following Python packages installed:

-   `requests`
-   `beautifulsoup4`
-   `fuzzywuzzy`
-   `indic_transliteration`
-   `python-telegram-bot`
-   `selenium`
-   `webdriver-manager`
-   `chromedriver-binary`

You can install these packages using pip:

```sh
pip install requests beautifulsoup4 fuzzywuzzy indic_transliteration python-telegram-bot selenium webdriver-manager
```

## Configuration

1.  **Set Up Telegram Bot Token**: Replace the `TOKEN` variable with your own Telegram Bot API token. Obtain this token by creating a bot on Telegram.

2.  **Update the Target URL**: Modify the `url` variable in the `handle_message` function to point to the website you want to scrape.

## Usage

1.  **Run the Bot**: Execute the script using Python:

    ```sh
    `python telegram-bot.py`
    ```

2.  **Interact with the Bot**: Start a chat with your bot on Telegram and send a query. The bot will respond with the most relevant link found on the specified website.

## Code Overview

-   **`scrape_website_with_selenium(url)`**: Scrapes the website's content using Selenium and BeautifulSoup.
-   **`transliterate_query(query)`**: Converts the query between ITRANS and Devanagari scripts.
-   **`find_most_relevant_link(query, soup)`**: Identifies the most relevant link based on the query.
-   **`start(update, context)`**: Handles the `/start` command.
-   **`handle_message(update, context)`**: Processes user messages and responds with relevant links.
-   **`main()`**: Sets up and starts the Telegram bot.

## Logging

The bot uses Python's built-in logging module to provide information about its operations. Logs are set to `INFO` level by default.

## Troubleshooting

-   **Web Scraping Issues**: Ensure that the website you are scraping allows automated access and that the URL is correct.
-   **Telegram API Issues**: Verify that your Telegram Bot token is valid and that your bot is correctly set up.

## Contributing

Feel free to submit issues or pull requests if you find bugs or want to add new features. Contributions are always welcome!

## License

This project is licensed under the [MIT License](LICENSE).

## Author

- **Ashis Srivastava**
  - GitHub: [Ashish Srivastava](https://github.com/shouttolearnorg)
  - LinkedIn: [Ashish Srivastava](https://www.linkedin.com/in/text-ashish/)

---

Made with ❤️.

* * * * *
