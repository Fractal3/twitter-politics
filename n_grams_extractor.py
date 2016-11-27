import sklearn.feature_extraction.text as fet
# from sklearn.model_selection import train_test_split
# from sklearn.model_selection import KFold
# from sklearn.naive_bayes import MultinomialNB
# from sklearn.metrics import classification_report, f1_score, accuracy_score, precision_score, recall_score
# from sklearn.svm import LinearSVC
# from sklearn.linear_model import SGDClassifier
# from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
# from sklearn.linear_model import RidgeClassifier

import numpy as np
from time import time


def isRT(word):
    word = word.strip().lower()
    return "@" in word or "rt" in word or "www." in word or "http" in word or word == ""


def load_data(username):
    x_data = []
    with open("data/tweets_{}.csv".format(username), 'r') as data_file:
        string_doc = x_data
        for line in data_file.readlines():
            new_line = " ".join([x.strip().lower() for x in line.split() if not isRT(x)])
            string_doc.append(new_line)
    data_file.close()
    return x_data


def extract_n_grams(X_train, username, save_ngrams=False):
    output_path = "results/best_ngrams_{}.tsv".format(username)
    vect = fet.CountVectorizer(ngram_range=(1, 3), analyzer="word", min_df=0, stop_words='english')
    term_doc_mat = vect.fit_transform(X_train)
    term_doc_mat_summed = term_doc_mat.sum(axis=0)
    scores_array = np.array(term_doc_mat_summed)
    sorted_scores = (-scores_array).argsort().flatten()[:5000]
    if save_ngrams:
        save_to_file(vect, term_doc_mat_summed, output_path, sorted_scores)
    trainx = term_doc_mat[:, sorted_scores]
    # testx = vect.transform(x)[:, sorted_scores]
    return trainx, vect, sorted_scores

def save_to_file(vect, term_doc_mat, output_path, sorted_scores):
    features = vect.get_feature_names()#[:, sorted_scores]
    print(type(term_doc_mat))
    word_scores = term_doc_mat.A1 #[:, sorted_scores]
    with open(output_path, "w") as output_file:
        output_file.write("word\tcount\n")
        for l in sorted_scores:
            towrite = str(features[l]) + "\t" + str(word_scores[l]) + "\n"
            output_file.write(towrite)
    output_file.close()



if __name__ == "__main__":



