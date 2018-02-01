preProcess.py file was used for the preprocessing, by which model.json file was created. In json file I used autoincremented id(0-based indexing) and mapping is present in the docId.txt file. Starting index is 0 and the file present in the ith line has docid (i-1).

in case of any query run using terminal following exactly given format:
	python solve.py x AND y
Command line arguments will be considered as input variables(string x and string y). Input is case sensitive(as mentioned in the question paper), any kind of invalid input will not generate any valid output.

For the query x AND y, merge postings and skip pointers both will be used and no of iterations taken to execute the query will be used as the parameter for the comparison purpose. For x AND y query only once list of documents will be shown in the terminal as output.