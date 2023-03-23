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
