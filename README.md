# naive-bayesian-spam-filter

Spam Filtering is a problem that may be modeled as a two-category classification problem. The first category represents
legitimate messages or Ham, and the other category represents junk e-mail also known as Spam. This program classifies emails into these two categories using Conditional Probability and and Naive Bayes' Theorem.

The program has Training phase and Testing phase. In the Training phase, your goal is to provide pre-classified e-mails to your program so that it can use the information extracted from those e-mails as a basis for computing the probability of an e-mail being classified as legitimate or unsolicited. You will classify e-mails as Spam of Ham solely based on the frequency of words in Spam or Ham e-mails. Once your program has been trained with pre-classified information, you can then input actual e-mail content into your program and classify them as Ham or Spam using the results from the Training phase. However, to test the performance of your Spam Filter, you will feed a second set of pre-classified e-mails to your program to check how well it classifies e-mails. You are to assess the performance of your Spam Filter quantitatively using the Precision and Recall metrics.

A .zip file containing all the emails will be provided, namely trec06p-eee111.zip, which came from the website: https://plg.uwaterloo.ca/∼gvcormac/treccorpus06/about.html. Upon extraction, you will see two files and one folder. The first file, named "labels" contains the true classification of all the email files in the set. The second file, named "README.rtl" just tells you that the relevant emails that you will use for the Training phase in the "data" folder are the content of folders 0 to 70, and the dataset for the Testing phase are in folders 71 onwards. Finally, the "data" folder holds all the email files grouped into many folders as stated in the README.rtl file. Note that each folder has 300 emails with a standard naming convention.

For simplicity, the following are considered:
- You will ignore e-mail contents that do not use ASCII or UTF-8 encoding as we are building a Spam Filter suited for those who use English as their primary language.
- Attached images, video and other files are also ignored.
- A word is defined as any string with only alphabetical characters. Each word is separated by a whitespace (spaces, tabs, newlines, and similar characters) in front of the word (or nothing if it is the first word), and by whitespace or a single symbol of any kind (periods, commas, and similar symbols). For example, “Hello”, “ XDXB! ”, and “NBSP&” are words, but “Hello...”, “spicy_gil123”, or similar constructs are not. Additionally, treat every word having the same case (Apple, APple, apple and APPLE are all the same).
- Lambda Smoothing is introduced in the filtering process. The value of λ may be defined by the Software Developer, but for the purpose of this project, the set value will be 1. Setting the value of λ to 1 changes the name of this approach from “Lambda Smoothing” to “Laplacian Smoothing” since setting it to 1 is a special case. Modifying the numerator entails that the probability computation will change, and we do not want the computation to be far off from the original computation. Thus, we add a factor V · λ to the denominator to reduce the impact of adding λ to the numerator. The value of V is the size of the test vocabulary that we have. In the case of this project, the set value of V is 5000.

In assessing the performance of the spam filter, precision and recall is introduced. 
- Precision = TP / TP + FP
- Recall = TP / TP + FN
- TP is defined as the number of spam e-mails classified as spam. TN is defined as the number of ham
e-mails classified as ham. FP is defined as the number of ham e-mails classified as spam. FN is defined as
the number of spam e-mails classified as ham.
