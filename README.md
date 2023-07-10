# tweets-sentiment-analysis
Using NLP and ML for identifying abusive speech for Twitter users in Indonesia

# Problem Statement:
Twitter is the biggest platform where anybody and everybody can have their views heard. Some of these voices spread hate and negativity. Twitter is wary of its platform being used as a medium to spread hate.
by using NLP techniques, performing specific cleanup for tweets data, and making a robust model.

# Analysis to be done:

Clean up tweets and build a classification model by using NLP techniques, cleanup specific for tweets data already be done by using SWAGGER UI,
However, visualization and prediction still be needed by using Machine Learning and trying to get the best model.

# About the dataset
dataset for multi-label hate speech and abusive language detection in the Indonesian Twitter.

The main dataset can be seen at **re_dataset** with labels information as follows:
* **HS** : hate speech label;
* **Abusive** : abusive language label;
* **HS_Individual** : hate speech targeted to an individual;
* **HS_Group** : hate speech targeted to a group;
* **HS_Religion** : hate speech related to religion/creed;
* **HS_Race** : hate speech related to race/ethnicity;
* **HS_Physical** : hate speech related to physical/disability;
* **HS_Gender** : hate speech related to gender/sexual orientation;
* **HS_Gender** : hate related to other invective/slander;
* **HS_Weak** : weak hate speech;
* **HS_Moderate** : moderate hate speech;
* **HS_Strong** : strong hate speech.

For each label, `1` means `yes` (tweets including that label), `0` mean `no` (tweets are not included in that label).
