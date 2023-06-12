import hava_durumu
import il_ilce_verileri
import veritabani_islemleri as dbs
from telegram import Update , InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import MessageHandler, filters, CallbackQueryHandler, ContextTypes, ApplicationBuilder, CommandHandler

async def start(update:Update,context:ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    name = update.message.from_user.first_name
    last_name = update.message.from_user.last_name

    if not dbs.kullanici_var_mi(user_id):
        dbs.kullanici_ekle(user_id,name,last_name)

    await context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=f"Merhaba {update.effective_user.full_name} Ben Hava durumu bilgilerini sağlayan bir botum.Lütfen ilinizi yazınız:"
    )


async def iliCekIlceYap(update:Update,context:ContextTypes.DEFAULT_TYPE):

    user_id = update.message.from_user.id
    il= update.message.text

    if dbs.kullanici_var_mi(user_id):
        dbs.il_ekle(il,kullanici_id=user_id)

    keyboard = []
    for ilce in il_ilce_verileri.ileGoreIlceListesi(il=dbs.ili_cek(user_id)):
        keyboard.append([InlineKeyboardButton(ilce, callback_data=ilce)])
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("İlçeyi seçiniz:",reply_markup=reply_markup)


async def button(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    user_id = update.effective_user.id

    query = update.callback_query
    await query.answer()

    ilce_main = query.data
    if dbs.kullanici_var_mi(user_id):
        dbs.ilce_ekle(ilce_main.capitalize(),user_id)
    await query.edit_message_text(text=hava_durumu.mgm(il=dbs.ili_cek(user_id),ilce=dbs.ilceyi_cek(user_id))+hava_durumu.google_veri(ilce=dbs.ilceyi_cek(user_id),il=dbs.ili_cek(user_id))+"\n\nKonfigürasyon tamamlandı. Artık ne zaman isterseniz hava durumunu öğrenebilirsiniz. /sondurum yazmayı unutmayın :)")
async def secili(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    user_id = update.effective_user.id
    try:
        if not dbs.ilceyi_cek(user_id):
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text="Seçili ilçe bulunamadı"
            )
        elif not dbs.ili_cek(user_id):

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text = "Seçili il bulunamadı"
            )
        else:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"Seçili Il ilçe verileri = {dbs.ili_cek(user_id)},{dbs.ilceyi_cek(user_id=user_id)}"
            )

    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Seçili il,ilce bulunamadı"
        )
async def sondurum(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    try:
        user_id = update.effective_user.id
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text=hava_durumu.mgm(il=dbs.ili_cek(user_id),ilce=dbs.ilceyi_cek(user_id))+hava_durumu.google_veri(il=dbs.ili_cek(user_id),ilce=dbs.ilceyi_cek(user_id))
        )
    except:
        await context.bot.send_message(
            chat_id=update.effective_chat.id,
            text="Hatalı il ilce eşleşmesi lütfen il ya da ilçenin doğru olduğundan emin olunuz. Lütfen ili yazınız"
        )
async def ildegistir(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    try:
        if(dbs.ili_cek(update.effective_user.id)):
            pass
        await context.bot.send_message(chat_id=update.effective_chat.id,text="Lütfen değiştirmek istediğiniz ili yazınız")
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="Bir şeyler ters gitti, /start a basınız")


async def ilcedegistir(update:Update,context:ContextTypes.DEFAULT_TYPE)->None:
    try:
        user_id = update.effective_user.id
        keyboard = []
        for ilce in il_ilce_verileri.ileGoreIlceListesi(il=dbs.ili_cek(user_id=user_id)):
            keyboard.append([InlineKeyboardButton(ilce, callback_data=ilce)])
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text("İlçeyi seçiniz:", reply_markup=reply_markup)
    except:
        await context.bot.send_message(chat_id=update.effective_chat.id,text="Bir şeyler ters gitti, /start a basınız")

if __name__ == '__main__':
    application = ApplicationBuilder().token("BURAYA BOT TOKEN'I YAZILACAK").build()


    start_handler = CommandHandler('start',start)
    il_handler = MessageHandler(filters.TEXT & (~filters.COMMAND),iliCekIlceYap)
    secili_handler = CommandHandler('secili',secili)
    sondurum_handler = CommandHandler('sondurum',sondurum)
    ildegistir_handler = CommandHandler('ildegistir',ildegistir)
    ilcedegistir_handler = CommandHandler('ilcedegistir',ilcedegistir)

    application.add_handler(ilcedegistir_handler)
    application.add_handler(ildegistir_handler)
    application.add_handler(sondurum_handler)
    application.add_handler(secili_handler)
    application.add_handler(start_handler)
    application.add_handler(il_handler)
    application.add_handler(CallbackQueryHandler(button))
    application.run_polling()
