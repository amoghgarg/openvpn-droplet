import paramiko
import digitalocean
import os

######## Configuration required ########
# Generate an API token from the digitalocean console.
# You need to do this only once.
apiToken = "3ae7749f75e2b6ff582b476d73fb41288ef30ee23fd518101c8c4c7cfc363802"

# Location of the remote server
# Possible values:
# AMS1, AMS2, AMS3, BLR1, FRA1, LON1, NYC1, NYC2, NYC3, SFO1, SFO2, SGP1, TOR1
# i.e amsterdam, bangalore, france, new york, san fransisco, singapore, toronto.
# Updated list might be on: http://speedtest-sfo1.digitalocean.com/
region = 'blr1'
########################################

###### Configuration may be required ######
# You need to upload your **public** SSH key to
# digitalocean. Do it from the webconsole, it is a one time step.

# This script will need your **private** key to provision(set up)
# your server once it is up.
defaultSSHKeyPath = os.path.expanduser("~")  + "/.ssh/id_rsa"

# Using the default path to your ssh key. You can choose to use
# some other path.
privateSSHKey = defaultSSHKeyPath
###########################################

##########################################
serverConfFile = 'server.conf'
staticKeyFile = 'static.key'
clientConfFile = 'client.conf'
staticKeyFileRemote = '/etc/openvpn/static.key'

manager = digitalocean.Manager(token=apiToken)
###########################################


## Create a ssh connection object to given hostname
def getSSHConnection(hostname):
  print "Connecting.."
  sshcon   = paramiko.SSHClient()  # will create the object
  sshcon.set_missing_host_key_policy(paramiko.AutoAddPolicy())
  sshcon.connect(hostname, username="root", key_filename=privateSSHKey)
  print "Connected."
  return sshcon

## Install openvpn, generate static key and set up NAT on the remote server.
def setupVPN(sshcon):
  print "Installing openvpn and setting up NAT on remote server..."
  setupCommands = [
  "sudo apt-get --yes --force-yes install openvpn",
  "openvpn --genkey --secret " +  staticKeyFileRemote,
  "sudo modprobe iptable_nat",
  "echo 1 | sudo tee /proc/sys/net/ipv4/ip_forward",
  "sudo iptables -t nat -A POSTROUTING -s 10.4.0.1/2 -o eth0 -j MASQUERADE"
  ]
  for comm in setupCommands:
    stdin , stdout, stderr = sshcon.exec_command(comm)
    print stdout.read()
    if len(stderr.read()) > 0:
      print(stderr.read())

## Copy the server conf for openvpn to the remote
def configureServer(sshcon):
  print "Copying open vpn server config to the remote server..."
  with open(serverConfFile) as f:
    serverConf = f.read().splitlines()
  for line in serverConf:
    cm = "echo " + line + " >> /etc/openvpn/server.conf"
    stdin , stdout, stderr = sshcon.exec_command(cm)
    if len(stderr.read()) > 0:
      print(stderr.read())

## Get the static key from the remote server
def getStaticKey(sshcon):
  print "Getting openvpn key from the server..."
  key = open(staticKeyFile, "w")
  stdin , stdout, stderr = sshcon.exec_command("cat " + staticKeyFileRemote)
  key.write(stdout.read())
  key.close()
  if len(stderr.read()) > 0:
    print(stderr.read())

## Start the openvpn daemon on the remote.
def startVPNServer(sshcon):
  print "Starting openvpn on remote server..."
  stdin , stdout, stderr = sshcon.exec_command("sudo service openvpn@server start")  #TODO: change status to start
  print stdout.read()
  if len(stderr.read()) > 0:
    print(stderr.read())

## Add the IP address of the created server to
## client conf file
def createClientConfig(ipadd):
  os.system("cp ./client.conf.template ./client.conf")
  os.system("echo remote " + ipadd + " >> ./client.conf")
  keyPath = os.getcwd() + '/' + staticKeyFile
  os.system("echo secret " + keyPath + " >>./client.conf")


## Create a new remote server(droplet) in the digital ocean
## cloud. Return its IP address.
def createServer():
  print "Creating a new remote server in %s..." % (region)
  keys = manager.get_all_sshkeys()
  droplet = digitalocean.Droplet(token=apiToken,
                               name='vpnServer',
                               region=region,
                               image='ubuntu-16-04-x64',
                               size_slug='512mb',
                               ssh_keys=keys,
                               backups=False)
  droplet.create()
  actions = droplet.get_actions()
  print droplet
  print droplet.name
  print droplet.ip_address

  setup = False
  print actions
  for action in actions:
      setUp = action.wait()

  if setUp:
    droplet.load()
    ip_address = droplet.ip_address
    print "Remote server was created. IP Address: " + ip_address
    return ip_address
  else:
    print "Remote server could not be created."
    return 0

## Check if any droplets are online.
## Returns IP address of either a new server or an existing one,
## depending on user input.
def getIPAddress():
  print "Checking if any server already on..."
  droplets = manager.get_all_droplets()
  count = len(droplets)

  if count > 0:
    print "You already some servers online. Choose from one of the following options:"
    for idx, d in enumerate(droplets):
      print '%d. Name: %s, IP: %s, Region: %s' % (idx+1, d.name, d.ip_address, d.region['name'])
    print '%d. Create a new droplet.' % (count+1)
    choice = int(raw_input('Choose from one of the above options [1 to %d]: ' % (count+1)))

    if choice == count + 1:
      return createServer()
    else:
      return droplets[choice-1].ip_address
  else:
    print "No servers were found online."
    return createServer()



def main():
  ipadd = getIPAddress()
  print 'Configuring %s' % (ipadd)
  createClientConfig(ipadd)
  sshcon = getSSHConnection(ipadd)
  setupVPN(sshcon)
  configureServer(sshcon)
  getStaticKey(sshcon)
  startVPNServer(sshcon)
  sshcon.close()

  print "\nRemote VPN server has been set up and your client configuration file"
  print "client.conf has been created. Use this to connect to the VPN."
  print "Start openvpn daemon on Linux, or Tunnelblick on Mac with this conf."

if __name__ == "__main__":
  main()
