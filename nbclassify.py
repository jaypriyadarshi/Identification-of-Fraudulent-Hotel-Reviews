import sys
import os
import math


maindir = sys.argv[1]

f1 = open('nbmodel.txt','r')
f2 = open('nboutput.txt','w')

p1 = f1.readline()
p1 = p1.split(" ")[4]
p1 = p1[:-1]
prior_pos = float(p1)

p1 = f1.readline()
p1 = p1.split(" ")[4]
p1 = p1[:-1]
prior_neg = float(p1)

p1 = f1.readline()
p1 = p1.split(" ")[4]
p1 = p1[:-1]
prior_truth = float(p1)

p1 = f1.readline()
p1 = p1.split(" ")[4]
p1 = p1[:-1]
prior_fake = float(p1)

probs = f1.readlines()

cond_pos = {}
cond_neg = {}
cond_truth = {}
cond_fake = {}

for p in probs:
	arg = p.split(" ")
	word = arg[1]
	cls = arg[3]
	val = arg[6]
	
	val = val[:-1]
	
	if cls == "positive":
		cond_pos[word] = float(val)
	
	elif cls == "negative":
		cond_neg[word] = float(val)
	
	elif cls == "truth":
		cond_truth[word] = float(val)

	elif cls == "fake":
		cond_fake[word] = float(val)

paths = []
counter = 0

for (dirpath, dirname,files) in os.walk(maindir):
	for filename in files:
		paths.append(os.path.join(dirpath, filename))

for path in paths:
	
	if ".txt" in path and "README.txt" not in path:
		#print path
		counter = counter+1
		f = open(path,'r')
		content = f.readlines()
		pos_prob = math.log10(prior_pos)
		neg_prob = math.log10(prior_neg)
		truth_prob = math.log10(prior_truth)
		fake_prob = math.log10(prior_fake)
		for i in content:
			text = i.replace("\r","")
			tokens = text.split(" ")
			for each_word in tokens:
				t=""
				for k in each_word:
					if k.isalpha():
						t = t+k
				t = t.lower()
				
				if t in cond_pos:
					try:
						pos_prob = pos_prob+math.log10(cond_pos[t])
					except ValueError:
						pass

				if t in cond_neg:
					try:
						neg_prob = neg_prob+math.log10(cond_neg[t])
					except ValueError:
						pass

				if t in cond_truth:
					try:
						truth_prob = truth_prob+math.log10(cond_truth[t])
					except ValueError:
						pass
				if t in cond_fake:
					try:
						fake_prob = fake_prob+math.log10(cond_fake[t])
					except ValueError:
						pass
		if pos_prob > neg_prob:
			label_b = "positive"
		else:
			label_b = "negative"

		if truth_prob > fake_prob:
			label_a = "truthful"
		else:
			label_a = "deceptive"

		f2.write(label_a+" "+label_b+" "+path+"\n")		
				

f2.close()
