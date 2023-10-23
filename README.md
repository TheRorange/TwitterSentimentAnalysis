# TwitterSentimentAnalysis
## EDA
The dataset consists of 61.2% negative, 22.7% neutral, and 16.1% positive tweets. So, it is expected to have a bias toward negative results. 
## Cleaning
Some tweets consist of the string "RT" which stands for "retweet", so, it should be removed. Moreover, links and quotation marks should be removed as well.
## Tokenizing
For better analysis, tokenizer was used to vectorize and convert text into Sequences so the Network can deal with it as input.
## Training
LSTM network was used because it has feedback connections. Hence, it has a short-term memory, which helps to have acceptable results. 
## Accuracy
The accuracy on training and validation is 97.3% and 83.1% respectively.
## Data Extraction using Tweepy
A specific text can be given to extract tweets that include that and classify them using the model.
## Web Application
The model was saved and used in a web application. The application works in a way that the user inputs a sentence and the app outputs the sentiment.
## Future Work
Sometimes quotation marks have different meanings in different situations. So, it's also good to consider them in some situations.
