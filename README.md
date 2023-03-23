# Ov-bike-availability-NL
For the course online data collection and management, our team scraped data from all stations in the Netherlands that provide OV-bikes. NS, the railway company of the Netherlands, provide these so called OV-bikes. There are in total 284 stations in the Netherlands where you can rent the bikes. We scraped data of all the 284 stations in the Netherlands for a period of 7 days with an interval of 15 minutes. We collected data about the number of bikes that are available in total and the current availibility of bikes. Moreover, we collected standard information about the type of bicycle storage and the address. We also stored the date and time of when the data was scraped, so we knew about which moment the availibility of bikes was. To give an overview, we scraped:

* Date
* Time
* Name of the station
* Total bikes 
* Current availability
* Type of facility
* Address

As mentioned before, we scraped for a period of 7 days and with intervals of 15 minutes. Of course, it is impossible to scrape 7 days in a row, every 15 minutes manually. We did this with the help of a virtual computer. We copied our code to a virtual computer and ran our Python script every 15 minutes with the help of a cronjob. The type of virtual computer we used was an EC2 instance offered by Amazon Web Services (AWS). AWS also offers a so called s3 bucket; this is a cloud storage service and it allows you to store and retrieve any amount of data from anywhere on the web. We used this tool to automatically store the data every 15 minutes in the cloud, so we were sure the data was stored safely. We can show the roadmap of our project graphically in the graph below, were the project is divided into three parts:

<img src="https://scrapeovfiets.s3.amazonaws.com/Roadmap.png" alt="Roadmap">

## Dependencies
For the installation of an virtual computer (EC2 instance) you can follow the steps on [this installation guide](https://tilburgsciencehub.com/tutorials/scale-up/running-computations-remotely/cloud-computing/).

We can also show in steps how we did it:

### Launch an EC2 instance via AWS
We launched an EC2 instance via Amazon Web Services (AWS) by following the steps from the [Running Computations Remotely article](https://tilburgsciencehub.com/tutorials/scale-up/running-computations-remotely/cloud-computing/) on Tilburg Science hub. This way, we got an EC2 instance as shown in the picture below:

<img src="https://scrapeovfiets.s3.amazonaws.com/EC2.png" alt="EC2 instance" width = "900">

### Connect to EC2 instance
The next step was to connect to the EC2 instance via our terminal. this had to be done by specifying the HOST and the KEY variable by running the following commands in our terminal:
```dash
export HOST=<OUR-PUBLIC-IPV4-DNS>
export KEY=<PATH_TO_OUR_KEY_PAIR_FILE>
```
You than use the `ssh` command to actualy connect to the instance:
```dash
ssh -i /path/to/key.pem ec2-user@<EC2-instance-DNS>
```
We then got the following output in our terminal, which meant we were connected to our EC2 instance:

<img src="https://scrapeovfiets.s3.amazonaws.com/Connecting_to_EC2.png" alt="Connecting to EC2 instance" width = "500">

### Move python script from own computer to EC2 instance
The next step was to move our python script to our EC2 instance so we can, in the next step, run it via our cronjob. First, we needed to make sure we were in the directory where our python script was located via the terminal (with cd commands). We then ran one line of code to copy files to the EC2 instance:
```dash
scp -i $KEY -r $(pwd) ec2-user@$HOST:/home/ec2-user
```

### 2.4 Set up a cronjob to run the code every 15 minutes
The code now needed to be executed every 15 minutes automatically. This was done by setting up a cronjob on our EC2 instance. In small steps, the following was typed in our terminal while connected with the EC2 instance:
1. ` crontab -e `: this opened the vim editor
2. `I`: this allowed us to type a cronjob in the vim editor
3. `*/15 * * * * /usr/bin/python3 /home/ec2-user/ScrapeFiets/ScrapeFiets.py `: the cron syntax '`*/15 * * * *`' means that the code runs all the time with an interval of 15 minutes. `/usr/bin/python3` is the path to the python installation on our EC2 instance. To know this path to our python installation, we runned the code below once in python. `/home/ec2-user/ScrapeFiets/ScrapeFiets.py ` is the path to our python script.
4. ` :wq `: this way, we closed the vim editor and saved the cronjob. 

Now we could verify our crontab was set up by running `crontab -l` and seeing our crontab line.

```
# finding the path to the python installation on the EC2 instance
path = os.path.dirname(sys.executable)
print(path)
```

# About
This respository was made by Jonas Klein, Matthijs van Gils, Marijn Bransen, Lisa Holling and Roos van Sambeek and was commissioned by Hannes Datta, proffesor at Tilburg University as part of the course 'Online data collection & management'.
