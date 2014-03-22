#!/opt/python-2.6/bin/python2.6
# Mami Sasaki and Nat Byington
# # LING 572 HW4 Feature Filter
# Uses a feature list sorted by chi_square values to modify training data
# Args: training data, feature list, significance level, new training file

import sys
import re

training = open(sys.argv[1])
feat_list = open(sys.argv[2])
SIG_LVL = float(sys.argv[3])
new_training = open(sys.argv[4], 'w')
chi_sq_0 = 0.0
# Assign proper value to chi_sq_0; assumes df = 2
if SIG_LVL == 0.1:
    chi_sq_0 = 4.605
if SIG_LVL == 0.05:
    chi_sq_0 = 5.991
if SIG_LVL == 0.025:
    chi_sq_0 = 7.378
if SIG_LVL == 0.01:
    chi_sq_0 = 9.210
if SIG_LVL == 0.001:
    chi_sq_0 = 13.816

# Create set of related terms using values from feature list   
related = set()
for f in feat_list.readlines():
    x = re.match(r'^([\S]+) ([\S]+) ', f)
    term = x.group(1)
    chi = float(x.group(2))
    if chi > chi_sq_0:
        related.add(term)

# Cycle through training data; build new training file using only relevant terms
output_flag = False
for line in training.readlines():
    if output_flag:
        new_training.write('\n')
    output_flag = True
    output_list = []
    header = re.match(r'^([\S]+ [\S]+) ', line).group(1)
    output_list.append(header)
    terms_list = re.findall(r' ([A-Za-z]+) ([0-9]+) ', line) # list of (term, count) in vector
    for term in terms_list:
        if term[0] in related:
            x = ' ' + term[0] + ' ' + term[1]
            output_list.append(x)
    new_line = ''.join(output_list)
    new_training.write(new_line)

