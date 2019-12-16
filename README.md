# Bert_Squad_SEO
This tool provide a "Bert Score" for first max 30 pages responding to a question in Google

This tool is using  Bert-SQuAD created by Kamal Raj. We modified  it to calculate a "Bert Score"
regarding several documents and not a score inside a unique document (softmax score).
see original BERT-SQuAD : https://github.com/kamalkraj/BERT-SQuAD

# What is BERT?

Bidirectional Encoder Representations from Transformers (BERT) is a technique for NLP (Natural Language Processing) pre-training developed by Google

# What is SQuAD?

Stanford Question Answering Dataset (SQuAD) is a reading comprehension dataset, consisting of questions posed by crowdworkers on a set of Wikipedia articles, where the answer to every question is a segment of text, or span, from the corresponding reading passage, or the question might be unanswerable.

See more information about SQuAD :  https://rajpurkar.github.io/SQuAD-explorer/

# Pretrained Model for Q&A tasks

In order to use this tool you need to download a BERT pretrained model fine tuned for Question and Answers tasks.  Kamal created one and you can download [here](https://www.dropbox.com/s/8jnulb2l4v7ikir/model.zip). 

NB : This file is too big to be upload on Github.

After installing this repository on your computer,  unzip and move files to "model" directory

# Requirements

* Python 3 or Anaconda 3.6 or 3.7
* pip3 (or pip) install -r requirements.txt

# Run Bert_Squad_SEO_Score.py on your computer 

Beware !!! The process is very long so we advice you to run it in an IDE (for example Spyder) 
Define your question at the begining of the program :
myKeyword="When Abraham Lincoln died"

* The system will scrap Google to get the first 30 pages answering to the question, 
* Next scraping the content of each page
* And for each page calculate a score for the 20 bests responses - The Bert Score for a page is the mean of these 20 scores.

# Run Bert_Squad_SEO_Score_Colab.py in [Google Colab](https://colab.research.google.com)

We create a Jupyter Notebook in order to run it in Google Colab.  Google Colab may be more fast to run it on his environment than on your computer. Don't forget to select Python3 and GPU in  the notebook parameters.

You need to upload this Github files in your Gogole Drive first.  Next you will need to "mount" you Gogole Drive in Google Colab in order to access the model and to save results files.

# Predict Results

When you ask for a prediction (for example)
answer = model.predict( dfPagesUnique.loc[i, 'body'],myKeyword)

answer is a dictionary that contents :
* "answers" : 20 responses texts from  the document
* "starts" : 20 Start indexes of responses in doc_tokens
* "ends" : 20 end  indexes of responses in doc_tokens
* "doc_tokens" : document tokens
* "local_probs" : 20 best local probs (old indicators or results after softmax)
* "total_scores" :20 best scores (not softmaxed)
* "total_probs" : 20 best probs  (not softmaxed)
* "mean_total_prob" : mean on 20 best probs : our new bert score indicator !!!














