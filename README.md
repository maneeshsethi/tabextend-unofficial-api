
# TabExtend Unofficial API (v0.1.0)

[tabExtend](https://tabextend.com) makes a great Chrome Extension that lets you create new tasks and notes on the fly. Unfortunately, the data is contained completely within tabExtend, and has no API to connect to your other systems and processes.

In this project, I wanted to create a simple system to interact with tabExtend so I could sync with my other systems. 

Because tabExtend is a Chrome extension, this API will open up a non-headless (fully-visual) Chrome browser with Selenium and automate tasks. This means you'll need to have a browser open for this to work.

This is a small project, and might break with any future changes in the tabExtend framework. 


## License

[MIT](https://choosealicense.com/licenses/mit/)


## Screenshots

![Screenshot-Google Chrome -New tabExtend-2021-12-03 at 14 06 31](https://user-images.githubusercontent.com/620799/144610471-a7301953-8205-4cf2-b47b-11d0175a2a80.png)
<img width="1059" alt="Screenshot-Sidekick -FastAPI - Swagger UI-2021-12-03 at 14 07 44" src="https://user-images.githubusercontent.com/620799/144610506-522622bc-7071-4d26-9af5-659c270f8cf6.png">


# How to Deploy TabExtend API

  

Requirements; Python3, Google Chrome

  

To test as a dev on a Mac with Chrome 0.96, do the following.

  

1.  `git clone` [`https://github.com/maneeshsethi/tabextend-unofficial-api.git`](https://github.com/maneeshsethi/tabextend-unofficial-api.git)
2.  `cd tabextend-unofficial-api/`
3.  _recommended_: `python3 -m venv venv && source venv/bin/activate`
4.  `python3 -m pip install -r requirements.txt`
5.  `cp .env-example .env && nano .env` and replace with your username and pass
6.  now start the server: `uvicorn main:app -host 0.0.0.0 --reload`
7.  That’s it! The server is now running. You can test and run the API commands by navigating to [http://localhost:8000/docs](http://localhost:8000/docs)

  

## Did you get a “Chrome Driver” error?

  

*   Go to [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads) from your chrome browser. Check the version of your existing chrome browser (About Chrome), and download the proper chromedriver for your system.Replace the ./chromedriver file in the /root of the repository with the correct chromedriver file.
    *   (By default, the chromedriver included in the repo is 0.96 for the Mac m1)

## For Production Use (with Zapier, etc) 

  

1.  Set up server with Ubuntu and VNC access.. I recommend 20.04 and Vultr. Here are the instructions: [https://www.vultr.com/docs/install-gui-environment-for-ubuntu](https://www.vultr.com/docs/install-gui-environment-for-ubuntu) .
2.  Once set up, VNC in — you should see a GUI and be able to open a browser (probably firefox is preinstalled). Open up a terminal.
3.  `git clone` [`https://github.com/maneeshsethi/tabextend-unofficial-api.git`](https://github.com/maneeshsethi/tabextend-unofficial-api.git)
4.  `cd tab extend-unofficial-api/`
5.  Once you’re set up, install google chrome by navigating to [https://www.google.com/chrome/](https://www.google.com/chrome/)
6.  Check the version of your installed chrome by opening chrome and viewing Help>About Chrome. Navigate to [https://chromedriver.chromium.org/downloads](https://chromedriver.chromium.org/downloads) and download the proper chrome driver for your system. The versions 0.96 are included in the repo/chromedriver directory. Replace the chromedriver exec file in the root of the repository with the correct chromedriver file.
7.  `sudo apt-get install python3 python3-pip tmux python3.9-venv`
8.  `tmux`
9.  _recommended_: `python3 -m venv venv && source venv/bin/activate`
10.  `python3 -m pip install -r requirements.txt`
11.  `cp .env-example .env && nano .env` and replace with your username and pass
12.  now start the server: `uvicorn main:app —host 0.0.0.0 --reload`
13.  You can now use the IP address of your server for Zapier requests and any other webhooks you might want.
## API Reference

```
GET /get_groupname/{group_id} Get Groupname

GET /get_all_groupnames Get All Groupnames

GET /get_item/{group_id}/{item_id} Get Item

GET /get_all_items/(group_id} Get All Items From Group

GET /get_all_items Get All Items

GET /is_logged_in Is Logged In

POST /add_item/{text} Add Item

POST /add_item/{group_id}/(text} Add Item

POST /add_item Add Item

POST /do_item_action/(group_id}/{item_id}/{action} Do Item Action

GET /get_todo_state/{group_id}/{item_id} Get Todo State

POST /mark_checkbox_todo/(group_id}/(item_id}/(completed) Mark Checkbox Todo

POST /mark_checkbox_todo/(group_id}/(item_id} Mark Checkbox Todo

GET /get_item_type/{group_id}/{item_id} Get Item Type

```
