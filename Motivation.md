### Why did I chose to set up my own vpn server

#### Why do I need VPN?
Lot of web services are restricted to a particular region. Hotstar is only available in India. Skysports EU only in EU. Australian Open video only in Australia.

#### How about paid VPN like zenmate, tunnelbear?
The ones I tried were very unreliable speed wise or had data limits or were costly. I don't want to pay >6~7 USD per month.

#### Did you try other cloud providers?
Yes, this repo is possible because of this [article](https://www.comparitech.com/blog/vpn-privacy/how-to-make-your-own-free-vpn-using-amazon-web-services/). As the article suggests, I set up an AWS account first and used it for about 1 week. However, AWS has very high data transfer rates (~$0.12/GB). Which works out to about ~$4 per test match!!  (AWS Free tier provides upto 15GB free transfer per month, ~ 2 ODIs).    
I then looked at other Virtual Server providers. I found that only DigitalOcean fulfills these criteria:

1. Easy spinning up new servers
2. Option of a cheap, very light weight server. Tunneling requires very low specs
3. Cheap data rates. Digital Ocean has virtually unlimited data transfer
4. Datacentre location in India

On top of it, they also provide APIs to interact with cloud. I have found the data transfer to be reliable as well uptill now.

#### Ok, how much will this setup cost?
There are two components to cost:
- **Compute (server/droplet charges)**: You need a very basic server. 512MB server on DigitalOcean costs $0.007/hour or $5/month, whichever is lower.
- **Data transfer**: Although 512MB server/droplet on DigitalOcean has 1000GB monthly limit, they don't enforce it currently. In anycase 1000GB is about 1000 hours of 720p video. (A month has 720 hours).

So if you leave the server on continuously, it will cost you $5/month. This repo can help you pay even less than that by running the server only when you need, i.e. $0.007/hour, billed by the hour.

I will add the following about DigitalOcean billing for sake of completeness:

1. If you spin up an instance for only 1 hour, they will charge you $0.01 (not $0.007) because that is minimum they can bill you for.
1. They round up third decimals to the next two decimals. For example, and instance running for 2.5 hours would be billed for 3 hours. Which is $0.021, but you will be billed for $0.03.

