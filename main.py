from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
TELEGRAM_TOKEN = '7923867650:AAEwTiMIk1FGEX7hXuXDlDc7EmajPpERRL0'

def get_price(source):
    url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd"
    response = requests.get(url)
    return float(response.json()['bitcoin']['usd'])

async def btc_price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        price_coingecko = get_price("coingecko")
        formatted_coingecko = "{:,.2f}".format(price_coingecko)
        await update.message.reply_text(f'Coingecko: {formatted_coingecko} USD')
    except requests.exceptions.Timeout:
        await update.message.reply_text('La solicitud ha excedido el tiempo de espera. Por favor, intenta de nuevo más tarde.')

def main():
    application = Application.builder().token(TELEGRAM_TOKEN).read_timeout(20).write_timeout(20).build()
    btc_handler = CommandHandler('btc', btc_price)
    slash_handler = MessageHandler(filters.Regex(r'^/$'), btc_price)
    application.add_handler(slash_handler)
    application.add_handler(btc_handler)
    application.run_polling()

if __name__ == '__main__':
    main()