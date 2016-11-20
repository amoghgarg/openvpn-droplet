#### Set up the VPN server manually
This section will help you set up the VPN server manually. Doing this manually will atleast once will show you what the script `create.py` is doing.
First you need to finish the one time set up described (here)[Initial Setup]. Follow this guide after that:
1. [Create](https://cloud.digitalocean.com/droplets/new]) a new droplet/server on DigitalOcean. Choose Ubuntu distro, $5/month size. Do not forget to ADD the SSH keys you uploaded earlier to DigitalOcean console. You can leave all the options unchecked.
1. After the Droplet is created, [find](https://cloud.digitalocean.com/droplets) out its IP Address.
1. SSH into the new droplet
    ```
    local:$ ssh root@<ip address>
    ```
1. Once inside the droplet, run the following commands. Notice that the last command will create a key to access the vpn.
    ```
    remote:$ sudo apt-get install openvpn
    remote:$ sudo modprobe iptable_nat
    remote:$ echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward
    remote:$ sudo iptables -t nat -A POSTROUTING -s 10.4.0.1/2 -o eth0 -j MASQUERADE
    remote:$ cd /etc/openvpn
    remote:$ openvpn --genkey --secret static.key
    ```
1. Create a server conf file `/etc/openvpn/server.conf` in the **remote** droplet with the following content:
    ```
    port 1194
    proto tcp-server
    dev tun1
    ifconfig 10.4.0.1 10.4.0.2
    status server-tcp.log
    verb 3
    secret  vpn.key
    ```
1. Start the openvpn daemon on the remote server
    ```
    remote:$  sudo service openvpn@server start
    ```
1. Copy the `/etc/openvpn/static.key` file you created just a moment ago to your local machine. `remote:$ cat /etc/openvpn/static.key` will show you the contents on the terminal, you can copy paste this and save to a local file `static.key`.
1. Create a local `client.conf` file with the following content. Replace the IP address and the secret path.
    ```
    proto tcp-client
    port 1194
    dev tun
    redirect-gateway def1
    ifconfig 10.4.0.2 10.4.0.1
    remote <droplet IP>
    secret "/complete/path/to/static.key"
    ```
1. Connect to the openvpn server. On linux, copy the `client.conf` file to `/etc/openvpn/` on your local machine and run `local:$ sudo service openvpn@client start`. On Mac, double click on the `client.conf` file to open it with Tunnelblick and click on connect.
1. If everything went well, all your traffic should be routed through the remote server. To check, search for `my ip` on google, it should the IP address of the droplet you just created.