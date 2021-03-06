# Google Search Website: https://www.geeksforgeeks.org/performing-google-search-using-python-code/
# Translate https://www.tutorialspoint.com/python_text_processing/python_text_translation.htm
# Computer Search https://www.youtube.com/watch?v=XQgXKtPSzUI
# Synoyms https://stackoverflow.com/questions/43814754/python-beautifulsoup-how-to-get-href-attribute-of-a-element/43814994
# Weather https://www.thepythoncode.com/article/extract-weather-data-python

from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
from urllib.error import HTTPError
from googlesearch import search
import requests
import re
import random

def bing_search():
    i = 1
    session = requests.Session()

    # optional
    session.headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.61 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://www.google.com'
        }

    # hard code
    search = input("Bing search: ")

    print("loading search...\n")

    url = ('https://www.bing.com/search?q=' + search)
    webpage = session.get(url)

    if webpage.ok == True:
        html = soup(webpage.text,"html.parser")

        text = html.findAll('li',{'class':'b_algo'})

        for texts in text:
            print(str(i) + "." + texts.h2.text)
            print(texts.h2.a.get("href"))
            print()
            i += 1

    else:
        print("Could not load webpage!")
            
def translator():
    """Spanish To English 
    or English to Spanish"""
    
    # getting input from user
    string = input("Please enter an enlgish or spanish phrase: ")
    
    # converting string to a format the website can read it in
    
    if " " in string:
        string = string.replace(" ","%20")
    
    
    try:
        # downloading url with customized url based
        # on user's input
        my_url = "https://www.spanishdict.com/translate/" + string 

        client = uReq(my_url)
        html = client.read()
        client.close()
        translation = soup(html, "html.parser")
        phrase2 = translation.find("a", {"class" : "neodictTranslation--2vd6M2gR"})
        for word in phrase2:
            print(word)
    except:
        print("Connection Error. Please try again.")

        

def synonyms():
    """Ask the user on what word they want 
    to use to see what other associated words 
    are to that word."""
    valid = False
    
    while valid == False:
        # counter
        i = 1
        find_word = []
        word = input("Type in word for synonyms: ")
        print("Retrieving synonyms...\n")

        # scrapes browser and searches for synonyms
        try:
            my_url = "https://www.thesaurus.com/browse/"+ word + ""
            client = uReq(my_url)
            html = client.read()
            client.close()
            letter = soup(html, "html.parser")
            word_search = letter.findAll("div", {"class" : "css-16lv1yi e1qo4u831"})
            
            # Displaying results 
            for find_word in word_search:
                for found_word in find_word.findAll("a", {"class": "css-1kg1yv8 eh475bn0", "class" : "css-1gyuw4i eh475bn0", 'href' : True}):
                    user_word = found_word['href']
                    print(str(i) + "." +  user_word.replace('/browse/', " "))
                    i += 1
                    
            valid = True
        except HTTPError:
            print("Please enter a valid word.")

def fun_fact():
    """
    Displays a random fun fact to the user!
    """
    print("Retrieving a fun fact...")
    
    # counter
    i = 1
    
    # fun fact url
    fact = "https://bestlifeonline.com/random-fun-facts/"
    
    # downloads url
    fun = uReq(fact)
    
    # reads the url
    awesome = fun.read()
    
    # closes url
    fun.close()
    
    # reads the html format of url and stores it 
    # in many_facts
    many_facts = soup(awesome, "html.parser")
    
    title = many_facts.find("h1", {"class" : "post-title center-block"})
    print(title.text + "\n")
    
    # finds all the fun facts
    fun_facts = many_facts.findAll("div", {"class": "title"})
    
    # converts all fun facts to text format
    fun_facts_text = []
    for fun_fact in fun_facts:
        fun_facts_text.append(fun_fact.text)
    
    # chooses a random fun fact
    data = random.choice(fun_facts_text)
    
    print(data)
        
