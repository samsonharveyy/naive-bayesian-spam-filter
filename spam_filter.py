# THIS SCRIPT IS DEVELOPED AND IMPLEMENTED IN PYCHARM
""" PYTHON CODE IMPLEMENTATION OF A SPAM FILTER USING BAYES' THEOREM """

import os
import math
from collections import Counter
from nltk.corpus import stopwords
import re
import time


start = time.time()

# load stopwords, use nltk.download('stopwords') if non-existent prior to running the program
mystopwords = stopwords.words('english')
# common words that (possibly) will not tell significantly the email classification

""" Open labels and classify as SPAM or HAM, and TRAINING set data or TESTING set data """
lbel = open('labels', 'r').read()
all_labels = lbel.split('\n')
train_set_data = all_labels[0:21300]
test_set_data = all_labels[21300:37822]



""" SPAM FILTER: TRAINING PHASE """


""" read contents of each train set email and store to spam list if spam, otherwise ham list """
spam_list = []
ham_list = []
ham_email_count = 0
spam_email_count = 0

for tag in train_set_data:
    sep = tag.split(' ') #separate by whitespace
    code, file = sep
    file = file.strip('../') #strip such characters from the filename

    dirs = os.path.dirname((os.path.realpath('__file__'))) #access to file pathname
    file_dir = os.path.join(dirs, file)
    bypass = "" #where all the read contents go

    with open(file_dir, 'r', encoding='utf-8', errors='ignore') as mail:
        inbody = False
        for every_line in mail:
            if inbody:
                bypass += every_line
            elif every_line == '\n':
                # reading starts after first occurrence of blank line in the email
                inbody = True
        bypass = re.findall('\w+', bypass) #find all alphanumeric characters in lowercase, splits punctuations
        bypass = [x.strip() for x in bypass if x.strip()] #removes unwanted empty 'lines' or strings

    if code == "ham":
        filterer = []
        for k in bypass:
            k = k.lower()
            if not k in mystopwords and k.isalpha():
                if not k in filterer: # makes the filterer a list of only unique words
                    filterer.append(k)
        for term in filterer:
            ham_list.append(term)
        ham_email_count = ham_email_count + 1 # adds 1 to total count of ham emails read

    elif code == "spam":
        filterer = []
        for k in bypass:
            k = k.lower()
            if not k in mystopwords and k.isalpha():
                if not k in filterer:
                    filterer.append(k)
        for term in filterer:
            spam_list.append(term)
        spam_email_count = spam_email_count + 1 # adds 1 to total count of spam emails read

""" Gets top 5000 words, total count, spam occurences and ham occurences """
combined_list = spam_list + ham_list
combined_list = Counter(combined_list)
combined_list = combined_list.most_common(5000)

spamwords_count = []
hamwords_count = []
for pair in combined_list:
    w = pair[0]
    spamwords_count.append(spam_list.count(w)) #appends every spam email occurrence of the top 5000 words according to order
    hamwords_count.append(ham_list.count(w))   #appends every ham email occurrence of the top 5000 words according to order


""" Stores data count to .txt file """
final_list = list(zip((x for x in combined_list), spamwords_count, hamwords_count))
with open('occurences.txt', 'w', encoding='utf-8') as occ:
    occ.write("Top 5000 words, Total Occurences, Spam Occurences, Ham Occurences")
    occ.write('\n')
    occ.write('\n')
    occ.write('\n'.join('{} {} {}'.format(x[0],x[1], x[2]) for x in final_list))

""" COMPUTING DATA PROBABILITIES """
spam_prior_prob = spam_email_count / (spam_email_count + ham_email_count)
ham_prior_prob = ham_email_count / (spam_email_count + ham_email_count)

# PREDEFINED VALUES:
lam = float(input("Enter a lambda (float) value: "))
# 1 is default value. 0.05, 0.1, 0.5 and 2 are appropriate lambda values as well
v = 5000

#Laplacian setting lists
spam_laplist = []
ham_laplist = []
for sp in spamwords_count:
    spam_laplacian = (sp + lam) / (spam_email_count + v*lam)
    spam_laplist.append(spam_laplacian)
for hm in hamwords_count:
    ham_laplacian = (hm + lam) / (ham_email_count + v*lam)
    ham_laplist.append(ham_laplacian)

