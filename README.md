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

![Roadmap](https://github.com/Lisa-Holling/Ov-bike-availability-NL/raw/main/images/Roadmap.png)

## Repository Overview
```
├── README.md
├── .gitignore
└── src
    └── paper
 ```

## Dependencies
For the installation of an virtual computer (EC2 instance) you can follow the steps on [this installation guide](https://tilburgsciencehub.com/tutorials/scale-up/running-computations-remotely/cloud-computing/).

We can also show in steps how we did it:

### Launch an EC2 instance via AWS
We launched an EC2 instance via Amazon Web Services (AWS) by following the steps from the [Running Computations Remotely article](https://tilburgsciencehub.com/tutorials/scale-up/running-computations-remotely/cloud-computing/) on Tilburg Science hub. This way, we got an EC2 instance as shown in the picture below:

![EC2](https://github.com/Lisa-Holling/Ov-bike-availability-NL/raw/main/images/EC2.png)

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

<img src="https://github.com/Lisa-Holling/Ov-bike-availability-NL/raw/main/images/Connecting_to_EC2.png" alt="Roadmap" width="500">

### Move python script from own computer to EC2 instance
The next step was to move our python script to our EC2 instance so we can, in the next step, run it via our cronjob. First, we needed to make sure we were in the directory where our python script was located via the terminal (with cd commands). We then ran one line of code to copy files to the EC2 instance:
```dash
scp -i $KEY -r $(pwd) ec2-user@$HOST:/home/ec2-user
```

### Set up a cronjob to run the code every 15 minutes
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

### Linking to a S3 bucket
The last step was to link our EC2 instance to an s3 bucket. An s3 bucket is a cloud-based object storage service also offered by Amazon Web Services (AWS).
We used S3 buckets for backup and recovery, since we automatically uploaded the data to the s3 bucket every 15 minutes. This way, it can be accessed when needed and even when, in extreme cases, the EC2 instance crashes or gets hacked, we still have the lastest retrieved data in the cloud in our s3 bucket. An s3 bucket can be set up in a few steps:

### Creating an s3 bucket
First of all, we created an s3 bucket on our same AWS account as on which we created our EC2 instance. This was not that difficult and could be set up in minutes (see picture). Our s3 bucket was called 'scrapeovfiets'. The difficult part was creating the IAM role and linking the s3 bucket to the EC2 instance with the IAM role (see 3.2 and 3.3). 

![Bucket](https://github.com/Lisa-Holling/Ov-bike-availability-NL/raw/main/images/bucket.png)

### Creating an IAM role with s3:PutObject permissions
For the EC2 instance to be allowed to put objects in the s3 bucket, it needed to be assigned an IAM role. An IAM role can be compared to a permission that a mother grants to her child to play with certain toys in the house. The EC2 instance is the child, and the S3 bucket is the toy box. We thus needed to set up an IAM role in two steps:
1. Create a policy

    We first need to create a policy which is a permission to put objects in the s3 bucket (policies and permissions are used both, but have the same meaning). We did this by tying the following json formatted code in the json editor for creating a policy:

    ```json
    {
        "Version": "2012-10-17",
        "Statement": [
            {
                "Sid": "S3PutObject",
                "Effect": "Allow",
                "Action": [
                    "s3:PutObject"
                ],
                "Resource": [
                    "arn:aws:s3:::scrapeovfiets/*"
                ]
            }
        ]
    }
    ```
    We then could give our policy a name and save it. 

2. Create IAM role and assign policy

    Then we create an actual IAM role. In this step we can assign the policy created in step 3.2 to our IAM role. We then give our IAM role a name and save it. 


### Assign IAM role to the EC2 instance
So far, we have created an s3 bucket and we created an IAM role with s3:PutObject permissions. We now want to assign this IAM role to the EC2 instance, so the EC2 instance is allowed to put objects in the s3 bucket (we want the mother to give permissioins to the child to play with the toys). We do this by just connecting the IAM role to the EC2 instance.

![Assign IAM Role](https://github.com/Lisa-Holling/Ov-bike-availability-NL/raw/main/images/AssignIAMrole.png)

After we have connected the IAM role with the EC2 instance, we can tes in our terminal if it worked. For this, we have to connect with the EC2 instance in our terminal and type the following command in our terminal:
```dash
aws iam list-users
```
If everything worked, we should get the output:

<img src="https://github.com/Lisa-Holling/Ov-bike-availability-NL/raw/main/images/IAMroleterminal.png" alt="Roadmap" width="500">

### Include code in Python script that puts the json files in the s3 bucket
The last step was to include code in our Python script that puts the json files created in the script in our s3 bucket. The code for this can be found in the source code.

## Resources 
- Amazon EC2 - Secure and resizable 
	compute capacity – Amazon Web 
	Services. (z.d.). Amazon Web 
	Services, Inc. 
	https://aws.amazon.com/ec2/pricing/
- Amazon S3 Simple Storage Service Pricing Amazon Web Services. (z.d.). Amazon Web Services, Inc. 
https://aws.amazon.com/s3/pricing/ 
- Baumeister, T. (2019). The rise of shared 
	mobility: Understanding the challenges 
	and opportunities. Routledge.
- Horstman, M. (n.d.). Over deze website - 
	ovfietsbeschikbaar.nl. 
	https://ovfietsbeschikbaar.nl/over
- How to rent an OV-fiets | Door to door | NS. 
	(z.d.). Dutch Railways. 
https://www.ns.nl/en/door-to-door/ov-fiets/how-it-works.html
- Joshi, A., & Narayan, P. (2020). The emergence 
	of shared mobility: A review of the 
	literature. Transport Reviews, 40(6), 
	691-719.

- Openbaar Vervoer Nederland. (n.d.). OpenOV. 
	Retrieved March 16, 2023, from 
	https://openov.nl/.
- Koch, T. (n.d.). KV78Turbo-OVAPI Wiki. 
	Retrieved March 16, 2023, from 
https://github.com/koch-t/KV78Turbo-OVAPI/wiki.
- Pluister, B. (2022). OV-fiets: where to go?: A 
	study on OV-fiets user characteristics 
	and destinations. Master Thesis Civil 
	Engineering and Management, 
	University of Twente. 
http://essay.utwente.nl/93399/1/Pluister%20B.%201718150%20_openbaar.pdf
- Stichting OpenGeo. (n.d.). openOV. 
	https://openov.nl/
- Wu, X., Wang, Y., & Chen, Y. (2021). Shared 
	mobility in the age of smart cities: 
	Current status and future trends. 
	Sustainability, 13(7), 3227.

## About
This respository was made by Jonas Klein, Matthijs van Gils, Marijn Bransen, Lisa Holling and Roos van Sambeek and was commissioned by Hannes Datta, proffesor at Tilburg University as part of the course 'Online data collection & management'.
