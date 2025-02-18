from QuoteRetriever import QuoteRetriever

quoteRetriever: QuoteRetriever = QuoteRetriever("storedQuotes.txt")
print(quoteRetriever.retrieveRandomQuote())
print(quoteRetriever.addLastSentQuoteToFavorites())