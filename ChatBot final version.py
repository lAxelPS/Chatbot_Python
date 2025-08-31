import os


def list_of_files(directory, extension):
    # Initialize an empty list to store file names
    files_names = []
    # Browse through the list of files in the given directory
    for filename in os.listdir(directory):
        # Check if the file has the given extension
        if filename.endswith(extension):
            # Append the file name to the list
            files_names.append(filename)
    # Return the list of file names
    return files_names


def extract_name(directory, extension):  # Extract the names of the presidents from the names of the text files provided
    # Initialize an empty list to store president names
    list_names = []
    # Iterate through files in the given directory with the given extension
    for filename in list_of_files(directory, extension):
        # Split the filename by discarding the "Nomination_" part
        file_parts = filename.split("_")
        # Check if there are at least two parts
        if len(file_parts) >= 2:
            # Extract the name by discarding the ".txt" part
            name = file_parts[1].split(".")[0]
            # Remove the last character if it is a digit
            if name[-1] in '12':
                name = name[:-1]
            # Append the cleaned name to the list
            list_names.append(name)
    # Remove duplicates
    list_names = list(set(list_names))
    return list_names


list_names = extract_name("speeches", "txt")


def first_names():  # Associate to each president their first name
    # Define a dictionary mapping last names to first names
    list_firstnames = {"Chirac": "Jacques", "Giscard dEstaing": "Valéry", "Hollande": "François", "Macron": "Emmanuel",
                       "Mitterrand": "François", "Sarkozy": "Nicolas"}
    return list_firstnames


def display_names(list_names,list_firstnames):  # Display the list of president's names (without any duplicates) and their first names
    print("\n List of presidents from the document corpus:")
    for i in range(len(list_names)):
        print("-", list_names[i])
    for i in range(len(list_names)):
        print(f"{list_names[i]}'s first name is: {list_firstnames[list_names[i]]}.")


special_characters = {"à": "a", "â": "a", "ä": "a", "ç": "c", "é": "e", "è": "e", "ê": "e", "ë": "e", "î": "i",
                      "ï": "i", "ô": "o", "ö": "o", "ù": "u", "û": "u", "ü": "u", "ÿ": "y", "œ": "oe", "æ": "ae",
                      "À": "A", "Â": "A", "Ä": "A", "Ç": "C", "É": "E", "È": "E", "Ê": "E", "Ë": "E", "Î": "I",
                      "Ï": "I", "Ô": "O", "Ö": "O", "Ù": "U", "Û": "U", "Ü": "U", "Ÿ": "Y", "Œ": "OE", "Æ": "AE"}


def convert_file(directory,extension):  # Convert the texts in the 8 files to lower case and store the contents in new files that are stored in a new folder called "cleaned"
    # Create a new directory "cleaned" if it doesn't exist
    if not os.path.exists("cleaned"):
        os.makedirs("cleaned")
    for filename in list_of_files(directory, extension):
        # Read the content of each file
        with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
            content = file.read()
            cleaned_content = ""
            for char in content:
                # Iterate through each special character and replace if found
                for original_char, replacement_char in special_characters.items():
                    if char == original_char:
                        char = replacement_char
                        break
                # Convert uppercase letters to lowercase
                if ord("A") <= ord(char) <= ord("Z"):
                    char = chr(ord(char) + 32)
                cleaned_content += char
            # Create a new filename for the cleaned text
            new_filename = f"Cleaned_text_{filename}"
            new_file_path = os.path.join("cleaned", new_filename)
            # Create a new filename for the cleaned text
            with open(new_file_path, "w", encoding="utf-8") as new_file:
                new_file.write(cleaned_content)


convert_file("speeches", "txt")

punctuation_characters = ["!", '"', "'", "(", ")", ",", "-", ".", ":", ";", "?", "#", "$", "%", "&", "*", "+", "/", "<",
                          "=", ">", "@", "[", "]", "^", "_", "`", "{", "|", "}", "~", "//"]


def delete_punctuation(directory,extension):  # For each file stored in the "cleaned" directory, run through its text and remove any punctuation characters
    for filename in list_of_files(directory, extension):
        # Get the full file path
        file_path = os.path.join(directory, filename)
        with (open(file_path, "r", encoding="utf-8") as file):
            content = file.read()
            cleaned_content = ""
            # Iterate through each character in the content
            for char in content:
                # Check if the character is not in the list of punctuation characters
                if char not in punctuation_characters:
                    # Append the character to the cleaned content
                    cleaned_content += char
                else:
                    # Append a space to the cleaned content for punctuation characters
                    cleaned_content += " "
            # Write the cleaned content back to the original file
            with open(file_path, "w", encoding="utf-8") as new_file:
                new_file.write(cleaned_content)


