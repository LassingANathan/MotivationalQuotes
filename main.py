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
                # Create and send quote
                quote = quoteRetriever.retrieveRandomQuote()
                sendQuote(quote, socket)

    # Make a clean exit
    context.destroy()

# Sends a quote on the given socket
def sendQuote(quote: tuple, socket) -> None:
    if quote[1] == None:
        socket.send_string(quote[0])
    else:
        socket.send_string(quote[0] + " - " + quote[1])

main()