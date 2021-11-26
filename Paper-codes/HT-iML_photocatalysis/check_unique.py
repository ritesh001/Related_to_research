import numpy as np
with open('list_rel_2019','r') as f1:
     a = f1.readlines()

list_or = []
for i in range(len(a)):
	list_or.append(a[i].split('/')[0])

f1.close()

common = []
def find_common(fil):
	list_c = []
	with open(fil,'r') as f:
		b = f.readlines()
	for i in range(len(b)):
		list_c.append(b[i].split()[0])
	for i in range(len(b)):
		if list_c[i] in list_or:
			common.append(b[i])
			rem = b[i].split()[0] + '/\n'
			a.remove(rem)
		else:
			continue
	f.close()
	return common, a

def find_common_(fil):
	list_c = []
	with open(fil,'r') as f:
		b = f.readlines()
	for i in range(len(b)):
		list_c.append(b[i].split()[0])
	for i in range(len(b)):
		if b[i] in a:
			common.append(b[i])
			a.remove(b[i])
		else:
			continue
	f.close()
	return common, a

find_common('list_III_X-Y_1_all')
find_common('list_III_X-Y_2_done')
find_common_('list_MXY_1_done')
find_common('list_MXY_2_done')
find_common_('list_scan_2019')

print(len(a))
print(len(common))

f_ = open('left_after_2019_27-06-20.dat','w')
for i in range(len(a)):
	f_.write('%s' %(a[i]))
f_.close()