delete_punctuation("cleaned", "txt")


# ------------------------------------------------------------------------------#
#                   THE TF-IDF METHOD WRITTEN BY AXEL                          #
# ------------------------------------------------------------------------------#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ TF (Term Frequency) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def tf(directory, extension):  # Return a dictionary associating with the word the number of times it appears
    tf_scores = {}
    for filename in list_of_files(directory, extension):
        with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
            content = file.read()
            text = content.split()
            for word in text:
                if word not in tf_scores:
                    tf_scores[word] = {}
                if filename not in tf_scores[word]:
                    tf_scores[word][filename] = 1
                else:
                    tf_scores[word][filename] += 1
    return tf_scores


tf_scores = tf("cleaned", "txt")

# ~~~~~~~~~~~~~~~~~~~~~~ IDF (Inverse Document Frequency) ~~~~~~~~~~~~~~~~~~~~~~#

from math import log


def idf(directory, extension):  # Return a dictionary associating with each word its IDF score
    nbText = len(list_of_files(directory, extension))
    inText = {word: 0 for word in tf(directory, extension)}
    for filename in list_of_files(directory, extension):
        with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
            content = file.read()
            text = content.split()

        for word in inText:
            if word in text:
                inText[word] += 1
    idf_score = {word: log(nbText / inText[word]) for word in inText if inText[word] != 0}
    return idf_score


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ Final Score ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def TF_IDF_matrix(directory, extension):  # Create the TF-IDF matrix
    term_frequencies = tf(directory, extension)
    idf_scores = idf(directory, extension)
    corpus = list_of_files(directory, extension)
    unique_words = set()
    for filename in corpus:
        with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
            content = file.read()
            text = content.split()
            unique_words.update(text)
    unique_words = list(unique_words)
    tf_idf_matrix = []
    for document in corpus:
        row = []
        for word in unique_words:
            tf_value = term_frequencies.get(word, {}).get(document, 0)
            idf_value = idf_scores.get(word, 0)
            row.append(tf_value * idf_value)
        tf_idf_matrix.append(row)
    return tf_idf_matrix


tf_idf_matrix = TF_IDF_matrix("cleaned", "txt")


def tf_idf_dictionary(directory, extension):  # Return a dictionary associating with each word its TF-IDF
    tf_scores = tf(directory, extension)
    idf_scores = idf(directory, extension)
    tfidf = {}
    for word in tf_scores:
        tfidf[word] = {}
        for file in tf_scores[word]:
            if word in idf_scores:
                tfidf[word][file] = tf_scores[word][file] * idf_scores[word]
            else:
                tfidf[word][file] = 0
    return tfidf

# WRITTEN BY AXEL

def unimportant_words(directory, extension):  # Display the list of least important words in the document corpus
    unimportant = []
    tfidf = tf_idf_dictionary(directory, extension)
    for word in tfidf:
        for file in tfidf[word]:
            if tfidf[word][file] == 0:
                unimportant.append(word)
                break
    return unimportant

unimportantwords = unimportant_words("cleaned","txt")

def highest_TF_IDF_score(directory, extension):  # Display the first 10 words with the highest TD-IDF scores
    # Get the TF-IDF dictionary for the documents in the given directory
    tf_idf_dict = tf_idf_dictionary(directory, extension)
    # Flatten the dictionary into a list of tuples
    flat_scores = []
    for word, scores in tf_idf_dict.items():
        # Calculate the total TF-IDF score for each word
        total_score = sum(scores.values())
        flat_scores.append((word, total_score))
    # Sort the total scores in descending order
    for i in range(len(flat_scores)):
        for j in range(i + 1, len(flat_scores)):
            # Swap if the score at position i is less than the score at position j
            if flat_scores[i][1] < flat_scores[j][1]:
                flat_scores[i], flat_scores[j] = flat_scores[j], flat_scores[i]
    print("\nList of words with the highest TF-IDF scores:")
    top_scores = flat_scores[:10]
    for i in range(len(top_scores)):
        word, score = top_scores[i]
        print(f"{i + 1}. {word} (TF-IDF Score: {score})")


# WRITTEN BY AXEL

