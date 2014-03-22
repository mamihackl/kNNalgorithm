#!/usr/bin/env python2.6
#Mami Hackl
#Nat Byington
#572 hw4: implement kNN algorithm

import sys,re,math,output

#define constants
EUCLIDEAN=1
COSINE=2
TERMS = set() # master set of training features

# sort features
def sort_data(data,train):
    
   table_list = [] 
   
   if train:
      class_list = {} 
    
   #read data line by line
   lines = data.split('\n')
   for l in lines:
       if not l:break
       news = re.match('^(\S+) (\S+)', l)  
       table = output.Struct()
       table.instance = news.group(1)
       table.cls = news.group(2)

       if train:
          if table.cls not in class_list:
             class_list[table.cls] = 1

       f_list = re.findall('(\w+) (\d+)', l)
       cos_denom = 0
       for t,c in f_list:
           if train:
              TERMS.add(t)
           cos_denom += math.pow(float(c),2)
           if t in TERMS:
               table.terms.add(t) # ensures no OOV test terms get added
           if t not in table.feat_dict:
              table.feat_dict[t] = c
           else:
              table.feat_dict[t] = table.feat_dict.get(t,0) + c 
       table.cos_denom = math.sqrt(cos_denom)
       if table.cos_denom > 0:
           table_list.append(table)

   if train:
      return table_list,class_list
   else:
      return table_list
    

# classify test data
def classify(train,test,class_list):

    # initialize matrix
    matrix = output.Matrix(class_list)

    for test_inst in test:
        neighbors = []
        for train_inst in train:
            sum_val = 0
            term_union = test_inst.terms | train_inst.terms
            for term in term_union:
                v1 = int(train_inst.feat_dict.get(term, 0))
                v2 = int(test_inst.feat_dict.get(term, 0))
                # use euclidean distance
                if sim_func == EUCLIDEAN:
                    sum_val += math.pow((v1 - v2),2)
                # use cosine function 
                else:
                    sum_val += v1 * v2
            if sim_func == EUCLIDEAN:
                dist = math.sqrt(sum_val) 
            else:
                dist = sum_val /(train_inst.cos_denom * test_inst.cos_denom)
            neighbors.append((dist,train_inst.cls))
            #debug
            #print(sim_func,train_inst.instance,test_inst.instance,dist)
       
        if sim_func == EUCLIDEAN:
            neighbors.sort()
        else:
            neighbors.sort(reverse=True)
        # find K numbers of best neighbors
        test_class = {}
        for i in range(kval):
            # get class of neighbor_i
            vote = neighbors[i][1]
            if vote in test_class:
                test_class[vote] += 1
            else:
                test_class[vote] = 1
        # sort dict {class:count, } into list 
        results = sorted(test_class.items(),key=lambda x:int(x[1]),reverse=True)
 
        # assign class with highest vote to test_v
        matrix.set_value(test_inst.cls,results[0][0],1)
        # output
        sysf.write("%s %s" % (test_inst.instance,test_inst.cls))
        for cls,num in results:
            sysf.write(" %s %g" % (cls,(num/float(kval))))
        sysf.write('\n')
    return matrix


#######################
#main function 

#open files
trainf = open(sys.argv[1],'r')
testf = open(sys.argv[2],'r')
kval = int(sys.argv[3])
sim_func = int(sys.argv[4])
sysf = open(sys.argv[5],'w')

# test flag
TRAIN = 1

#sort training data; must be done first to populate TERMS
data = trainf.read() 
train_table,class_list = sort_data(data,TRAIN)

TRAIN = 0 
#sort test data
data = testf.read() 
test_table = sort_data(data,TRAIN)

# classify data 
matrix=classify(train_table,test_table,class_list)

# output result
feat_count = len(TERMS)
doc_count = len(test_table) 
matrix.output_acc(sys.argv[2],doc_count,feat_count,class_list)

#close file handlers
trainf.close()
testf.close()
sysf.close()
