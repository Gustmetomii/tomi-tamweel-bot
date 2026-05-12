import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = os.environ.get('TOKEN')
PORT = int(os.environ.get('PORT', 8443))

# الخدمات - هنزودها بعدين
SERVICES = {
    "telegram": "📢 خدمات تيليجرام",
    "tiktok": "🎵 خدمات تيك توك", 
    "youtube": "▶️ خدمات يوتيوب",
    "whatsapp": "💬 خدمات واتساب"
}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎁 الخدمات المجانية اليومية", callback_data='free')],
        [InlineKeyboardButton("💎 خدمات التمويل المدفوعة", callback_data='paid')],
        [InlineKeyboardButton("📊 رصيدك", callback_data='balance')],
        [InlineKeyboardButton("👨‍💻 صانع البوت: تومي", url='https://t.me/akosomak')] # غير اليوزر بتاعك
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🔥 **أهلا بيك في بوت تمويل تومي** 🔥\n\n"
        "أقوى بوت خدمات شرعية 100% للسوشيال ميديا\n"
        "ليك خدمتين مجاني كل 24 ساعة ✅",
        reply_markup=reply_markup,
        parse_mode='Markdown'
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'free':
        await query.edit_message_text("🎁 **الخدمات المجانية:**\nقريباً...")
    elif query.data == 'paid':
        text = "💎 **اختار المنصة:**"
        keyboard = [[InlineKeyboardButton(name, callback_data=f'service_{key}')] for key, name in SERVICES.items()]
        keyboard.append([InlineKeyboardButton("🔙 رجوع", callback_data='back')])
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    elif query.data == 'balance':
        await query.edit_message_text("📊 **رصيدك:** 0 جنيه\n\nاشحن رصيدك من @akosomak")
    elif query.data == 'back':
        await start(update, context)

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    # ده المهم لـ Render عشان ميفصلش
    app.run_webhook(
        listen="0.0.0.0",
        port=PORT,
        url_path=TOKEN,
        webhook_url=f"https://{os.environ.get('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    )

if __name__ == '__main__':
    main()