def mostRepeatedWord(directory, extension, President,unimportantwords):
    tf_scores = {}
    mostRepeatedWord = []
    PresidentName = President
    for filename in list_of_files(directory, extension):
        with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
            if PresidentName in filename:
                content = file.read()
                text = content.split()
                for word in text:
                    if word not in tf_scores:
                        tf_scores[word] = 1
                    else:
                        tf_scores[word] += 1
                    if word not in unimportantwords:
                        y = word
    for word in unimportantwords:
        if word in tf_scores:
            del tf_scores[word]
    for word in tf_scores:
        if tf_scores[y] < tf_scores[word]:
            if len(mostRepeatedWord) != 0:
                for i in range(len(mostRepeatedWord)):
                    if tf_scores[mostRepeatedWord[i]] < tf_scores[word]:
                        del (mostRepeatedWord[i])
                        y = word
                        mostRepeatedWord.append(y)
                    elif tf_scores[mostRepeatedWord[i]] == tf_scores[word] and mostRepeatedWord[i] != word:
                        y = word
                        mostRepeatedWord.append(y)
                    else:
                        y = word
            else:
                y = word
                mostRepeatedWord.append(y)
        elif tf_scores[y] == tf_scores[word]:
            if len(mostRepeatedWord) != 0:
                for i in range(len(mostRepeatedWord)):
                    if tf_scores[mostRepeatedWord[i]] < tf_scores[y] and y != word:
                        del (mostRepeatedWord[i])
                        mostRepeatedWord.append(y)
                        mostRepeatedWord.append(word)
                    elif tf_scores[mostRepeatedWord[i]] == tf_scores[y] and y != word and mostRepeatedWord[i] != y and \
                            mostRepeatedWord[i] != word:
                        mostRepeatedWord.append(y)
                        mostRepeatedWord.append(word)
            else:
                mostRepeatedWord.append(y)
                mostRepeatedWord.append(word)
        else:
            if len(mostRepeatedWord) != 0:
                for i in range(len(mostRepeatedWord)):
                    if tf_scores[mostRepeatedWord[i]] < tf_scores[y]:
                        del (mostRepeatedWord[i])
                        mostRepeatedWord.append(y)
                    elif tf_scores[mostRepeatedWord[i]] == tf_scores[y] and mostRepeatedWord[i] != y:
                        mostRepeatedWord.append(y)
            else:
                mostRepeatedWord.append(y)
    return mostRepeatedWord

# WRITTEN BY KIM LAN

def word_mentions(tf_scores,chosen_word):  # Return a dictionary associating a president with their number of mention(s) of the chosen word
    # Initialize an empty dictionary to store scores
    cleaned_scores = {}
    if chosen_word in tf_scores:
        for file_name, score in tf_scores[chosen_word].items():
            # Clean the president's name from the file name
            cleaned_name = file_name.replace("Cleaned_text_Nomination_", "").replace(".txt", "")
            cleaned_name_without_nums = ""
            # Remove numeric characters from the cleaned name
            for char in cleaned_name:
                if not char.isdigit():
                    cleaned_name_without_nums += char
            # Update the scores dictionary with the total mention count for each president
            if cleaned_name_without_nums in cleaned_scores:
                cleaned_scores[cleaned_name_without_nums] += score
            else:
                cleaned_scores[cleaned_name_without_nums] = score
    return cleaned_scores

def most_mentions(chosen_word_mentions, chosen_word):  # Display the president with the most mentions of the chosen word
    # Initialize the variables
    max_count = 0
    most_mentioned_president = ""
    # Iterate through each president and their mention count
    for president, count in chosen_word_mentions.items():
        # Update variables if the current president has more mentions
        if count > max_count:
            max_count = count
            most_mentioned_president = president
    print(
        f"The president with the most mentions of '{chosen_word}' is: {most_mentioned_president} (Count: {max_count})")

def word_first_mention(tf_scores, chosen_word):  # Display the first president to mention the chosen word
    # Initialize variables to track the first mention
    first_mention = None
    min_count = float('inf')
    if chosen_word in tf_scores:
        # Iterate through each document and its mention count for the current word
        for filename, count in tf_scores[chosen_word].items():
            # Update variables if the current mention is earlier than the current minimum
            if count < min_count:
                min_count = count
                first_mention = filename
    else:
        # Handle the case when the word is not in tf_scores
        print(f"The word '{chosen_word}' is not mentioned in any file.")
        # You can choose to return or handle this case differently based on your requirements
    if first_mention is not None:
        cleaned_name = first_mention.replace("Cleaned_text_Nomination_", "").replace("1", "").replace("2", "").replace(
            ".txt", "")
        print(f"The first president to mention '{chosen_word}' is: {cleaned_name}")

