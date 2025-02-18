# Setup
In your client (the program that will be requesting quotes), add the following to setup a connection to the server:
```
import zmq

# Create context (allows for socket creation)
context = zmq.Context()

# Create request socket
socket = context.socket(zmq.REQ)

# Connect to localhost:5555, this is the port that the server listens to.
socket.connect("tcp://localhost:5555")
```
# Retrieving A Random Quote
To request data, we'll use the previously created socket to send different strings which act as commands to request different data.
### Requesting a Random Quote
The following line will request a random quote:
```
socket.send_string("quote")
```
### Recieving a Random Quote
Once a quote has been requested, recieve and store the quote in the variable "message" with the following line:
```
message = socket.recv()
```
### Arguments
Add "-f" at the end of the command to request a favorite quote, and add "-nf" to request a non-favorite quote (if no additional arguments are present, the quote will be randomly chosen from a pool including the favorites list and the default list)
```
# Request a favorite quote
socket.send_string("quote -f")

# Request a non-favorite quote
socket.send_string("quote -nf")
```
### Errors
If an error occurs, due to unrecognized arguments or too many arguments being passed, the server will send back a string starting with "Error." and then a description of the error, instead of a quote.
# Adding a Quote To Favorites
To add the most recently retrieved quote to the Favorites list, send the following command:
```
socket.send_string("fav")
```
The server will either send back "True" or "False", based on if the favoriting succeeded (e.g., it will send back "False" if it couldn't find the quote, or if a quote hasn't yet been sent). This response can be retrieved with the following line:
```
message = socket.recv()
```
# Deleting a Quote
To delete the most recently retrieved quote, send the following command:
```
socket.send_string("del")
```
The server will either send back "True" or "False", based on if the deletion succeeded (e.g., it will send back "False" if it couldn't find the quote, or if a quote hasn't yet been sent). This response can be retrieved with the following line:
```
message = socket.recv()
```
# Adding a Quote
To add a quote, send a command of the following format:
```
socket.send_string("add QUOTE_CONTENT @ AUTHOR")
```
Where QUOTE_CONTENT is the actual quote itself, and AUTHOR is the author of the quote. 
It's important to note that the AUTHOR is optional, BUT you should NOT include the @ if you're not providing an author.
E.g., if you're adding the quote "To be, or not to be", but don't want to include the author, you'd send the following command:
```
socket.send_string("add To be, or not to be")
```
and if you do want to include the author, you'd send the following command:
```
socket.send_string("add To be, or not to be @ Shakespeare")
```
If an error occurred due to the command containing more than one @ (such as if the quote itself contained an @), the server will send back the string "Error. multiple @ symobls in request: REQUEST_STRING", and the quote will not be added.
