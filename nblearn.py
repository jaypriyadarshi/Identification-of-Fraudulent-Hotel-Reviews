import sys
import os


maindir = sys.argv[1]

o = open('nbmodel.txt','w')
positive = {}
negative = {}
truth = {}
fake = {}


pos = 0
neg = 0
true = 0
false = 0

total_pos = 0
total_neg = 0
total_true = 0
total_false = 0

pos_class = 0
neg_class = 0
truth_class = 0
fake_class = 0

paths = []
counter = 0 

for dirpath,dirname,files in os.walk(maindir):
	for filename in files:
		paths.append(os.path.join(dirpath, filename))
#print len(paths)

for path in paths:
	
	if ".txt" in path and "README.txt" not in path:
		if "positive" in path:
			pos = 1
			pos_class = pos_class+1
		else:
			pos = 0

		if "negative" in path:
			neg = 1
			neg_class = neg_class+1
		else:
			neg = 0

		if "truthful" in path:
			true = 1
			truth_class = truth_class+1
		else:
			true = 0

		if "deceptive" in path:
			false = 1
			fake_class = fake_class+1
		else:
			false = 0
		#print path
		counter = counter+1
		f = open(path,'r')
		content = f.readlines()
		for i in content:
			text = i.replace("\r","")
			tokens = text.split(" ")
			for new in tokens:
				t=""
				for k in new:
					if k.isalpha():
						t = t+k
				t = t.lower()
				#print t
				if t != "":
					if pos == 1:
						total_pos = total_pos+1
						if t in positive:
							positive[t] = positive[t]+1
						else:
							positive[t] = 1
			
					if neg == 1:
						total_neg = total_neg+1
						if t in negative:
							negative[t] = negative[t]+1
						else:
							negative[t] = 1

					if true == 1:
						total_true = total_true+1
						if t in truth:
							truth[t] = truth[t]+1
						else:
							truth[t] = 1

					if false == 1:
						total_false = total_false+1
						if t in fake:
							fake[t] = fake[t]+1
						else:
							fake[t] = 1
		f.close()
		

#print counter
	
vocab = set(positive.keys() + negative.keys())
vocab_size = len(vocab)

prior_pos = float(pos_class)/(pos_class+neg_class)
prior_neg = float(neg_class)/(pos_class+neg_class)
prior_truth = float(truth_class)/(truth_class+fake_class)
prior_fake = float(fake_class)/(truth_class+fake_class)

o.write("P( positive ) = "+str(prior_pos)+"\n")
o.write("P( negative ) = "+str(prior_neg)+"\n")
o.write("P( truth ) = "+str(prior_truth)+"\n")
o.write("P( fake ) = "+str(prior_fake)+"\n")

for v in vocab:
	if v in positive:
		cond_pos = float((positive[v]+1))/(total_pos + vocab_size)
		
	else:
		cond_pos = float(1)/(total_pos + vocab_size)

	if v in negative:
		cond_neg = float((negative[v]+1))/(total_neg + vocab_size)
	else:
		cond_neg = float(1)/(total_neg + vocab_size)

	if v in truth:
		cond_truth = float((truth[v]+1))/(total_true + vocab_size)
	else:
		cond_truth = float(1)/(total_true + vocab_size)

	if v in fake:
		cond_fake = float((fake[v]+1))/(total_false + vocab_size)
	else:
		cond_fake = float(1)/(total_false + vocab_size)

	o.write("P( "+v+" | positive ) = "+str(cond_pos)+"\n")
	o.write("P( "+v+" | negative ) = "+str(cond_neg)+"\n")
	o.write("P( "+v+" | truth ) = "+str(cond_truth)+"\n")
	o.write("P( "+v+" | fake ) = "+str(cond_fake)+"\n")


o.close()
