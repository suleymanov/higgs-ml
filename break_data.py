# Print info
if __name__ == '__main__' :
	print "\nThis script divides data file (train or test)"
	print "According to NA values structure in data points\n"

import csv, os, sys, numpy as np

def break_data(data_file, tmplt) :
	'''
		This function will divide train/test file with dataset for Higgs boson
		machine learning contest into 6 non-overlapping datasets and write
		them to separate files.
	'''
	assert os.path.exists(data_file)
	all_data = list(csv.reader(open(data_file, "rb"), delimiter = ","))
	header = all_data[0]
	all_data = all_data[1:]
	
	i_1 = header.index("DER_mass_MMC")
	i_2 = header.index("DER_deltaeta_jet_jet")
	i_3 = header.index("PRI_jet_leading_pt")
	sel1 = np.array([row[i_1] == "-999.0" for row in all_data])
	sel2 = np.array([row[i_2] == "-999.0" for row in all_data])
	sel3 = np.array([row[i_3] == "-999.0" for row in all_data])
	
	# define set A - examples with all variables defined
	filterA = ~(sel1 | sel2 | sel3)
	setA = np.array([all_data[i] for i in range(len(all_data)) if filterA[i]])
	with open(tmplt + " (A).csv", "wb") as csvfile :
		setAwriter = csv.writer(csvfile, delimiter = ",")
		setAwriter.writerow(header)
		for row in setA :
			setAwriter.writerow(row)
	
	# define set B - remaining examples with all variables defined 
	# except DER_mass_MMC
	filterB = sel1 & (~sel2) & (~sel3)
	setB = np.array([all_data[i] for i in range(len(all_data)) if filterB[i]])
	with open(tmplt + " (B).csv", "wb") as csvfile :
		setBwriter = csv.writer(csvfile, delimiter = ",")
		setBwriter.writerow(header)
		for row in setB :
			setBwriter.writerow(row)
	
	# define set C - remaining examples with all variables defined 
	# except DER_deltaeta_jet_jet
	filterC = (~sel1) & sel2 & (~sel3)
	setC = np.array([all_data[i] for i in range(len(all_data)) if filterC[i]])
	with open(tmplt + " (C).csv", "wb") as csvfile :
		setCwriter = csv.writer(csvfile, delimiter = ",")
		setCwriter.writerow(header)
		for row in setC :
			setCwriter.writerow(row)
	
	# define set D - remaining examples with all variables defined
	# except DER_mass_MMC and DER_deltaeta_jet_jet
	filterD  = sel1 & sel2 & (~sel3)
	setD = np.array([all_data[i] for i in range(len(all_data)) if filterD[i]])
	with open(tmplt + " (D).csv", "wb") as csvfile :
		setDwriter = csv.writer(csvfile, delimiter = ",")
		setDwriter.writerow(header)
		for row in setD :
			setDwriter.writerow(row)
	
	# define set E - remaining examples with all variables defined
	# except DER_deltaeta_jet_jet and PRI_jet_leading_pt
	filterE = (~sel1) & sel2 & sel3
	setE = np.array([all_data[i] for i in range(len(all_data)) if filterE[i]])
	with open(tmplt + " (E).csv", "wb") as csvfile :
		setEwriter = csv.writer(csvfile, delimiter = ",")
		setEwriter.writerow(header)
		for row in setE :
			setEwriter.writerow(row)
	
	# define set F - remaining examples with all variables defined
	# except DER_mass_MMC, DER_deltaeta_jet_jet and PRI_jet_leading_pt
	filterF = sel1 & sel2 & sel3
	setF = np.array([all_data[i] for i in range(len(all_data)) if filterF[i]])
	with open(tmplt + " (F).csv", "wb") as csvfile :
		setFwriter = csv.writer(csvfile, delimiter = ",")
		setFwriter.writerow(header)
		for row in setF :
			setFwriter.writerow(row)
	
	# make sure everything was done correctly
	num_ex = setA.shape[0] + setB.shape[0] + setC.shape[0] + \
			 setD.shape[0] + setE.shape[0] + setF.shape[0]
	assert num_ex == len(all_data)
						
if __name__ == '__main__' :
	break_data(sys.argv[1], sys.argv[2])