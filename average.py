f = open("average_cf.txt","r")
f1 = open("average_fa.txt","r")
sum = 0
i=0
for line in f:
	i+=1
	sum+= float(line)
Average_error = sum/i
Percentage_error = Average_error*100/5
print "Collaborative Filtering;",Percentage_error

sum =0
i=0

for line in f1:
	i+=1
        sum+= float(line)
Average_error = sum/i
Percentage_error = Average_error*100/5
print "Friends Average:", Percentage_error

