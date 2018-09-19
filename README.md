# Secure Troop Fork 

## Real-time collaborative live coding

Secure Troop is a fork off of [Troop](https://github.com/Qirky/Troop/), which includes the real-time collaborative functionality of Troop, but in a secure environment. Essentially, it runs all python executable commands from FoxDot in a docker container, keeping the host machine safe from any malicious commands executed by other collaborators. The container will then send OSC messages to SuperCollider through the established localhost connection. 

Currently Secure Troop only works with FoxDot. 

## Getting Started 

For details on what Troop actually is and what you need to have installed, please refer to the [Troop guidelines](https://github.com/Qirky/Troop/README.md). 

Once you have the basic FoxDot setup up and running, complete the Secure Troop specifics below :: 

1. Make sure that FoxDot is in your python path (not pythonX).
( verify this by running the following command python -c "import FoxDot; print(FoxDot.\__file\__) )
2. Install Docker, and make sure the Docker client is running.
3. Start SuperCollider with FoxDot ( using FoxDot.start command)

## Running the application

1. sudo chmod +x run-secure-client.sh 

Build and run a docker container for the FoxDot python commands. 
2. ./run-secure-client.sh 

Start the ordinary Troop client, that now redirects FoxDot commands to a docker container. The container will send messages to SuperCollider on your host machine so you can hear your tunes. 
3. python run-client.py 