def computer():
    """Ask the user what computer part 
    that they want to research about and 
    display that product."""
    
    try:
        computer_part = input("Please type in any computer part: ")
        print("Retrieving parts data...\n")

        # Incase the user types a space
        # we cannot have an empty space in the website url
        if " " in computer_part:
            computer_part = computer_part.replace(" ","+")

        # new url based on user's input
        url = "https://www.newegg.com/p/pl?d="+ computer_part + ""
        downloaded_url = uReq(url)

        # stores website in html_read 
        html_read = downloaded_url.read()

        downloaded_url.close()
    except:
        print("Connection Error. Please try again.")

    # converts html_read to a readable format
    website = soup(html_read, "html.parser")

    # gets the title of all the possible parts on page
    item = website.findAll("a", {"class" : "item-title"})
    itemPrice = website.findAll("div", {"class" : "item-action"})

    # prompts user to enter to choose how many items they would
    # like to display

    try:
        if len(item) == 0:
            print("There were no items for " + computer_part + ".")
            itemsToDisplay = 0
        else:
            valid = False
            while valid == False:
                print("There are " + str(len(item)) + " items to be displayed.")
                itemsToDisplay = int(input("How many items would you like to display? "))

                if itemsToDisplay < 0 or itemsToDisplay > len(item):
                    print("\nThe number is not in range.")
                    print("Please enter a number between 0 and " + str(len(item)) + ".")
                else:
                    valid = True

    except:
        print("Please enter a number.")

    # new line
    print()

    # displays information
    counter = 0
    while counter != itemsToDisplay:

        print("ITEM TITLE: " + item[counter].text.strip() + "\n" +
              "ITEM PRICE: " + itemPrice[counter].text.strip() + "\n")

        # increments counter
        counter += 1

    
def weather():
    """
    Asks the user their zip code
    and displays the weather in
    that area.
    """
    valid = False

    while valid == False:
        try:
            # initializes a list and a dictionary
            next_days = []
            result = {}

            # Getting input from user
            zip_code = input("Please enter your zip code: ")
            print("Retrieving weather data...")

            if " " in zip_code:
                zip_code = zip_code.replace(" ","+")

            # creates the url
            weather_url = "https://www.estesparknews.com/weather/?mode=week&weather_zip=" + zip_code + ""

            # Downloads the information in the url
            hail = uReq(weather_url)

            # reads the information
            html_url = hail.read()

            # closes the url
            hail.close()

        except:
            print("Connection Error. Please try again. ")

            # ends the function
            valid = True

        # converting url to html 
        hot = soup(html_url, "html.parser")

        # getting location from the zip code
        location = hot.find("h3", {"class" :"weather-title"})
        location = location.text.strip()

        # Checks to see if zip code is valid    
        if location == 'Invalid Location':
            print("Please enter a valid zip code: ")
        else:
            valid = True

        # new line
        print()

    # Displays information
    for locate in hot.findAll("div", {"class" : "weather-index-week-container"}):
        day_name = locate.find("div", {"class" : "weather-index-time col-sm-1 col-xs-2 opacity-change"})
        high_temp = locate.find("div", {"class" : "high-temp"})
        low_temp = locate.find("div", {"class" : "low-temp"})
        details = locate.find("div", {"class": "col-sm-6 col-xs-12"})
        print(day_name.text, "\nHigh Temperature:", high_temp.text)
        print("Low Temperature: ", low_temp.text, "\nDetails", details.text)
        for cold in hot.findAll("div", {"class": "weather-panel-details"}):
            print(cold.text)
            
def famous_quotes():
    url_to_search = "https://www.inc.com/sujan-patel/101-inspiring-quotes-from-the-most-successful-people-in-history.html"
    find = uReq(url_to_search)
    search = find.read()
    find.close()
    inspiration = soup(search, "html.parser")
    quote = inspiration.findAll("div", {"class": "standardText"})
    famous_quotes = []
    for inspiration_quote in quote:
        famous_quotes.append(inspiration_quote.text)
    famous = random.choice(famous_quotes)
    print(famous)
    

def main(): 
    '''
    Displays commands that the
    user can access within the program
    '''
    userChoice = ''

    while userChoice.lower() != 'exit':

        print("\nType '1' or type 'bing search' - Bing Search (Search bing!)")
        print("Type '2' or type 'synonyms'- Synonyms (Displays similar words!)")
        print("Type '3' or type 'weather' for Weather")
        print("Type '4' or type 'fun fact' Fun Fact (Displays a random fun fact)")
        print("Type '5' or type 'translator' - Translator (English to Spanish / vice versa")
        print("Type '6' or type 'newegg'- Newegg (search for computer parts)")
        print("Type '7' or type 'famous quotes'- Newegg (search for computer parts)")
        print("Exit - to exit the program")
        print()
        userChoice = input("Please enter a command: ")
        print()
        
        if userChoice == "1" or userChoice == "bing search":
            bing_search()
        elif userChoice == "2" or userChoice == "synonyms":
            synonyms()
        elif userChoice == "3" or userChoice == "weather":
             weather()
        elif userChoice == "4" or userChoice == "fun fact":
            fun_fact()
        elif userChoice == "5" or userChoice == "translator":
            translator()
        elif userChoice == "6" or userChoice == "newegg":
            computer()
        elif userChoice == "7" or userChoice == "famous quotes":
            famous_quotes()
        else:
            print("Please enter a valid command!\n")

    print("\nThank you for using " +
    "our program!")
    
if __name__ == "__main__":
     main()
