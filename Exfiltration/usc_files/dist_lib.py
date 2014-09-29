import sys, os

def get_feature(x):
	y = x.find('cedd')
	yy = x.find(' ', y+5)
	return x[yy+1:]

def pair_dist(A, B):
	min_dist = sys.float_info.max
	f1_ = get_feature(A).split(' ')
	f2_ = get_feature(B).split(' ')
	print f1_, f2_
	temp = cedd_dist(f1_, f2_)
	print temp
	return temp
	
def cedd_dist(f1, f2):
        f1_len = len(f1)
        f2_len = len(f2)
        if f1_len != f2_len:
                print "length not equal, please check!"
                return sys.float_info.max
        else:
                for i in range(f1_len):
                        f1[i] = float(f1[i])
                        f2[i] = float(f2[i])
                t_sum1 = sum(f1)
                t_sum2 = sum(f2)
                Result = 0
                if t_sum1 == 0 or t_sum2 == 0:
                        Result = 100
                elif t_sum1 == 0 and t_sum2 == 0:
                        Result = 0
                else:
                        tc1 = 0
                        tc2 = 0
                        tc3 = 0
                        for i in range(f1_len):
                                tc1 = tc1 + 1.0*f1[i]*f2[i]/(t_sum1*t_sum2)
                                tc2 = tc2 + 1.0*f1[i]*f1[i]/(t_sum1*t_sum1)
                                tc3 = tc3 + 1.0*f2[i]*f2[i]/(t_sum2*t_sum2)
                        Result = (100 - 100 * tc1/(tc2+tc3-tc1))
                return max(0, Result)