# WRITTEN BY AXEL

def wordSaidByAllPresident(directory,extension,unimportantwords):  # Excepti the unimportant words, which word(s) did all the president mention?
    inText = {}
    wordSaidByAllPresident = []
    for i in tf(directory, extension):
        inText[i] = 0
    for filename in list_of_files(directory, extension):
        with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
            content = file.read()
            text = content.split()
        for i in tf(directory, extension):
            if i in text and i not in unimportantwords:
                inText[i] += 1
    nbText = len(list_of_files(directory, extension))
    for word in inText:
        if inText[word] == nbText:
            wordSaidByAllPresident.append(word)
    return wordSaidByAllPresident

# ------------------------------------------------------------------------------#
#                             PART 2 OF THE PROJECT                            #
# ------------------------------------------------------------------------------#

# ------------------------------------------------------------------------------#
#                   QUESTION TOKENIZATION WRITTEN BY AXEL                      #
# ------------------------------------------------------------------------------#

# WRITTEN BY AXEL

def question_tokenization(question):  # Return the list of words that make up the question
    cleaned_question = ""
    for char in question:
        for original_char, replacement_char in special_characters.items():
            if char == original_char:
                char = replacement_char
                break
        if ord("A") <= ord(char) <= ord("Z"):
            char = chr(ord(char) + 32)
        if char not in punctuation_characters:
            cleaned_question += char
        else:
            cleaned_question += " "
    cleaned_question = cleaned_question.split()
    return cleaned_question

# ------------------------------------------------------------------------------#
#        SEARCH FOR THE QUESTION WORDS IN THE CORPUS WRITTEN BY KIM LAN        #
# ------------------------------------------------------------------------------#

def question_terms_in_corpus(cleaned_question, directory,extension):  # Identify the terms in the question that are also present in the document corpus
    # Initialize a set to store unique words
    words = set()
    for filename in list_of_files(directory, extension):
        with open(os.path.join(directory, filename), "r", encoding="utf-8") as file:
            content = file.read()
            words_in_file = content.split()
            # Update the set of found words with the intersection of the words of the question and the words in the file
            words.update(set(cleaned_question) & set(words_in_file))
    # Convert the set of words to a list and return
    return list(words)

# ------------------------------------------------------------------------------#
#   CALCULATE THE TF-IDF VECTOR FOR THE TERMS IN QUESTION WRITTEN BY AXEL       #
# ------------------------------------------------------------------------------#

def question_tf_score(cleaned_question, directory,extension):  # Associate a TF (Term Frequency) score with each word in the question. Set a 0 for words in the corpus that are not part of the question.
    list_files = list_of_files(directory, extension)
    tf_scores = {word: [] for word in cleaned_question}
    total_words_question = len(cleaned_question)
    common_terms = question_terms_in_corpus(cleaned_question, directory, extension)
    for i, file_name in enumerate(list_files):
        with open(os.path.join(directory, file_name), "r", encoding="utf-8") as file:
            content = file.read()
            text = content.split()
            for word in cleaned_question:
                if word in common_terms:
                    tf = text.count(word) / total_words_question
                    tf_scores[word].append(tf)
                else:
                    tf_scores[word].append(0)
    return tf_scores

def question_idf_score(cleaned_question, directory,extension):  # Use the previously calculated IDF scores of the words in the question that are in the corpus
    global_idf = idf(directory, extension)
    idf_score = {}
    for word in cleaned_question:
        idf_score[word] = global_idf.get(word, 0)
    return idf_score

def question_tf_idf_vector(cleaned_question, directory, extension):
    list_files = list_of_files(directory, extension)
    question_tf = question_tf_score(cleaned_question, directory, extension)
    question_idf = question_idf_score(cleaned_question, directory, extension)
    # Initialize TF-IDF vector with zeros
    question_tf_idf = [0] * len(list_files)
    # Populate TF-IDF vector with calculated scores
    for i, file_name in enumerate(list_files):
        with open(os.path.join(directory, file_name), "r", encoding="utf-8") as file:
            content = file.read()
            text = content.split()
            # Calculate TF-IDF for each word in the question for the current document
            tf_idf_score = 0
            for word in cleaned_question:
                tf_idf_score += question_tf[word][i] * question_idf[word]
            question_tf_idf[i] = tf_idf_score
    return question_tf_idf

