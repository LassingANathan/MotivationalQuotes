import random

class QuoteRetriever():
    def __init__(self, storedQuotesFilePath):
        self.filePath = storedQuotesFilePath
        self.authorDelimiter = "@"
        
        self.lastSentQuote = (None, None)
        
    # Retrieve a random quote from the list
    # param:includeFavorites is a boolean for whether the favorite quotes should be included in this search
    # returns: a tuple with the quote as the first element and the author as the second element, or None as the second element if no author was included
    def retrieveRandomQuote(self, includeFavorites=False) -> tuple:
        with open(self.filePath, 'r') as f:
            # Read file
            lines = f.readlines()
            favoriteQuotes = [] # Parallel arrays for storing a quote's CONTENT
            favoriteQuoteAuthors = [] # Parallel arrays for storing a quote's AUTHOR (or None)
            
            # Get all quotes that aren't favorites
            for line in lines:
                if line.strip() == "FAVORITES": # We've reached the favorites
                    if not includeFavorites: # If we don't include favorites, stop reading quotes
                        break
                    else: # If we DO include favorites, then go to the next line and proceed to add all the favorites
                        continue
                    
                else:
                    # Split line to separate author
                    quoteParts = line.split(self.authorDelimiter)
                    
                    # Determine if the quote had an author
                    if (len(quoteParts) == 1): # No author
                        favoriteQuotes.append(quoteParts[0].strip())
                        favoriteQuoteAuthors.append(None)
                    elif (len(quoteParts) == 2): # Quote had an author
                        favoriteQuotes.append(quoteParts[0].strip())
                        favoriteQuoteAuthors.append(quoteParts[1].strip())
                    else: # A quote likely had an @ symbol in it, and everything is ruined
                        favoriteQuotes.append(None)
                        favoriteQuotes.append(None)             

            
            # Generate a quote until one works
            while True:
                randQuoteIndex = random.randint(0, len(favoriteQuotes) - 1)
                
                quoteContent = favoriteQuotes[randQuoteIndex]
                
                # Pick another quote if this quote's content is None, it means something is messed up with it
                if quoteContent == None:
                    continue
                
                quoteAuthor = favoriteQuoteAuthors[randQuoteIndex]
                
                # Return the tuple described at function header
                self.lastSentQuote = (quoteContent, quoteAuthor)
                return (quoteContent, quoteAuthor)
    
    # Retrieve a random quote from the favorites list
    # returns: a tuple with the quote as the first element and the author as the second element, or None as the second element if no author was included
    def retrieveRandomFavoriteQuote(self) -> tuple:
        with open(self.filePath, 'r') as f:
            # Read file
            lines = f.readlines()
            
            inFavorites = False
            favoriteQuotes = [] # Parallel arrays for storing a quote's CONTENT
            favoriteQuoteAuthors = [] # Parallel arrays for storing a quote's AUTHOR (or None)
            
            # Skip all lines that aren't before the "FAVORITES" line
            for line in lines:
                if not inFavorites:
                    if line.strip() == "FAVORITES":
                        inFavorites = True
                        continue
                else: # In favorites list at this point
                    # Split line to separate author
                    quoteParts = line.split(self.authorDelimiter)
                    
                    # Determine if the quote had an author
                    if (len(quoteParts) == 1): # No author
                        favoriteQuotes.append(quoteParts[0].strip())
                        favoriteQuoteAuthors.append(None)
                    elif (len(quoteParts) == 2): # Quote had an author
                        favoriteQuotes.append(quoteParts[0].strip())
                        favoriteQuoteAuthors.append(quoteParts[1].strip())
                    else: # A quote likely had an @ symbol in it, and everything is ruined
                        favoriteQuotes.append(None)
                        favoriteQuotes.append(None)
                        
        # Generate a quote until one works
        while True:
            randQuoteIndex = random.randint(0, len(favoriteQuotes) - 1)
            
            quoteContent = favoriteQuotes[randQuoteIndex]
            
            # Pick another quote if this quote's content is None, it means something is messed up with it
            if quoteContent == None:
                continue
            
            quoteAuthor = favoriteQuoteAuthors[randQuoteIndex]
            
            # Return the tuple described at function header
            self.lastSentQuote = (quoteContent, quoteAuthor)
            return (quoteContent, quoteAuthor)
        
    # Adds the most recently sent quote to the Favorite list
    # returns: False if the quote couldn't be added, and True otherwise
    def addLastSentQuoteToFavorites(self) -> bool:
        # Return false if a quote hasn't yet been sent
        if self.lastSentQuote == (None, None):
            return False
        with open(self.filePath, 'a') as f:
            f.write(self.lastSentQuote[0] + " @ " + self.lastSentQuote[1])
            return True