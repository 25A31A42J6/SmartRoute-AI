# SmartRoute AI — BANKING77 EDA
import os,re
import pandas as pd
import matplotlib.pyplot as plt
from collections import Counter

DATA_DIR='../data'
train=pd.read_csv(os.path.join(DATA_DIR,'banking77_train.csv'))
test=pd.read_csv(os.path.join(DATA_DIR,'banking77_test.csv'))
print('Train shape:',train.shape,'Test shape:',test.shape)
print('\nDtypes:\n',train.dtypes)
print('\nMissing values:\n',train.isna().sum())
print('\nDuplicate rows:',train.duplicated().sum(),test.duplicated().sum())
train['text_length_chars']=train.text.astype(str).str.len()
train['word_count']=train.text.astype(str).str.split().str.len()
print('\nLength stats:\n',train[['text_length_chars','word_count']].describe())
print('\nUnique labels:',train.label.nunique())
print('\nClass distribution:\n',train.label.value_counts())
plt.figure(figsize=(12,18)); train.label.value_counts().sort_values().plot(kind='barh'); plt.title('BANKING77 Training Intent Distribution'); plt.tight_layout(); plt.show()
plt.figure(figsize=(10,5)); plt.hist(train.word_count,bins=35); plt.title('Query Word Count Distribution'); plt.tight_layout(); plt.show()
train_labels=set(train.label.unique()); test_labels=set(test.label.unique())
print('\nLabels missing from test:',sorted(train_labels-test_labels))
print('Labels missing from train:',sorted(test_labels-train_labels))
overlap=set(train.text.astype(str)).intersection(set(test.text.astype(str)))
print('Exact train/test text overlap:',len(overlap))
tokens=[]
for t in train.text.astype(str): tokens += re.findall(r'[a-zA-Z]+',t.lower())
stop={'the','a','an','and','or','to','of','is','i','my','it','in','for','on','me','this','that','do','does','can','how','what','why','was','be','have','has','with','are','am','please','there','you'}
print('\nTop words:',Counter(w for w in tokens if w not in stop and len(w)>2).most_common(25))
