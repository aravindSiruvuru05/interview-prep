Design a web scraperProvided with initial set of URLsScrape all possible nested urls and find images in all urls and return the list against parent urlMultiple followups

Round 5: ManagerialQuestions around situations how I handled a project with vague requirementsHow I helped a team member growConflict with manager

We are working on a clone of Facebook. We want to add a numeric count to every post showing how many friends the post's author has at the time of viewing the post, like
USER
 'user_id' (primary key)
 name' 
'created_date' 
 
USER RELATIONSHIP 
 'friendship_id' (primary key, unique to each relationship) ) 
 'user_id' (indexed)
 'user2_id' (indexed)
 'Start_date'
 
Focusing on the database, how would you implement the friend-count feature? Note we will soon be more popular than Facebook, so the solution needs to scale.
 
2.) We are working on a clone of Google Docs.
The software has the following features and limitations: Multiple users may work on a single document at the same time.
 * A document must be handled by a single server, no matter how many users are * We have a fixed number of servers which will be sufficient to handle our exp properly.
Our load balancer uses a round-robin system to permanently assign documents to each server will have an equal number of documents. 
Do you have any concerns about this load balanging system?
In those cases scalability, how to fix this issue
 
3.) Which consistency model is more appropriate for each of these applications: strong or eventual consistency? Why? 
 An API call that needs to respond within 20 milliseconds, used to retrieve meta video stream. The metadata includes things like the author name, rating, and view 
A web analytics platform recording every single click on a popular web page. 
A banking system that makes deposits and payments to checking accounts.
 
4.) Another scenario was something like that there was a bug on an application, and you ended up having a lot of failed requests. You have a database that stores all IDs that are there, and you also have large log files from about 500 different production servers that log the IDs of the successful requests. How would you come up with a solution to find the IDs that were missing/
 
 
We are working on a service that generates subtitles for users' videos. This process starts a new thread for every video and is processor-intensive. Currently, this service runs as a single process on a machine. 
We've run into a bug where if the service is processing more than 10 videos at the same time, the service crashes the server, losing all requests currently being processed and affecting other processes on the machine. It may take a long time to find and fix this bug. What workarounds could we implement to continue running the service while we do ?
 
2.) You're working on infrastructure for internet-connected vending machines. The plan is to install around 188,888 of these vending machines in the coming year, in major cities around the world. These machines will connect to the internet through cellular network.
Each machine will connect to a central server at midnight to report remaining stock and any maintenance issues like coin jams or stuck items. These machine status updates will be stored in a database, and a batch job will run at 1 AM to schedule the restocking and maintenance of machines. Are there any problems with the above design?
How to solve these problems?
 
3.) We are working on a mobile app for the board game Go. We'd like to add a feature where the computer will analyze a complete game. The analysis looks at each position from the game and provides suggested moves to help improve our users' play. We've found a library we can use to do this analysis. It takes an average of a minute on a modern desktop computer to analyze entire game. An average game consists of about 200 moves. We are considering two approaches. 1) running this analysis on the phone itself, and 2) sending the game to a server farm for analysis that will be returned to the user.
 What are some advantages or disadvantages of each approach ?
 
4.) We are running a simple photo storage and sharing service. People upload their photos to our servers and then give links to other users who can then view them. Instead of using a cloud service, we have our own server farms. You've been tasked with creating an estimate of the storage required over the coming year and the cost of that storage
What information would you need and what factors would you consider as you generate this estimate?
 
5.) We are running a simple photo storage and sharing service. People upload their photos to our servers and then give links to other users who can then view them. We're trying to figure out how to split the photos and associated data evenly onto multiple machines, especially as we get new users. We've decided to shard the photos evenly alphabetically by username. For example, if we had 26 servers, all the usernames starting with awould be on server 1, usernames starting with b' would be on server 2, and so on. We have created a scheme like this that will work for any number of servers. 4 5 Are there any problems with this design?
How to solve these?