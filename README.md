# ADS-B Flight to KML #

## Introduction ##

This is a collection of two python scripts, one to capture ADS-B and MLAT data from a running
dump1090 instance and store it in CSV files.  Each CSV file contain one day's worth of data (based
on UTC), and the other script to generate KML files from the data in the CSV file.  The KML files
can then be  viewed in Google Earth as shown below.

![](https://c1.staticflickr.com/1/658/32469774155_930de0bbff_b.jpg)

Detailed steps are provided below to configure your workstation with the necessary tools for
generating the KML files.  If your PC is already configured with the items as described in the
requirements, you may need to adjust the scripts in order for it to work properly.

****Note that the script to create the KML files have been used successfully with Apache Spark
2.0.2 with Hadoop 2.6 and do not work properly with newer versions of Apache Spark and Hadoop.****

## Scripts ##

#### capture_dump1090.py ####
Captures ADS-B and MLAT data from a running dump1090 instance and stores it in a CSV file.

#### process_dump1090.py ####
Analyses the data in the CSV file and create KML files based on certain criteria(s), or no criteria
at all. Criteria includes creating KML files for all flights, exclude or include MLAT, flights that
was in a holding pattern, or flights that are passes through certain coordinates/altitude (e.g.:
for capturing flights that arrives/departs from an airport).
          
## Requirements ##

The *process_dump1090.py* requires the following, aside from Python 2.7 or 3.x.  

* Scala: https://www.scala-lang.org/download/

* Apache Spark 2.0.2 with Hadoop 2.6: http://spark.apache.org/downloads.html

* latest Java JDK: http://www.oracle.com/technetwork/java/javase/downloads/jdk8-downloads-2133151.html

* Microsoft C++ Redistributable Package 2010: https://www.microsoft.com/en-us/download/details.aspx?id=26999

* winutils: https://github.com/steveloughran/winutils (click on the download then download zip)

## Configuration of prerequisites ##

* Install Scala with default settings
* Download Apache Spark and open the tar, if you do not have a tool that can open tar files, use
  7-Zip
* If using 7-Zip to open the tar file, you should see a *spark-2.0.2-bin-hadoop2.6* file, double
  click on that file to view the contents
* Extract the *spark-2.0.2-bin-hadoop2.6* folder into *C:\spark*,  you should now have various
  folders under *C:\spark\spark-2.0.2-bin-hadoop2.6*
* Create *spark-warehouse* folder under *C:\spark\spark-2.0.2-bin-hadoop2.6*
* In the *C:\spark\spark-2.0.2-bin-hadoop2.6\conf* folder, copy *spark-defaults.conf.template* to
  *spark-defaults.conf*
* Using your favourite text editor other than Notepad, open *spark-defaults.conf* and append the
  below line to the file and save

       spark.sql.warehouse.dir            file:///C:/spark/spark-2.0.2-bin-hadoop2.6/spark-warehouse

* Open the winutils zip file and browse to *winutils-master\hadoop-2.6.4*
* Extract the *bin* folder to *C:\spark*, you should now have *C:\spark\bin* with a bunch of files
  in it
* Install the Microsoft C++ Redistributable Package 2010 (prerequisite for winutils)
* Run the following command:

       C:\spark\bin\winutils.exe chmod 777 C:\spark\spark-2.0.2-bin-hadoop2.6\spark-warehouse

* Install the latest Java JDK
* Create these system environment variables (adjust for your version of Java installed)

       HADOOP_HOME=C:\spark
       SPARK_HOME=C:\spark\spark-2.0.2-bin-hadoop2.6
       JAVA_HOME=C:\Program Files\java\jdk1.8.0_121

* Append the below paths to the system path:

       C:\spark\bin
       %SPARK_HOME\bin
       %JAVA_HOME%\bin

* Run the below command, Windows firewall may ask you about something, allow it for private
  networks.

       C:\spark\spark-2.0.2-bin-hadoop2.6\bin\spark-shell.cmd

* There should be no errors, may have a WARN SparkContext, but nothing else.
* Type *:quit* to exit Scala.
* Configure the two Python scripts to suit your neads.
  * capture_dump1090.py
    * update the variables *url* and *ADSBDir* for your configuration, refer to comments in code
      on what these variables do
  * process_dump1090.py
    * update the variables *allFlights, showHolding, mlat* and *ADSBDir* for your configuration
      and purpose, refer to comments in code on what these variables do

## Usage ##

To start collecting data and saving to a CSV file, run the *capture_dump1090.py*.  This can be
done by simpy double-clicking on the file in a Windows environment if have Python 2.7, or from
the command line, such as `C:\Python27\python.exe <path to>\capture_dump1090.py`. Changes are
required in the script if you wish to use Python 3.x.  I use an old laptop running this script
on bootup, saving the data to a mapped network drive (as defined in the variable *ADSBDir*).

To analyze a CSV file, ensure that the variables in the *process_dump1090.py* are configured the
way you want.  Run the *process_dump1090.py*.  For testing you can use the CSV file from 
*sample dump1090_2017-02-03.zip*.  The script then create the KML files in a sub-folder named 
*sample 2017-02-03*.  When processing your own CSV files, the sub-folder will be named using the
YYY-MM-DD format.  Once the KML files have been created, an explorer window will appear showing
all of the KML files which you can then drag them into Google Earth to visualize.  

## History ##

Originally, I have been saving the data from my dump1090 using various revisions of a vbscript
running on an old laptop since January 2015.  Tableau was used to plot data which worked to some
degree but was not ideal, later tried R, but that too was not ideal.  Both were slow in processing
large sets of data.  It wasn't until the holiday break in December 2016 that I was nudged (she
claims it was more than a nudge, and more like pushed off a cliff....) to play around with Python,
Pyspark, Apache Spark and Hadoop and using the data I had from the dump1090.  The time it took to
analyze the data was much quicker.

The processing of the ADS-B data first started in analyzing the flights and creating KML files,
then later splitting up a flight into individual flights if the flight had stops along the way
(ie.: Montreal to Toronto to Winnipeg).  The final goal was then to identify flights that were in
a holding pattern, still looking for a better to do this.

The code was then cleaned up along with migrating the capture script in vbscript to Python.  Both
scripts were then made available on GitHub in early February 2017 for others to use and improve.

Want to capture your own data? Check out FlightAware at http://flightaware.com/.

## On the to do list.... ###

* Find a better way of identifying planes in a holding pattern
* Filter out or fix data that has erroneous coordinates and/or altitude
* Update script to use newer version of Apache Spark and Hadoop
* Make a nice front end to allow the configuration of various options and save these options to a
  configuration file