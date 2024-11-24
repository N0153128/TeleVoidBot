# Void Bot

### What is Void Bot?
Void Bot - is a general purpose Telegram Bot made to streamline bot creation process.
This bot can also add more features to both group and personal chats out of the box, as part of its Example modules.
Currently implemented features:
scenarios/motd - Work in progress
scenarios/political party - allows group chat members to separate into various parties and earn in-chat currency to redeem special actions.
scenarios/roleplay - allows group chat members to express their actions within a group chat using commands.
scenarios/telegraph - allows to create and quickly access created notes using Telegraph - works in both group and personal chats.


### How to Run
- ```pip install -r requirements.txt ```
- Fill in all required constants in the ``config-blueprint.py``
- rename ``config-blueprint.py`` to just ``config.py``
- Run the bot with ``python main_controller BOT_API_KEY``

### TODO:
~~automatically create logs/general.log file for general logging.~~
implement conditional MOTDs, where a user would report their condition to the bot and the next message will be tailored to the condition. Example 1: the user is feeling happy - the weather and wallet balance will be bolded. Example 2: the user is feeling sick - a tailored message, wishing them to get well will be displayed, money related rows will be removed.
add weather forecast for motd - highest & lowest temp + rain possibility
add unread email counter for motd
add ton difference 24h for motd
add FTUE features, such as auto-create ``config.py`` and request minimal required data for the config to run the bot

### Known Issues
- the bot would randomly crash if it was launched outside of the Docker environment.