# ------------------------------------------------------------------------------#
#                   CALCULATING SIMILARITY WRITTEN BY KIM LAN                  #
# ------------------------------------------------------------------------------#

# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~ SCALAR PRODUCT ~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

def scalar_product(A,B):  # Take as parameters two vectors A and B of the same dimension M (number of words in the corpus). Calculate and return A.B
    # Initialize the scalar product variable
    scalar_prod = 0
    # Iterate through each component in the vectors
    for i in range(len(A)):
        # Update the scalar product with the product of corresponding components
        scalar_prod += A[i] * B[i]
    return scalar_prod

# ~~~~~~~~~~~~~~~~~~~~~~~~~~ NORM OF THE VECTOR ~~~~~~~~~~~~~~~~~~~~~~~~~~#

from math import sqrt

def norm_vector(A):  # Calculate and return the square root of the sum of the squares of its components
    # Initialize the sum
    sum_squares = 0
    for value in A:
        sum_squares += value ** 2
    # Calculate the square root of the sum of squares to get the norm
    norm = sqrt(sum_squares)
    return norm

# ~~~~~~~~~~~~~~~~~~~~~~~~ CALCULATING SIMILARITY ~~~~~~~~~~~~~~~~~~~~~~~~#

def similarity_score(A, B):  # Calculate the similarity of two vectors
    # Calculate the scalar product of vectors A and B
    scalar = scalar_product(A, B)
    # Calculate the norms of vectors A and B
    norm_A = norm_vector(A)
    norm_B = norm_vector(B)
    # Check for division by zero to avoid errors
    if norm_A * norm_B == 0:
        result = 0
    else:
        # Calculate the similarity score using the given formula
        result = scalar / (norm_A * norm_B)
    return result

# ------------------------------------------------------------------------------#
#         CALCULATING THE MOST RELEVANT DOCUMENT WRITTEN BY KIM LAN            #
# ------------------------------------------------------------------------------#

def most_relevant_doc(tf_idf_matrix, question_vector,list_files):  # Return the document with which the question obtains the highest similarity value
    # Initialize variables to track the highest similarity and the most relevant document
    highest_similarity = 0
    most_relevant_document = None
    # Iterate through each document vector in the TF-IDF matrix
    for i in range(len(tf_idf_matrix)):
        # Extract the document vector from the TF-IDF matrix
        document_vector = tf_idf_matrix[i]
        # Calculate the similarity score between the question vector and the document vector
        current_similarity = similarity_score(question_vector, document_vector)
        # Update the highest similarity and most relevant document if the current similarity is higher
        if current_similarity > highest_similarity:
            highest_similarity = current_similarity
            most_relevant_document = list_files[i]
    return most_relevant_document

# ------------------------------------------------------------------------------#
#                       GENERATING A RESPONSE WRITTEN BY AXEL                  #
# ------------------------------------------------------------------------------#

def question_tfidf_score(cleaned_question, directory, extension):
    tfidf = {}
    idf = question_idf_score(cleaned_question, directory, extension)
    tf = question_tf_score(cleaned_question, directory, extension)
    for word in tf:
        tfidf[word] = {}
        for filename in tf[word]:
            tfidf[word][filename] = tf[word][filename] * idf[word]
    return tfidf

def answer_generation(directory, extension, cleaned_question, tf_idf_matrix, question_vector, list_files):
    mostRelevantDoc = most_relevant_doc(tf_idf_matrix, question_vector, list_files)
    tfidf = question_tfidf_score(cleaned_question, directory, extension)
    mostRelevantWord = None
    for word in tfidf:
        tfidf_value = tfidf[word][mostRelevantDoc]
        if tfidf_value > max_tfidf_value:
            max_tfidf_value = tfidf_value
            mostRelevantWord = word
    with open(os.path.join(directory, most_relevant_doc), "r", encoding="utf-8") as file:
        most_relevant_doc_content = file.read()
    sentences_divided = most_relevant_doc_content.split(".")
    for sentence in sentences_divided:
        if mostRelevantWord in sentence:
            mostRelevantSentence = sentence
            break
    return mostRelevantSentence

# ------------------------------------------------------------------------------#
#                         REFINE AN ANSWER WRITTEN BY AXEL                      #
# ------------------------------------------------------------------------------#

