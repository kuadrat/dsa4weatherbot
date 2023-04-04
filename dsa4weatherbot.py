import telegram as tgm
import telegram.ext as tge

import dsa4weather.dsa4weather as dsa4w

## Callback data mappings
CB_SUMMER = 0
CB_AUTUMN = 1
CB_WINTER = 2
CB_SPRING = 3
CB_SEASONS = [dsa4w.SUMMER, dsa4w.AUTUMN, dsa4w.WINTER, dsa4w.SPRING]
CB_REGIONS = dsa4w.REGIONS
CB_SEASON_SELECT = 'Select season:'
CB_REGION_SELECT = 'Select region:'

class DSA4WeatherBot() :

    weather_models = {}

    def get_weather_model(self, update: tgm.Update) :
        if update.message is not None :
            chat_id = update.message.chat.id
        else :
#            chat_id = update.callback_query.chat_instance
            chat_id = update.callback_query.message.chat.id
        return self.weather_models[chat_id]

    async def start(self, update: tgm.Update, context: 
                    tge.ContextTypes.DEFAULT_TYPE) :
        await update.message.reply_text('Welcome to the DSA4 Weather Bot!')
        weather_model = dsa4w.DSA4Weather()
        self.weather_models.update({update.message.chat.id: weather_model})

        # Generate the relevant keyboards
        self.keyboard_seasons = [
            [
                tgm.InlineKeyboardButton(dsa4w.SUMMER, callback_data=0),
                tgm.InlineKeyboardButton(dsa4w.AUTUMN, callback_data=1)
            ],
            [
                tgm.InlineKeyboardButton(dsa4w.WINTER, callback_data=2),
                tgm.InlineKeyboardButton(dsa4w.SPRING, callback_data=3)
            ]
        ]

        self.keyboard_regions = []
        n_col = 2
        n_regions = len(dsa4w.REGIONS)
        i = 0
        while i < n_regions :
            row = []
            for region in dsa4w.REGIONS[i:i+n_col] :
                row.append(tgm.InlineKeyboardButton(region, callback_data=i))
                i += 1
            self.keyboard_regions.append(row)

    async def weather(self, update: tgm.Update, context: 
                      tge.ContextTypes.DEFAULT_TYPE) :
        """
        Guide user through a menu and create a random weather pattern
        """
        reply_markup = tgm.InlineKeyboardMarkup(self.keyboard_seasons)
        await update.message.reply_text('Select season:', 
                                        reply_markup=reply_markup)

    async def next_weather(self, update: tgm.Update, context: 
                      tge.ContextTypes.DEFAULT_TYPE) :
        """
        Develop the weather from an existing weather pattern.
        """
        w = self.get_weather_model(update)
        w.roll_next_weather()
        await update.message.reply_text('Weather for the next day is:\n' + 
                                        w.get_weather_string())

    async def callback_handler(self, update: tgm.Update, context: 
                               tge.ContextTypes.DEFAULT_TYPE) :
        text = update.callback_query.message.text

        # Apparently this needs to be present
        await update.callback_query.answer()

        # Decide what to do
        if text == CB_SEASON_SELECT :
            await self.on_season_select(update)
        elif text == CB_REGION_SELECT :
            await self.on_region_select(update)

    async def on_season_select(self, update: tgm.Update) :
        """ Set the weather model's season and query region. """
        w = self.get_weather_model(update)
        season = int(update.callback_query.data)
        w.season = CB_SEASONS[season]

        chat = update.callback_query.message.chat
        reply_markup = tgm.InlineKeyboardMarkup(self.keyboard_regions)
        await chat.send_message('Select region:', reply_markup=reply_markup)

    async def on_region_select(self, update: tgm.Update) :
        """ Once the region is selected, weather can be calculated. """
        w = self.get_weather_model(update)
        w.roll_new_weather()
        region = CB_REGIONS[int(update.callback_query.data)]
        w.region = region

        chat = update.callback_query.message.chat
        await chat.send_message(w.get_weather_string())

    async def help(self, update: tgm.Update, context: 
                   tge.ContextTypes.DEFAULT_TYPE) :
        await update.message.reply_text('Abandon all hope.')

    async def unknown(self, update: tgm.Update, context: 
                      tge.ContextTypes.DEFAULT_TYPE) :
        await update.message.reply_text('I don\'t understand this command.')

if __name__ == "__main__" :
    bot = DSA4WeatherBot()
    with open('token.txt', 'r') as f :
        token = f.readline()[:-1]
    app = tge.Application.builder().token(token).build()
    app.add_handler(tge.CommandHandler('start', bot.start))
    app.add_handler(tge.CommandHandler('help', bot.help))
    app.add_handler(tge.CommandHandler('weather', bot.weather))
    app.add_handler(tge.CommandHandler('next', bot.next_weather))

    app.add_handler(tge.CallbackQueryHandler(bot.callback_handler))

    # Filters out unknown commands
    app.add_handler(tge.MessageHandler(tge.filters.COMMAND, bot.unknown))

    print('Starting to poll...')
    app.run_polling()

