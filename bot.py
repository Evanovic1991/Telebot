import requests
from telegram import Update
from telegram.ext import Updater, CommandHandler, CallbackContext

# إعداد مفاتيح API
TELEGRAM_BOT_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
COINMARKETCAP_API_KEY = "YOUR_COINMARKETCAP_API_KEY"
COINMARKETCAP_URL = "https://pro-api.coinmarketcap.com/v1/cryptocurrency"

# وظيفة جلب سعر العملة
def get_price(crypto: str):
    headers = {'X-CMC_PRO_API_KEY': COINMARKETCAP_API_KEY}
    params = {'symbol': crypto.upper(), 'convert': 'USD'}
    response = requests.get(f"{COINMARKETCAP_URL}/quotes/latest", headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        price = data["data"][crypto.upper()]["quote"]["USD"]["price"]
        return f"سعر {crypto.upper()} هو: ${price:.2f}"
    return "تعذر الحصول على البيانات. تأكد من رمز العملة."

# أوامر البوت
def price_command(update: Update, context: CallbackContext):
    if len(context.args) == 0:
        update.message.reply_text("يرجى تحديد رمز العملة. مثال: /price BTC")
    else:
        crypto = context.args[0]
        price = get_price(crypto)
        update.message.reply_text(price)

# تشغيل البوت
def main():
    updater = Updater(TELEGRAM_BOT_TOKEN)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("price", price_command))
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
