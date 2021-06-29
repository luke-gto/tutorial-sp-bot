# Tutorial shitposting Telegram bot
#### _The most boring, buggy and useless bot ever created_

This is a telegram bot that makes random and pointless tutorials. You can use a keyword to generate the title or you can feed the bot with your beautyful title. If you don't feel inspired, the bot can pick a random title. In the [examples folder](https://github.com/luca-go/tutorial-sp-bot/tree/master/examples) you can find some... examples.

## Features

- It may work as intened

## Installation

You could install this using a Python virtual environment but you could encounter a couple of issues. For a smooth installation I'd suggest you to use Docker. A couple of steps below are specific for Linux-based distros but if you use MacOS or Windows and you know how to use a Dockerfile, you'll do this in 5 minutes.

1. Install [Docker](https://docs.docker.com/get-docker/).

2. Clone this repository:

    ```sh
    git clone https://github.com/luca-go/tutorial-sp-bot
    ```
    
3. Create a telegram bot with [Bot Father](https://t.me/botfather) and copy the API TOKEN

4. In the folder

    ```tutorial-sp-bot/src```

    there's the file

    ```.env```

    Open it and paste the API TOKEN you got from Bot Father. The file content should look like this:

    ```
    API_TOKEN='YOUR TOKEN HERE'
    ```

5. In the direcotry```tutorial-sp-bot``` launch the terminal and run this command to build the Docker image:

    ```
    docker build -t telegram-shitposting-bot .
    ```

    It may take a couple of minutes to finish.
    
6. Now you can launch the bot by typing:

    ```
    docker run -d tutorial-shitposting-bot
    ```
    
7. Now open the chat with the bot you created at step 3, tap on "Start" and enjoy(?).

**P.S.:** Remember to edit the .env file and rebuild the image (Step 5) when you change the API token of your bot.

****

The bot could be a bit buggy, feel free to open an issue if needed. 
