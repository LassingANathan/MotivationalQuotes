from QuoteRetriever import QuoteRetriever
import zmq
import time

def main():
    context = zmq.Context()
    
    # Create quoteRetriever
    quoteRetriever = QuoteRetriever("storedQuotes.txt")
    
    # Create reply socket
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")
    
    while True:
        # Receive message
        message = socket.recv()
        
        # Ensure message isn't empty
        if len(message) > 0:
            # Decode and split message
            decodedMessage = message.decode()
            splitMessage = decodedMessage.split()
            
            if splitMessage[0] == 'Q': # Client asked server to quit
                break
            elif splitMessage[0] == "quote": # Client asked server to give a quote
                # Options: 
                # -f: only from favorites
                # -nf: don't include favorites
                if len(splitMessage) == 0:
                    # Retrieve and send quote
                    quote = quoteRetriever.retrieveRandomQuote()
                    sendQuote(quote, socket)
                elif len(splitMessage) == 1:
                    if splitMessage[1] == "-f":
                        # Retrieve and send favorite quote
                        quote = quoteRetriever.retrieveRandomFavoriteQuote()
                        sendQuote(quote, socket)
                    elif splitMessage[1] == "-nf":
                        # Retrieve and send non-favorite quote
                        quote = quoteRetriever.retrieveRandomQuote(False)
                        sendQuote(quote, socket)
                    else:
                        socket.send_string("Error, unknown argument passed: " + splitMessage[1])
                else:
                    # Get entire command into one string
                    errorString = ""
                    for s in splitMessage:
                        errorString.append(s)
                        
                    socket.send_string("Error, multiple arguments passed in request: " + errorString) 
            elif splitMessage[0] == "fav": # Client asked server to favorite the last quote
                pass
            elif splitMessage[0] == "del": # Client asked server to delete the last quote
                pass
            elif splitMessage[0] == "add": # Client asked server to add a quote to the list
                pass

    # Make a clean exit
    context.destroy()

# Sends a quote on the given socket
def sendQuote(quote: tuple, socket) -> None:
    if quote[1] == None:
        socket.send_string(quote[0])
    else:
        socket.send_string(quote[0] + " - " + quote[1])

main()