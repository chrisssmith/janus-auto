import nltk.data
from fuzzywuzzy import fuzz

global question_dict
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
def question_sorter(data):
    from IPython.core.display import display, HTML
    display(HTML("<style>.container { width:100% !important; }</style>"))
    question_list = list(question_dict.values())
    tokenizer = nltk.data.load('tokenizers/punkt/english.pickle')
    clean = '\n-----\n'.join(tokenizer.tokenize(data))
    split_list = clean.split('\n-----\n')

    matches1 = {}
    index_list = []

    for key in question_dict.keys():

        matches2 = {}
        i = 0

        for sentence in split_list:
            x = fuzz.ratio(question_dict[key], sentence)
            matches2[i] = x
            i += 1

        calc = max(matches2, key=matches2.get)
        maximum = [calc, matches2[calc]]
        start_index = max(matches2, key=matches2.get) + 1
        maximum.append(start_index)
        matches1[key] = maximum

    matches3 = {}

    for key, value in matches1.items():
        if value[1] >= 80:
            matches3[key] = matches1[key]
            index_list.append(matches1[key][0])
        else:
            pass

    index_list.pop(0)

    i2 = 0

    for key, value in matches3.items():
        try:
            value.append(index_list[i2] - 1)
            i2 += 1
        except IndexError:
            value.append(len(split_list) - 1)

    responses = {}

    for key, value in matches3.items():

        i = value[2]
        data = []

        while i <= value[3]:
            data.append(split_list[i])
            i += 1

        responses[key] = data
        return data

