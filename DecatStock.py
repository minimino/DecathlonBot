import requests
from requests_html import HTMLSession
from time import sleep

# TODO: Currently the code doesn't look for stock in products with several options (e.g. Zapatillas)

# Looks up if a number of products are in stock and notifies a user whenever they are
def stock_finder(ITEMS):
    # Create HTML session
    session = HTMLSession()
    # IDs of the products
    # ids = ['969931', '970069']
    ids = ['970069']
    
    # For each items...
    for item in ITEMS:
        # Check a product's status
        products = session.get(ITEMS[item]).html.find('ul.sizes__list', first = True)
        
        for el in products.find('li'):
            # If the product is in stock, notify the user via Telegram's Decabot bot
            el_id = el.attrs['data-id']
            el_qty = el.attrs['data-available-quantity']
            
            if el_id in ids:
                print(el_id, el_qty)
            
            if el_id in ids and int(el_qty) > 0:
                print(item + ' is in stock!! Waking up DecaStockBot')
                telegram_bot(item, ITEMS[item])
                


# Notifies the user through a Telegram message sent by the Decabot bot
def telegram_bot(productName, productURL):

    # Chat information
    token = ""  # Bot token
    chatId = "" # Chat ID

    # Send message to chat
    requests.post('https://api.telegram.org/bot'+token+'/sendMessage?chat_id='+chatId+'&text=' + productName + ' is in stock!!')
    requests.post('https://api.telegram.org/bot'+token+'/sendMessage?chat_id='+chatId+'&text=Buy ' + productName + ' here: ' + productURL)


def main():

    # Waiting time between requests
    wait_time = 30
    counter   = 1

    # Dictionary composed of the names of the products to find and their URL
    ITEMS = {
        #'Rack': 'https://www.decathlon.es/es/p/rack-cross-training-musculacion-domyos-500-squat-traction/_/R-p-158534?mc=8380452',
        'Discos': 'https://www.decathlon.es/es/p/disco-de-fundicion-28-mm-musculacion-0-5-kg-a-20-kg-domyos-cross-fitness/_/R-p-7278'
    }

    while True:
        print('\nLooking for stock! Times searched: ' + str(counter))
        stock_finder(ITEMS)
        #print('\nWait ' + str(wait_time) + ' seconds for next request...')
        counter = counter + 1
        sleep(wait_time)

if __name__ == "__main__":
    main()
