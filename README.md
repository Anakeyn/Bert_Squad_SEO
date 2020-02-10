# Bert_Squad_SEO

This tool provide a "Bert Score" for the first 30 pages responding to a question in Google

This tool is using  Bert-SQuAD created by Kamal Raj. 

We modified the "get_answer" function in order to calculate a "Bert Score"  (in utils.py file)
regarding several documents and not a score inside a unique document (softmax score).
see original BERT-SQuAD : https://github.com/kamalkraj/BERT-SQuAD

We also modify the "QA" class in bert.py file in order to use "official" pre trained fine tuned for SQuAD models from Hugging Face (see below)

# What is BERT?

Bidirectional Encoder Representations from Transformers (BERT) is a technique for NLP (Natural Language Processing) pre-training developed by Google

# What is SQuAD?

Stanford Question Answering Dataset (SQuAD) is a reading comprehension dataset, consisting of questions posed by crowdworkers on a set of Wikipedia articles, where the answer to every question is a segment of text, or span, from the corresponding reading passage, or the question might be unanswerable.

See more information about SQuAD :  https://rajpurkar.github.io/SQuAD-explorer/

# Pretrained Model for Q&A tasks

You can find pre trained model fine tuned on SQuAD on the official list from Hugging Face
https://huggingface.co/transformers/pretrained_models.html 

At that time we found two available models (in English only) :
* 'bert-large-uncased-whole-word-masking-finetuned-squad'
* 'bert-large-cased-whole-word-masking-finetuned-squad'

As we modify the QA class written by Kamal Raj, You need to give directly the name of a pretrained model (not a directory on your computer) and a size for the n best values desired :
```
n_best_size = 20
model = QA('bert-large-uncased-whole-word-masking-finetuned-squad', n_best_size) 
```


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

We create a Jupyter Notebook in order to run it in Google Colab.  Google Colab may be more fast to run it on its environment than on your computer. Don't forget to select Python3 and GPU in  the notebook parameters.

You will need to "mount" you Google Drive in Google Colab in order to save results files.

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

# More 
Post (in french) about this tool : https://www.anakeyn.com/2019/12/18/score-bert-referencement-seo/
Post (in English) about this tool : https://www.jcchouinard.com/get-bert-score-for-seo-by-pierre-rouarch/  (Thanks to Jean-Christophe Chouinard)












