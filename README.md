# Text Classification on Twitter data scraped using the Tweepy API
NLP on Twitter Data

## Introduction
This research sets out to implement machine learning text classification algorithms to identify those Twitter users who have bipolar disorder. The text classification problem is concerned with a single label compared to numerous other experiments that attempt to group specific diseases together based on similar symptomatology and context derived from a corpus. The healthcare term for two or more diseases that are present in an individual is referred to as comorbidity. Since bipolar disorder is often associated with clinical depression and manic episodes, cases of bipolar disorder are often linked with major depressive disorders. This further complicates the process of the text classification problem. The research team implements a NLP pipeline and then downstream text classification models to identify whether or not a Twitter user has been diagnosed with bipolar disorder.  

## Research Questions/Objectives
Will analyzing natural language across a tweet provide reliable insight to the factors contributing to the onset of BP? 

How reliable can identifying causal relationships in tweets related to BP be in classifying an individual as having BP or not? Or is the criteria by which we classify an individual as having BP or not limited to an official diagnosis by a psychiatrist?

We provide a multi-part NLP component technique across multiple sentences to identify bipolar disorder-causality using a corpus of twitter data. We also implement machine learning classification models to perform single-label text classification. This work shines light on the utility of examining short-text written by a diverse community of users who share first-hand accounts and documentation of their experiences with bipolar disorder.

## Results/Further work
With respect to the AUC and F-beta scores, the Logistic regression model performed the best out of all models tested. Our methodology provides a guideline to a system that can be used to aid medical practitioners in their diagnoses of bipolar disorder. The biggest drawback would be the amount of improper classifications made by the model, although low. With better hardware and more data to work with, it would be possible to train the model to achieve better accuracy and predicting capabilities. This system should not be used to solely diagnose a patient as the diagnosis should not be only based on model predictions. This is due to the fact that there is no actual medical information on the disorder to cross-check with. Rather, it should be used as a tool by the practitioner for aid in diagnosis. 
An important thing to note is the removal of negation words during stopword removal. Words like ‘no’, ‘not’ are vital in our case and their removal results in the loss of important information regarding the content of the text. The use of a custom corpus or list of stopwords would be something to look into for improving this project in the future. 
