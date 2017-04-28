# -*- coding: utf-8 -*-
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
from nltk.tokenize import sent_tokenize
import string


#Questions that will be matched
question_dict = {
    0: 'How strongly do you agree or disagree with our proposed environmental objective for the next regime?',
    1: 'Any additional comments on our proposed environmental objective for the next regime?',
    2: 'How strongly do you agree or disagree with our proposal for the length of the next regime?',
    3: 'Any additional comments on our proposal for the length of the regime?',
    4: 'How strongly do you agree or disagree with our proposal to introduce a new QC/0.125 category for aircraft between 81 and 83.9 EPNdB?',
    5: 'How strongly do you agree or disagree with our proposal for all aircraft quieter than this to remain QC/0 but count towards the airports movement limit?',
    6: 'Any additional comments on our proposals for the Quota Count System?',
    7: 'How strongly do you agree or disagree with the proposal for movement limits to remain unchanged at Heathrow?',
    8: 'Any additional comments on our proposal for Heathrow movement limits?',
    9: 'How strongly do you agree or disagree with the proposal for movement limits to remain unchanged at Gatwick?',
    10: 'Any additional comments on our proposal for Gatwick\'s movement limit?',
    11: 'How strongly do you agree or disagree with the proposal to raise Stansted\'s movement limits to reflect the current number of exempt aircraft in operation?',
    12: 'Any additional comments on our proposal for Stansted\'s movement limit?',
    13: 'How strongly do you agree or disagree with our proposals to encourage the use of quieter aircraft at Heathrow?',
    14: 'Any additional comments on how you feel noise quotas can be set in order to encourage the use of quieter aircraft at Heathrow?',
    15: 'How strongly do you agree or disagree with our proposals to encourage the use of quieter aircraft at Gatwick?',
    16: 'Any additional comments on how you feel noise quotas can best be set in order to encourage the use of quieter aircraft at Gatwick?',
    17: 'How strongly do you agree or disagree with our proposals to encourage the use of quieter aircraft at Stansted?',
    18: 'Any additional comments on how you feel noise quotas can best be set in order to encourage the use of quieter aircraft at Stansted?',
    19: 'Q10 Any further views on our proposals, or their potential impact on governments ability to fulfil requirements of the Public Sector Equality Duty.',
    20: 'What additional evidence do you have on the expected costs and benefits of the policy options outlined in sections 5 and 6 of the IA.',
    21: 'What additional evidence do you have on the assumptions to develop the unconstrained scenario and the policy scenarios outlined in section 7.1.2. In particular, any additional evidence on how airports would make use of the carryover and overrun flexibility and which flights would be affected when and airport hits either its movement or quota limit. Please email any attachments to night.flights@dft.gsi.gov.uk',
    22: 'What additional evidence do you have on how airlines that have ordered new aircraft types (e.g. Airbus A320neo and Boeing 737 Max) plan on introducing these into their fleets, as outlined in section 7.1.4.',
    23: 'What additional evidence do you have on airline responses to a reduction in night flights regarding flight cancellations and rescheduling, and how passengers might respond to these changes, as outlined in sections 6.2.6 and 7.3.',
    24: 'What additional evidence do you have on the likely amount of time needed for stakeholders to read and understand the regulations, as outlined in section 8.2.2.',
    25: 'What additional evidence do you have on the monetised impact on business of the policy options outlined in section 10.',
    26: 'What additional evidence do you have on the economic and wider impacts of changes to the night flights regime outlined in section 11.',
    27: 'What additional evidence do you have on the impact of our policy options on competition, as outlined in section 11.1.',
    28: 'What additional evidence do you have of the policy impacts on small and micro businesses, outlined in section 11.2.',
    29: 'What additional evidence do you have on which policy option is best suited to achieve the environmental objective as outlined in section 12.'

                 }

def extract_qa(content):
    import string
    #Remove illegal characters
    content = content.replace("\n", "");
    content = content.replace("\x0c", "");
    printable = set(string.printable)
    content =  filter(lambda x: x in printable, content)
    # Tokenize document content
    string_list = sent_tokenize(content)
    questions_answers = []
    string_counter = 0
    for string in string_list:
        counter = 0
        while counter < len(question_dict):
            #Get's the fuzzymatching ratio of question to string.
            ratio =  fuzz.partial_ratio(string, question_dict[counter])
            if ratio > 80:
                #If the match ratio is above 80
                #print "Question " + str(counter) + " found on string " + str(string_counter)
                questions_answers.append([counter, str(string_counter), ratio])
                #print question_dict[counter]
                #print string
                #print ratio
            counter = counter + 1
        string_counter = string_counter + 1
    #print ""
    #print questions_answers

    counter = 0
    cleaned_qa = []
    while counter < len(question_dict):
        #print "Looking for answers for " +str(question_dict[counter])
        collated_matches = []

        for match in questions_answers:

            if match[0] == counter:

                #print "match"
                collated_matches.append(match)
        cleaned = sorted(collated_matches, key=lambda i: i[2], reverse=True)
        try:
            cleaned_qa.append(cleaned[0])
        except IndexError:
            pass
        #print question_dict[counter]
        counter = counter + 1
    #print cleaned_qa
    for qa in cleaned_qa:
        #qa.append(answer)
        #print qa
        # "Question is on " + str(qa[1])
        question_string = qa[1]
        try:
            #print "Next question on " + str(cleaned_qa[qa[0]+1][1])
            next_question_string = cleaned_qa[qa[0]+1][1]
        except IndexError:
            next_question_string = cleaned_qa[-1][1]

        if question_string == next_question_string or int(question_string) > (int(next_question_string) - 4):
            #print "next question is on same line"
            try:
                next_question_string = cleaned_qa[qa[0]+4][1]
            except IndexError:
                next_question_string = cleaned_qa[-1][1]
            #print "Next question on " + next_question_string
        answer_lines = int(next_question_string) - int(question_string)
        #print "Answer Lines - " + str(answer_lines)
        counter = 0
        answer = ""
        while counter < answer_lines:

            answer = answer + string_list[(int(question_string)) +  counter]

            counter = counter + 1
        #print answer
        qa.append(answer)

    for qa in cleaned_qa:
        #print ""
        #print "Question - " + question_dict[qa[0]]
        #print ""
        qa.append(question_dict[qa[0]])
        #print "Answer - " + qa[3]

    return cleaned_qa