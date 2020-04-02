# Project 2

## Web Programming with Python and JavaScript

### Flack
It is the instant messaging application where person can send messages to one another in real time. Created as the Project 2 of CS50W 2020 batch.
The server side language used is Flask and client side language is javascript and i used flask-socketio to create the duplex channel between client and server such that they can communication with each other. I also used bootstrap 4 for the appearance of the application.

### Features
* Username entered should be unique and must have length > 0.
* As soon as the channel created,  it will be shown to each and every client without refreshing the page.
* Channel name must be unique and must have length > 0.
* Users can talk to each other in real time without need to refreshing the page.
* The name and the timestamp will be associated with each and every message.
* I took care of accidently pressing the send button as the users cannot send blank messages because the send button will remain disabled by default if the length of message typed is null.
* You can see at the top the number of active users.
* Session is also stored so that if the user closes the browser and opens the app again,  then it will redirect him/her directly to where he/she left (whether inside any channel or at the channel list along with their name).
