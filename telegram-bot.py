import os
import requests
from bs4 import BeautifulSoup
from fuzzywuzzy import fuzz
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from collections import Counter

TOKEN = os.getenv('TELEGRAM_BOT_TOKE')
if not TOKEN:
    raise ValueError("Telegram bot token is not set.")
print(f'TOKEN: {TOKEN}')  # Add this line to verify the token


COOLDOWN_PERIOD = 10  # Cooldown period in seconds
user_last_response_time = {}  # To store last response time per user
link_cache = {}  # Cache to store fetched links

logging.basicConfig(level=logging.INFO)

def scrape_website_with_selenium(url):
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=chrome_options)
    driver.get(url)
    
    time.sleep(5)  # Adjust as necessary

    soup = BeautifulSoup(driver.page_source, 'html.parser')
    driver.quit()
    
    return soup

def transliterate_query(query):
    hindi_query = transliterate(query, sanscript.ITRANS, sanscript.DEVANAGARI)
    hinglish_query = transliterate(hindi_query, sanscript.DEVANAGARI, sanscript.ITRANS)
    return hindi_query, hinglish_query

def find_most_relevant_link(query, soup):
    relevant_links = []
    keywords = query.lower().split()
    keyword_count = Counter(keywords)

    main_links = soup.find_all('a', href=True)

    for link_tag in main_links:
        link_text = link_tag.text.strip().lower()
        link_url = link_tag['href'].lower()
        
        match_count = sum(keyword_count[keyword] for keyword in keyword_count if keyword in link_text)
        match_count += sum(keyword_count[keyword] for keyword in keyword_count if keyword in link_url)

        logging.info(f"Link: {link_tag['href']} Match Count: {match_count}")

        if match_count > 0:
            relevant_links.append((link_tag.text, link_tag['href'], match_count))
    
    relevant_links.sort(key=lambda x: x[2], reverse=True)

    if relevant_links:
        return relevant_links[0][0], relevant_links[0][1]
    else:
        return None, None

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text('Hello! Send me your query, and I will find the most relevant link.')

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user_id = update.message.from_user.id
    current_time = time.time()

    if user_id in user_last_response_time:
        last_response_time = user_last_response_time[user_id]
        if current_time - last_response_time < COOLDOWN_PERIOD:
            await update.message.reply_text("Please wait before sending another query.")
            return
    
    user_last_response_time[user_id] = current_time

    query = update.message.text
    url = 'https://www.shouttolearn.org/p/sitemap.html'

    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    if query in link_cache:
        text, link = link_cache[query]
    else:
        soup = scrape_website_with_selenium(url)
        if soup:
            text, link = find_most_relevant_link(query, soup)
            if link:
                link_cache[query] = (text, link)
        else:
            await update.message.reply_text("Failed to scrape the website.")
            return
    
    if link:
        await update.message.reply_text(f"Most relevant link found:\nText: {text}\nLink: {link}", disable_web_page_preview=False)
    else:
        await update.message.reply_text("No relevant link found.")

def main():
    application = ApplicationBuilder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    application.run_polling()

if __name__ == '__main__':
    main()

