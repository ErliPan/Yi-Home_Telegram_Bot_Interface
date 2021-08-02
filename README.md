# Yi-Home_Telegram_Bot_Interface
Ditch Xiaomi's cloud and use a Telegram bot instead
***
## Features
⋅⋅* Motion detection
> Works by monitoring the a tmp file that is created only when the camera detects a motion

⋅⋅* Get a picture from the camera
> Uses the snapshot.sh functionality to get a real time picture

⋅⋅* Multi camera support
> Add as many cameras as you please

⋅⋅* The bot works in groups and there's a API limit bypass
> Multiple bot token can be added to round robin the requests (Telegram bots cannot send many messages per second in a group chat)

⋅⋅* Text to speech to all cameras
> Use the speak.sh functionality to convert text to audio. Supports en-US, en-GB, de-DE, es-ES, fr-FR, it-IT

⋅⋅* Text to speech to a single camera
> Same but limited to a single camera

⋅⋅* Play any preconfigured sound to all cameras
> Play any audio from a specified folder (default: sound/) use ffmpeg to convert it to the needed format

⋅⋅* Play any preconfigured sound to a single camera
> Same but limited to a single camera

⋅⋅* Send a voice note and it will play on all cameras
> Send a voice message and ffmpeg will convert it and play simultameusly to all cameras

⋅⋅* Alert if a camera goes offline
> No description

⋅⋅* Alert if a camera goes online
> No description

⋅⋅* Function to enable/disable motion notification
> Mute the camera alerts

⋅⋅* Function to enable/disable the camera while retaining the audio functionalities
> Disable video and photo functionalities of the camera

⋅⋅* Media retention settings
> All media are saved into a folder (default: recording/) and will be deleted in X days. Set 0 to delete immediately

⋅⋅* Multi language
> Currently supports IT and EN languages. You can add more by adding a locale file in config/


## Note
⋅⋅* No need for Xiaomi's cloud service (The app is needed only for the first setup)
⋅⋅* The cameras don't need to connect to the internet so they will work fine in a isolated vlan
> If you have a UniFi access point you can add a Wi-Fi network with a custom VLAN else you can simply use a dedicated access point

⋅⋅* You'll need to install Yi-Hack firmware on the camera and enable FTP and motion recording
> https://github.com/TheCrypt0/yi-hack-v4
> https://github.com/roleoroleo/yi-hack-MStar
> https://github.com/roleoroleo/yi-hack-Allwinner
> https://github.com/roleoroleo/yi-hack-Allwinner-v2

⋅⋅* For the text to speech functionality you'll need to install the extra nanotts package
> https://github.com/roleoroleo/yi-hack-utils

⋅⋅* A Raspberry/Docker or LXC Container/VM needs to be connected to the isolated network and to a network with internet access


## How to use
Edit config/config.py and add your bot api token and the cameras ip address and nickname and then run main.py

## Dependencies
https://github.com/python-telegram-bot/python-telegram-bot
urllib
ftplib
requests
> I'm not sure which one are already packaged with Python 3
