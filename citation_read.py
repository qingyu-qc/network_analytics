from paper import Article
import sys, operator

class Citation_Reader:

      def __init__(self, pacs_map):
          
          self.pacs_map = pacs_map
          self.papers = {}
          
      def create_paper(self, paper_doi):
          if paper_doi not in self.papers:             
             paper = Article(paper_doi)
             pac_code = self.pacs_map[paper_doi]
             
             paper.set_pac_id(pac_code[0])
             paper.set_pac_set(eval(pac_code[1]))
          
             self.papers[paper_doi] = paper
                         
          return self.papers[paper_doi]
      
      def process(self, path):
          print("creating citation network...")
          lines = open(path, "r").readlines()
          total_length = len(lines) - 1
          print("total number of citation pairs: "+str(total_length))
          count = 0
          errors = []
          for line in lines[1:]:
            try:
              elements = line.strip().split(",")
              A, B = self.create_paper(elements[0][1:-1]), self.create_paper(elements[1][1:-1])
              A.cites_paper(B)
              B.cited_by_paper(A)
              count += 1
          
            except KeyboardInterrupt:
               sys.exit(0)
            except:  
              errors.append(str(sys.exc_info()[1])+"\n")
              
          writer = open("citation_errors.txt", "w")
          writer.writelines(errors)   
          writer.close()   
          print ('successfully create '+str(len(self.papers))+' papers')
          lines = []
          
          return sorted(list(self.papers.values()), key=operator.attrgetter('doi'))
      
      def generate_mapping(self, input_path, year_map, paper_map, dest_path):
            def swap(paper_doi):
                  paper_index, paper_year = paper_map[paper_doi][0], paper_map[paper_doi][1]
                  swapped_paper_index = len(year_map[paper_year]) - 1 - paper_index
                  swapped_paper = year_map[paper_year][swapped_paper_index]
                  return swapped_paper 

            print("read citation pairs...")
            lines = open(input_path, "r").readlines()
            newlines = [lines[0]]
            for line in lines[1:]:
                elements = line.strip().split(",")
                query, subject = elements[0], elements[1]
                swapped_query, swapped_subject = swap(query), swap(subject)
                newlines.append(swapped_query + ',' + swapped_subject + '\n')
            writer = open(dest_path, 'w')
            print('write', len(newlines), 'pairs')
            writer.writelines(newlines)
            writer.close()