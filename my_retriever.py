import math
import time

class Retrieve:
    # Create new Retrieve object storing index and termWeighting scheme
    def __init__(self,index, termWeighting):
        self.index = index
        self.termWeighting = termWeighting
    
    def forQuery(self, query):
        
#        record duration
        begin = time.time()
        dtc_dict = self.docid_terms_counts()
        
        candidate = self.getCandidate(dtc_dict, query)#get the subset for each query
        candidateid_size_dict = {}#calculate the similarity between query and candidate document (cos<q,d>)
        idf_dict = self.calculate_idf()# dictionary form {term:idf}
        similarity_dict = {}# dictionary form {docid:similarity}
        for candidate_docid in candidate:
            #calculate the size of each candidate
            candidate_size = self.computeVectorLenth(candidate[candidate_docid], self.termWeighting, idf_dict)
            #vector lenth is the size of candidate
            candidateid_size_dict[candidate_docid] = candidate_size
            #compute similarity and store them into dictionary
            similarity_dict[candidate_docid] = self.computeDotproduct(query,candidate[candidate_docid], self.termWeighting, idf_dict)/candidate_size
        #sort the similarity dictionary    
        sorted_by_value = sorted(similarity_dict,key = lambda x:similarity_dict[x],reverse = True)
        #store the top 10 similarity docid into result list
        result = sorted_by_value[:10]
        end = time.time()
        duration = end - begin
        print("duration for the query: ", duration)
        return result
           
    def getCandidate(self,dtc_dict,query):#docid - term - counts
        candidate_dtc_dict={}
        query_set = set(query.keys())
        for docid in dtc_dict:
            candidate_set = set(dtc_dict[docid])#{docid1:set(term1,term2...), ...}
            if(len(query_set & candidate_set) > 0):
                candidate_dtc_dict[docid] = dtc_dict[docid]
        return candidate_dtc_dict
    
    
    #5. functions to compute required value
    def calculate_D(self):
        temp=set()
        for term in self.index:
            for docid in self.index[term]:
                temp.add(docid)
        return len(temp)
    
   
    def calculate_df(self):
        df_dict={}
        for term in self.index:
            df_dict[term] = len(self.index[term])
        return df_dict
    
    
    def calculate_idf(self):
        df_dict = self.calculate_df()
        D = self.calculate_D()
        
        idf_dict = {}
        for term in df_dict:
            idf_dict[term]=math.log(D/df_dict[term])
        
        return idf_dict
    
   
    def docid_terms_counts(self):
        docDict = {}
        for term in self.index:
            for docid in self.index[term]:
                if docid not in docDict:
                    docDict[docid] = {}
                docDict[docid][term] = self.index[term][docid]
        
        return docDict
        
    def computeVectorLenth(self,doc_dict,termWeighting,idf_dict):
        summation = 0
        if termWeighting == "binary":
            for term in doc_dict:
                summation +=1
                
        elif termWeighting == "tf":
            for term in doc_dict:
                summation += doc_dict[term]**2
        
        elif termWeighting == "tfidf":
            for term in doc_dict:
                summation += (doc_dict[term]*idf_dict[term])**2
                
        summation = math.sqrt(summation)
        return summation
        
        
    def computeDotproduct(self,query,dtc_dict,termWeighting,idf_dict):
        summation = 0
        for term in query:
            if term in dtc_dict:
                if termWeighting == "binary":
                        summation +=1       
                elif termWeighting == "tf":
                        summation += query[term] * dtc_dict[term]
                elif termWeighting == "tfidf":
                        summation += query[term] * dtc_dict[term] * idf_dict[term]**2
        return summation
            
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        