def refining_answer(directory, extension, question, tf_idf_matrix, question_vector, list_files):
    answer = answer_generation(directory, extension, question, tf_idf_matrix, question_vector, list_files)
    term_of_the_question = question_terms_in_corpus(question, directory, extension)
    refine_dico = {"Comment": "Après Analyse, ", "Pourquoi": "Car, ", "Peux-tu": "Oui, bien sûr!",
                   "Quel": "C'est que, ", "Qui": "C'est, ", "Quoi": "c'est, "}
    for word in refine_dico:
        if word == term_of_the_question:
            final_answer = refine_dico[word] + answer
    return final_answer

# ------------------------------------------------------------------------------#
#                       MAIN PROGRAM WRITTEN BY KIM LAN                        #
# ------------------------------------------------------------------------------#

# The final main program must have a menu offering the user two options:
# - Access Part I functionalities at the user's request
# - Access Chatbot mode, allowing the user to ask a question

def main():
    while True:
        print("\n~~~~~~~~~~~~ MENU ~~~~~~~~~~~~")
        print("1. Access to Part I Functionalities")
        print("2. Access to Chatbot Mode")
        print("0. Exit")
        choice = input("Enter your choice (0-2): ")
        if choice == "0":
            print("\nExiting the program.")
            break
        elif choice == "1":
            part_one_menu()
        elif choice == "2":
            question = str(input("\nEnter your question: "))
            cleaned_question = question_tokenization(question)
            question_vector = question_tf_idf_vector(cleaned_question, "cleaned", "txt")
            list_files = list_of_files("cleaned", "txt")
            result = most_relevant_doc(tf_idf_matrix, question_vector,list_files)
            print("The most relevant document is: ", result)
        else:
            print("Invalid choice. Please enter a number between 0 and 2.")

def part_one_menu():
    while True:
        print("\n~~~~~~~~ PART I FUNCTIONALITIES ~~~~~~~~")
        print("1. Display the list of presidents from the document corpus and their first names")
        print("2. Display all the unimportant words")
        print("3. Display the first 10 words with the highest TF-IDF scores")
        print("4. Display the most repeated word by the President of your choice (Excepti the 'unimportant' words)")
        print("5. Display which president(s) mention(s) the word of your choice and among them which one mentions it the most")
        print("6. Display the first president to mention the word of your choice")
        print("7. Display which word(s) all the president mention (Excepti the 'unimportant' words)")
        print("0. Return to the main menu")
        part_one_choice = input("Enter your choice (0-7): ")
        if part_one_choice == "0":
            print("Returning to the main menu.")
            break
        elif part_one_choice in ["1", "2", "3", "4", "5", "6", "7"]:
            part_one_functions(part_one_choice)
        else:
            print("Invalid choice. Please enter a number between 0 and 7.")

def part_one_functions(choice):
    if choice == "1":
        list_firstnames = first_names()
        display_names(list_names, list_firstnames)
    elif choice == "2":
        print("\nList of least important words in the document corpus: ")
        print(unimportantwords)
    elif choice == "3":
        highest_TF_IDF_score("cleaned", "txt")
    elif choice == "4":
        President = str(input("\nFrom which president, do you want to know the most repeated word ? "))
        if ord("a") <= ord(President[0]) <= ord("z"):
            President = chr(ord(President[0]) - 32) + President[1:]
        if President not in list_names:
            print(f"No president named {President} found in our data")
        else:
            most_repeated = mostRepeatedWord("cleaned", "txt", President,unimportantwords)
            print(f"{President} repeats the most : {most_repeated[0]}")
    elif choice == "5":
        chosen_word = str(input("\nWhat is the word you're looking for ? "))
        chosen_word=chosen_word.lower()
        chosen_word_mentions = word_mentions(tf_scores, chosen_word)
        if chosen_word_mentions:
            print(f"The president(s) who mention(s) '{chosen_word}' is/are:")
            for key, value in chosen_word_mentions.items():
                print(f"- {key}: {value} mentions")
            most_mentions(chosen_word_mentions, chosen_word)
        else:
            print("The chosen word is not mentioned in any file.")
    elif choice == "6":
        chosen_word = str(input("\nWhat is the word you're looking for ? "))
        chosen_word = chosen_word.lower()
        word_first_mention(tf_scores, chosen_word)
    elif choice == "7":
        result = wordSaidByAllPresident("cleaned", "txt",unimportantwords)
        if result == []:
            print("\nNo word was mentioned by all presidents.")
        else:
            print("\nWord(s) mentioned by all presidents : ")
            for i in range(len(result)):
                print("-", result[i])

main()