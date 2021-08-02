# Yi-Home_Telegram_Bot_Interface
Ditch Xiaomi's cloud and use a Telegram bot instead
***
## Features
+ Motion detection
> Works by monitoring a tmp file that is created only when the camera detects a motion
![IMG_2953](https://user-images.githubusercontent.com/45854343/127867115-da841676-2be6-4328-a8c3-335d1801fd0a.PNG)

+ Get a picture from the camera
> Uses the snapshot.sh functionality to get a real time picture
![IMG_2958](https://user-images.githubusercontent.com/45854343/127867139-5e337947-62d4-4481-90c2-19cfc313a7fd.PNG)

+ Multi camera support
> Add as many cameras as you please

+ The bot works in groups and there's a API limit bypass
> Multiple bot token can be added to round robin the requests (Telegram bots cannot send many messages per second in a group chat)

+ Text to speech to all cameras
> Use the speak.sh functionality to convert text to audio. Supports en-US, en-GB, de-DE, es-ES, fr-FR, it-IT

+ Text to speech to a single camera
> Same but limited to a single camera

+ Play any preconfigured sound to all cameras
> Play any audio from a specified folder (default: sound/). Use ffmpeg to convert it to the needed format

+ Play any preconfigured sound to a single camera
> Same but limited to a single camera
![IMG_2957](https://user-images.githubusercontent.com/45854343/127867186-5a267597-7146-466e-94c9-2e5f4a35a371.PNG)

+ Send a voice note and it will play on all cameras
> Send a voice message and ffmpeg will convert it and play simultameusly to all cameras
![IMG_2952](https://user-images.githubusercontent.com/45854343/127867198-459bdc37-5f80-46c9-ae74-d636883a1e83.PNG)

+ Alert if a camera goes offline
> No description

+ Alert if a camera goes online
> No description

+ Function to enable/disable motion notification
> Mute the camera alerts
![IMG_2956](https://user-images.githubusercontent.com/45854343/127867218-77129b4d-50c4-448c-86bc-f7a7b9f1fd49.PNG)

+ Function to enable/disable the camera while retaining the audio functionalities
> Disable video and photo functionalities of the camera
![IMG_2955](https://user-images.githubusercontent.com/45854343/127867233-244d9274-6174-450a-8e65-cb3ea66bf6c0.PNG)
![IMG_2954](https://user-images.githubusercontent.com/45854343/127867248-46935386-5c8a-4da8-bbc0-16bbc97c595b.PNG)

+ Media retention settings
> All media are saved into a folder (default: recording/) and will be deleted in X days. Set 0 to delete immediately

+ Multi language
> Currently supports IT and EN languages. You can add more by adding a locale file in config/
![IMG_2951](https://user-images.githubusercontent.com/45854343/127867263-75aea1ab-ef87-4573-8309-32d1f37f02c8.PNG)


## Note
+ No need for Xiaomi's cloud service (The app is needed only for the first setup)
+ The cameras don't need to connect to the internet so they will work fine in a isolated vlan
> If you have a UniFi access point you can add a Wi-Fi network with a custom VLAN else you can simply use a dedicated access point

+ You'll need to install Yi-Hack firmware on the camera and enable FTP and motion recording
> https://github.com/TheCrypt0/yi-hack-v4
> https://github.com/roleoroleo/yi-hack-MStar
> https://github.com/roleoroleo/yi-hack-Allwinner
> https://github.com/roleoroleo/yi-hack-Allwinner-v2

+ For the text to speech functionality you'll need to install the extra nanotts package
> https://github.com/roleoroleo/yi-hack-utils

+ A Raspberry/Docker or LXC Container/VM needs to be connected to the isolated network and to a network with internet access

+ There's 2 branches, one with a lot of emojis in the text and one with none

## How to use
Edit config/config.py and add your bot api token and the cameras ip address and nickname and then run main.py

## Dependencies
https://github.com/python-telegram-bot/python-telegram-bot
urllib
ftplib
requests
> I'm not sure which one are already packaged with Python 3
