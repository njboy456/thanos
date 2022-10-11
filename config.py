from sample_config import Config


class Development(Config):
    # get this values from the my.telegram.org
    APP_ID = 4524654
    API_HASH = "4cfbcd31ec888cc3f0709d8d20607ac8"
    # the name to display in your alive message
    ALIVE_NAME = "Շђคภ๏ร"
    # create any PostgreSQL database (i recommend to use elephantsql) and paste that link here
    DB_URI = "YOUR VALUE" # IF U DONT KNOW HOW TO MAKE THEN GO IN THANOS SUPPORT AND TYPE #DB_URI 
    # After cloning the repo and installing requirements do python3 stringsetup.py an fill that value with this
    STRING_SESSION = "YOUR VALUE"# IF U DONT KNOW HOW TO MAKE THEN GO IN THANOS SUPPORT AND TYPE #session 
    # --------------------------------------------------

    TG_BOT_TOKEN = "Your value"# create a new bot in @botfather and fill the following vales with bot token
    # create a private group and a rose bot to it and type /id and paste that id here (replace that -100 with that group id)
    PRIVATE_GROUP_BOT_API_ID = -1001638681164
    # command handler
    COMMAND_HAND_LER = "."
    VCMODE = "True"
    VC_SESSION = "your assistant id session"
    # command hanler for sudo
    SUDO_COMMAND_HAND_LER = "."
    # External plugins repo
    EXTERNAL_REPO = "https://github.com/rishabhanand2/tha_plugins"
    #don't edit this 
    THANOSABUSE = "False"#don't edit this
