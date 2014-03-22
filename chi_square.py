#!/opt/python-2.6/bin/python2.6
# Mami Sasaki and Nat Byington
# # LING 572 HW4 Chi Square Feature Selection
# Calculates chi_square feature values from training data
# Args: training data(piped in as stdin) > feat_list

import sys
import re

# For each vector in training data, tally class, terms.
term_in_class = {} # key is ('term', 'class')
classes = {}
terms = {} # tallies doc_freq per term
for line in sys.stdin.readlines():
    c = re.match(r'^[\S]+ ([\S]+) ', line).group(1) # class name
    if c in classes:
        classes[c] += 1
    else:
        classes[c] = 1
    terms_list = re.findall(r'([A-Za-z]+) [0-9]+', line) # list of terms in vector
    for t in terms_list:
        if t in terms:
            terms[t] += 1
        else:
            terms[t] = 1
        if (t, c) in term_in_class:
            term_in_class[(t, c)] += 1
        else:
            term_in_class[(t, c)] = 1

N = 0.0  # Total number of vectors
for c in classes:
    N += classes[c]

# Calculate chi-square for each term.
output = []
for term in terms:
    t_total = terms[term]
    not_t_total = N - t_total
    chi_sq = 0.0
    for c in classes:
        e = (t_total * classes[c]) / N
        o = float(term_in_class.get((term, c), 0))
        e_not = (not_t_total * classes[c]) / N
        o_not = classes[c] - o
        if e != 0:
            chi_sq += (o-e)**2 / e
        if e_not != 0:
            chi_sq += (o_not-e_not)**2 / e_not
    if chi_sq > 0:
        result = (chi_sq, term, t_total)
        output.append(result)

# Output results
output.sort(reverse=True)
for i in output:
    print i[1] + ' ' + str(i[0]) + ' ' + str(i[2])

