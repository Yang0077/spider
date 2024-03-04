from textblob import TextBlob


def analyze_sentiment(comment):
    blob = TextBlob(comment)
    return blob.sentiment.polarity, blob.sentiment.subjectivity