# def train_validate_phase(classifiers, X_train, Y_train, report_file):
#     best_classifiers = []
#
#     for classif_name in classifiers:
#         print(classif_name)
#         best_accuracy = 0
#         best_f1_score = 0
#         best_classifier = None
#         kfold = KFold(n_splits=5)
#         kfold.get_n_splits(X_train, Y_train)
#         chunks = kfold.split(X_train, Y_train)
#         accuracyscore = 0
#         precision = 0
#         recall = 0
#         f1score = 0
#         for train_index, test_index in chunks:
#             clf = classifier_factory(classif_name)
#             train_x_chunk = X_train[train_index, :]
#             test_x_chunk = X_train[test_index, :]
#             train_y_chunk = [Y_train[i] for i in train_index]
#             test_y_chunk = [Y_train[i] for i in test_index]
#             begin_time = time()
#             clf.fit(train_x_chunk, train_y_chunk)
#             end_time = time()-begin_time
#             report_file.write("clf {0} learning time : {1} \n".format(classif_name, end_time))
#             print("clf {0} learning time : {1}".format(classif_name, end_time))
#             begin_time = time()
#             prediction = clf.predict(test_x_chunk)
#             end_time = time()-begin_time
#             print("clf {0} validation time : {1}\n".format(classif_name, end_time))
#             report_file.write("clf {0} validation time : {1}\n".format(classif_name, end_time))
#             accuracy = accuracy_score(test_y_chunk, prediction)
#             print("mean accuracy : {}\n".format(accuracy))
#             report_file.write("clf {0} mean accuracy: {1}\n".format(classif_name, accuracy))
#             report = classification_report(test_y_chunk, prediction, digits=4)
#             report_file.write(report)
#             accuracyscore += accuracy
#             precision += precision_score(test_y_chunk, prediction)
#             recall += recall_score(test_y_chunk, prediction)
#             clf_f1_score = f1_score(test_y_chunk, prediction)
#             f1score += clf_f1_score
#             if best_f1_score < clf_f1_score:
#                 best_classifier = clf
#                 best_accuracy = accuracy
#             elif best_f1_score == f1_score(test_y_chunk, prediction):
#                 if best_accuracy < accuracy:
#                     best_classifier = clf
#                     best_accuracy = accuracy
#         accuracyscore /= 5.0
#         precision /= 5.0
#         recall /= 5.0
#         f1score /= 5.0
#         report_file.write(str(accuracyscore)+", "+str(precision)+", "+str(recall)+", "+str(f1score)+"\n")
#         best_classifiers.append(best_classifier)
#     return best_classifiers
#
#
# def classifier_factory(name):
#     return {
#         "MultinomialNB": MultinomialNB(),
#         "LinearSVC": LinearSVC(loss='squared_hinge', penalty='l2', dual=False, tol=1e-3),
#         "SGDClassifier": SGDClassifier(),
#         "RidgeClassifier": RidgeClassifier(),
#         "AdaBoostClassifier": AdaBoostClassifier(n_estimators=5),
#         "RandomForestClassifier": RandomForestClassifier(n_estimators=4, criterion='gini', min_samples_split=2)
#     }.get(name)
#
#
# def classify_data(save_ngrams=False):
#     t0 = time()
#     X_train, X_test, Y_train, Y_test = load_data("data/pos_examples_PosSentiment.txt",
#                                                  "data/neg_examples_NegSentiment.txt")
#
#     X_train, X_test, vect, sorted_scores = extract_n_grams(X_train, X_test, save_ngrams=save_ngrams)
#     print("preprocessing time : {}".format(time() - t0))
#     classifiers_name = [
#         'LinearSVC',
#         'SGDClassifier',
#         'MultinomialNB',
#         #'RandomForestClassifier'
#         #'AdaBoostClassifier',
#         'RidgeClassifier'
#     ]
#     with open("results/classification_report_sentiment.txt", 'w') as report_file:
#         best_classifiers = train_validate_phase(classifiers_name, X_train, Y_train, report_file)
#         print(len(best_classifiers))
#
#         for bc in best_classifiers:
#             begin_time = time()
#             prediction = bc.predict(X_test)
#             end_time = time() - begin_time
#             print("best clf {0} testing time : {1}\n".format(bc, end_time))
#             report_file.write("clf {0} testing time : {1}\n".format(bc, end_time))
#             accuracy = accuracy_score(Y_test, prediction)
#             print("mean accuracy : {}\n".format(accuracy))
#             report_file.write("best clf {0} mean accuracy: {1}\n".format(bc, accuracy))
#             report = classification_report(Y_test, prediction, digits=4)
#             report_file.write(report)
#     report_file.close()
#
#     testing_set = load_data("data/pos_examples_happy.txt",
#                             "data/neg_examples_sad.txt", split=False)
#     X_test_emo = vect.transform(testing_set[0])[:, sorted_scores]
#     Y_test_emo = testing_set[2]
#     with open("results/classification_report_emotional.txt", 'w') as report_file:
#         print(len(best_classifiers))
#         for bc in best_classifiers:
#             begin_time = time()
#             prediction = bc.predict(X_test_emo)
#             end_time = time() - begin_time
#             print("best clf {0} testing time : {1}\n".format(bc, end_time))
#             report_file.write("clf {0} testing time : {1}\n".format(bc, end_time))
#             accuracy = accuracy_score(Y_test_emo, prediction)
#             print("mean accuracy : {}\n".format(accuracy))
#             report_file.write("best clf {0} mean accuracy: {1}\n".format(bc, accuracy))
#             report = classification_report(Y_test_emo, prediction, digits=4)
#             report_file.write(report)
#     report_file.close()
#
