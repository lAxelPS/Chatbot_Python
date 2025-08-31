Name of project team members :
TRAN Kim Lan

PASQUET--SALETES Axel

Instructions for use :
Main Menu:
A menu will be displayed guiding the user to choose an option between 0 and 2. Enter a number to perform the corresponding actions:

Exit the program
Access to Part I Functionalities
Access to Chatbot Mode
If the user enters a number other than those specified, it will display "Invalid choice. Please enter a number between 0 and 2".

Part I Functionalities (Option 1):
If the user enters '1.', another menu will be displayed. The user then has to choose an option between 0 and 7. Enter a number to perform the corresponding actions:

Return to the main menu
Display the list of presidents from the document corpus and their first names
Display all the unimportant words
Display the first 10 words with the highest TF-IDF scores
Display the most repeated word by the President of your choice (Excepti the 'unimportant' words)
Display which president(s) mention(s) the word of your choice and among them which one mentions it the most
Display the first president to mention the word of your choice
Display which word(s) all the president mention (Excepti the 'unimportant' words)
If the user enters a number apart from those asked, it will display "Invalid choice. Please enter a number between 0 and 7".

Chatbot Mode (Option 2):
If the user enters '2.', the program will prompt the user to enter their question. After entering the question, the program will provide a proper answer.

Dependencies to be installed :
Python 3.x

Python File provided in the repository

Directory called "speeches", it should contain 8 text files:

-Nomination_Chirac1

-Nomination_Chirac2

-Nomination_Giscard dEstaing

-Nomination_Hollande

-Nomination_Macron

-Nomination_Mitterand1

-Nomination_Mitterand2

-Nomination_Sarkozy.

List of known bugs :
Bugs on the following functions:

-most_relevant_doc(tf_idf_matrix, question_vector,list_files)

-question_tfidf_score(cleaned_question, directory, extension)

-answer_generation(directory, extension, cleaned_question, tf_idf_matrix, question_vector, list_files)

-refining_answer(directory, extension, question, tf_idf_matrix, question_vector, list_files)
