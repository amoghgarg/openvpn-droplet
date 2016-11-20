## Setup cheap and reliable VPN in a single step..
after some initial setup. To access **regionally restricted** services.
### Why am I setting it up myself?
Read [this](./Motivation.md) for a detailed answer.   
**tl;dr** Want to watch cricket. Not available in Japan. This set up is **very reliable** and is **billed by the hour**. Costs about JPY 1/hour (INR 0.6/hour) or about JPY 40 (INR 24) for a complete Test match.
### Techinical things you should know to use this repository
1. Concept of VPN: The VPN being set up here is simply to access geo restricted websites through servers which are allowed to access them. For example www.hotstar.com broadcasts cricket but only for IPs accessing it from India. So we will set up a server in India and access *hotstar* through that server.
2. [DigitalOcean](https://www.digitalocean.com/): They let you set up servers accross different locations around the world. DigitalOcean likes to call these remote servers ***droplets***. You will need to create an account with DigitalOcean (requires credit card). You can use this [referal link](https://m.do.co/c/bb17d2f9f1e8) to sign up and get $10 credit :).
3. [OpenVPN](https://openvpn.net/): This software is used to tunnel all traffic from your computer(client) through the remote server you create in the digitalocean cloud. So if you open *hotstar* on your browser, *hotstar* will fell it is receiving the requests from the DigitalOcean server. And since the server is located in India, hotstar will have no problems returning responses to your requests. This repo will show you how to set up OpenVPN.
4. SSH: After creating up a server on Digital Ocean, it needs to be configured so that it can behave as a vpn server. To configure it, you need access to it. SSH is a protocal which lets you access the server. Simply put, you need to have a pair of private and public ssh keys. And you need to upload your **public keys** to DigitalOcean [security page](https://cloud.digitalocean.com/settings/security).

### What does this repo do
Actually, this repo is not really needed. Setting up a server on DigitalOcean and configuring it as a VPN server is a one time step. And then you can choose when to connect to it. BUT, leaving the server on will cost you $5 per month. Which is not a very big amount.
However, I only need the server only when there is a cricket match on. So I don't need to pay the entire $5. But setting up the everytime is a repetitive chore.
So, **this repository was written to automate the process of spinning up the DigitalOcean server and setting it as a VPN server.**

### Enough gyan, lets get it up
##### Requirements
- Your machine needs:
    - [Tunnelblick](https://tunnelblick.net/downloads.html) if you have MacOs. It is GUI client for OpenVPN.
    - OpenVPN if you have Linux (I have tested this script on Ubuntu)
    - python 2.7
    - python libraries you may need to install: [paramiko](http://www.paramiko.org/installing.html),  [digitalocean](https://github.com/koalalorenzo/python-digitalocean)
    - pip may be needed to install the python libraries
    - A set of SSH keys
    
##### Initial Setup
- Create an account on DigitalOcean (requires credit card or other payment method). Get $10 credit if you use this [referal link](https://m.do.co/c/bb17d2f9f1e8)
- Generate an API [token](https://cloud.digitalocean.com/settings/api/tokens) and copy it.
- Paste the generated token into the `create.py` file on [line 8](./create.py#L8):

    ```
    apiToken = "<TOKEN HERE>"
    ```
- Upload your ssh private key to the DigitalOcean [security page](https://cloud.digitalocean.com/settings/security)
- **If** path to your SSH **private** key is not "~/.ssh/id_rsa", set the correct path in `create.py` on [line 24](./create.py#L24):

    ```
    privateSSHKey = "<complete/path/to/private/sshKey>"
    ```
Now your are all set to spin up a vpn server.

##### Want to set it up manually?
In case you want to set up the VPN server only once follow [this](./Manual%20Setup.md) guide. I would suggest looking at it because it may help you debug in case the running the `create.py` script fails on your machine.

##### Create the VPN
Run the python script:
```
$ cd <this repo>
$ python create.py
```
If this script ran with out throwing any errors, a server was set up and configured to run as vpn server. You will see a new file called `client.conf` in the repo folder. To connect to the vpn server you need to start OpenVPN on your machine.    
If you are on Mac, double click on the `client.conf` file to open it with Tunnelblick. This will add the configuration to Tunnelblick. Now click on connect.    
If you are on Ubuntu run the following command :
```
$ cd <this repo>
$ sudo mv client.conf /etc/openvpn/
$ sudo service openvpn@client start
```
On Ubuntu, you can also do the following to connect to VPN server.
```
$ openvpn --config client.conf
```

### Note
1. The `create.py` script will by default spin up a server in Bangalore. You can change the region in the code. [List](http://speedtest-sfo1.digitalocean.com/) of available locations.
2. The server created has 512 MB memory. It is billed at about $0.007/hour maxing out to $5 per month.
3. Regarding data limits, $5 server has a upper limit of 1000 GB transfer limit. However DigitalOcean currently does not charge for data transfer above this limit. Also, there is no way to see the usgae limit on Digital Ocean console.
4. Hotstar's stream in 720p usualy is about 1GB for one hour.
5. The conf files here only support single client at a time, you will need to modify them to support multi clients
6. Only IPv4 address tunneling is handled in the current configuration.
