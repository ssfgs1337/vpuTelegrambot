from telegram import Update, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, MessageHandler, filters, \
    CallbackQueryHandler

from handlers.base_handler import BaseHandler

FOREST, TENT, HUNTING, BERRIES, = range(4)


class TwoConversationHandler(BaseHandler):
    @classmethod
    def register(cls, app):
        conversation_handler = ConversationHandler(
            entry_points=[CommandHandler('begingame', cls.game)],
            states={
                FOREST: [MessageHandler(filters.Regex('^(Так|Ні)$'), cls.forest)],
                TENT: [MessageHandler(filters.Regex('^(Право|Ліво)$'), cls.tent)],
                HUNTING: [MessageHandler(filters.Regex('^(Піти|Заснути)$'), cls.hunting)],
                BERRIES: [MessageHandler(filters.Regex('^(Зїсти|Не їсти)$'), cls.berries)],
                # COMPLETION: [MessageHandler(filters.Regex('^(Зїсти)$'), cls.сompletion)]
            },
            fallbacks=[CommandHandler('exit', cls.exit)]
        )

        app.add_handler(conversation_handler)

    @staticmethod
    async def game(update: Update, context: ContextTypes.DEFAULT_TYPE):
        keyboard = [
            [KeyboardButton('Так'), KeyboardButton('Ні')],
        ]

        reply_text = ReplyKeyboardMarkup(keyboard)
        await update.message.reply_text(f"Вітаю {update.effective_user.first_name}! Чи бажаєте ви зіграти у гру?",reply_markup=reply_text)

        return FOREST

    @staticmethod
    async def exit(update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(f'Вихід з квесту')

        return ConversationHandler.END

    @staticmethod
    async def forest(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == 'Так':
            keyboard = [
                [KeyboardButton('Право'), KeyboardButton('Ліво')],
            ]


            reply_text = ReplyKeyboardMarkup(keyboard)
            await update.message.reply_text(
            f"""
            Ви попали у чарівний світ.Вам потрібно дістатись до замку.Піти на Право чи на Ліво   
            """, reply_markup=reply_text)

            return TENT
        elif answer == 'Ні':
            await update.message.reply_text(f'Ви обрали не грати в гру.')
            return ConversationHandler.END
        else:
            await update.message.reply_text(f'Ви написало щочь не те.')

    @staticmethod
    async def tent(update: Update, context: ContextTypes.DEFAULT_TYPE):
        answer = update.message.text
        if answer == 'Право':
            keyboard = [
                [KeyboardButton('Піти'), KeyboardButton('Заснути')],
            ]

            reply_text = ReplyKeyboardMarkup(keyboard)
            await update.message.reply_text(
            f"""
          Ви побачили замок але він був надто далеко чи підете далі?     
            """, reply_markup=reply_text)
            return HUNTING
        elif answer == 'Ліво':
            await update.message.reply_text(f'Ви повернули не туди і загинули.')

            return ConversationHandler.END

        elif answer == 'Заснути':
            await update.message.reply_text(f'Ви заснули і більше не прокинулись.', reply_markup=reply_text )



            return ConversationHandler.END

    @staticmethod
    async def hunting(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        answer = update.message.text
        if answer == 'Піти':
         keyboard = [
                [KeyboardButton("З'їсти"), KeyboardButton('Не їсти')],
            ]
         reply_text = ReplyKeyboardMarkup(keyboard)

         await update.message.reply_text(
    f"""
            Там було якесь незрозуміле дерево з яблуками. Будете їсти їх?       
             """, reply_markup=reply_text)
         return BERRIES
        elif answer == 'Відпочити':
            await update.message.reply_text(f'Ви були змучені і померли.')
            return ConversationHandler.END

    @staticmethod
    async def berries(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
        answer = update.message.text
        if answer == 'Піти':
            keyboard = [
                [KeyboardButton("З'їсти"), KeyboardButton('Не їсти')],
            ]
            reply_text = ReplyKeyboardMarkup(keyboard)
            await update.message.reply_text(
                f"""
                        Яблуко було отруєне
                         """, reply_markup=reply_text)
            return BERRIES
        elif answer == "З'їсти":
            await update.message.reply_text(f'Ви померли.')

            @staticmethod
            async def completion(update: Update, context: ContextTypes.DEFAULT_TYPE):
                keyboard = [
                    [KeyboardButton("З'їсти")],
                ]

                reply_text = ReplyKeyboardMarkup(keyboard)
                await update.message.reply_text(
                    f"Кінець {update.effective_user.first_name}!", reply_markup=reply_text)


            return ConversationHandler.END