#store calculated probabilities to another .txt file
with open('probs.txt', 'w', encoding='utf-8') as p:
    p.write("Prior probability of spam emails: ")
    p.write(str(spam_prior_prob))
    p.write('\n')
    p.write("Prior probability of ham emails: ")
    p.write(str(ham_prior_prob))
    p.write('\n')
    p.write('\n')
    p.write('P given Spam of Top Words:')
    p.write('\n')
    p.write(str(spam_laplist))
    p.write('\n')
    p.write('\n')
    p.write('P given Ham of Top Words:')
    p.write('\n')
    p.write(str(ham_laplist))




""" SPAM FILTER: TESTING PHASE """

# zip a list with words, its count in spam emails, and its count in ham emails
words_only = []
for tandem in combined_list:
    single_word = tandem[0]
    words_only.append(single_word)
probs = list(zip(words_only, spamwords_count, hamwords_count))

true_positive = 0
true_negative = 0
false_negative = 0
false_positive = 0
test_extra_list = []
is_classified = []
classification = [] #merged list of test_extra_list and is_classified

# almost same method as training set data retrieval
for test in test_set_data:
    sep = test.split(' ')
    code, file = sep
    if code == 'ham':
        spamtruth = False
        hamtruth = True
    elif code == 'spam':
        spamtruth = True
        hamtruth = False

    file = file.strip('../')
    test_extra_list.append((file, code)) #for quick retrieval of data in storing to last .txt file

    dirs = os.path.dirname((os.path.realpath('__file__')))
    file_dir = os.path.join(dirs, file)
    bypass = ""
    with open(file_dir, 'r', encoding='utf-8', errors='ignore') as mail:
        inbody = False
        for every_line in mail:
            if inbody:
                bypass += every_line
            elif every_line == '\n': #reading starts after occurrence of first blank line
                inbody = True

    bypass = re.findall('\w+', bypass)  # remove/split symbols from characters
    bypass = [x.strip() for x in bypass if x.strip()] #removes unwanted empty 'lines' or strings
    filterer = []

    for k in bypass:
        k = k.lower()
        if not k in mystopwords and k.isalpha():
            if not k in filterer:
                filterer.append(k)


    total_ham = 0
    total_spam = 0

    for i in probs:
        word = i[0]
        count_spam = i[1]
        count_ham = i[2]

        if word in filterer:
            total_spam += math.log((count_spam + lam) / (spam_email_count + (v*lam)))
            total_ham += math.log((count_ham + lam) / (ham_email_count + (v*lam)))
        else:
            total_spam += math.log((1 - ((count_spam + lam) / (spam_email_count + (v*lam)))))
            total_ham += math.log((1 - ((count_ham + lam) / (ham_email_count + (v*lam)))))


    if total_spam > total_ham:
        is_classified.append('spam')
        spamyes = True
        if spamyes == spamtruth:
            true_positive += 1
        else:
            false_positive += 1

    elif total_ham > total_spam:
        is_classified.append('ham')
        hamyes = True
        if hamyes == hamtruth:
            true_negative += 1
        else:
            false_negative += 1


    classification = list(zip(test_extra_list, is_classified))

""" Store classified data in a .txt file """
with open('classification.txt', 'w', encoding='utf-8') as clas:
    clas.write("Data/Folder/File, TRUE label, CLASSIFIED label")
    clas.write('\n')
    clas.write('\n'.join('{} {}'.format(x[0], x[1]) for x in classification))


    P = true_positive / (true_positive + false_positive)
    R = true_positive / (true_positive + false_negative)

""" SPOT CHECK """
print("Precision: ", P)
print("Recall: ", R)

end = time.time()
print("Program runtime (in seconds): ", end - start)


# CALCULATED VALUES:
# for lam = 1: Precision:  0.944583413507793  Recall: 0.8817242927705433
# for lam = 0.05: Precision: 0.9558766859344894  Recall: 0.8910642119443197
# for lam = 0.1: Precision:  0.9544666923373123  Recall: 0.8904355635383925
# for lam = 0.5: Precision:  0.9489291598023064  Recall: 0.8793893129770992
# for lam = 2: Precision:  0.9373117469879518  Recall: 0.8942972608890885
