from collections import defaultdict
import sys

class Preprocessor:

      def __init__(self, source_path, dest_path):
          print('creating preprocessor...')
          self.errors = []
          self.preprocess(source_path, dest_path)
              
      def preprocess(self, source_path, dest_path):
          lines = open(source_path, "r", encoding="utf-8", errors='ignore').readlines()
          deslines = ["doi\tpacs_id\tpacs_set\tpacs_year\n"]
          print(str(len(lines)-1)+" entries to process")
          for line in lines[1:]:
              try:
                line = line.strip()
                elements = line.split(",")
             
                quotes_elements = line.split("\"")
                doi = elements[0]
                
                if len(quotes_elements) > 1:
                   pacs_id, pacs = self.process_pacs(self.create_pacs(quotes_elements[1][1:-1]))
                else:
                  pacs_id, pacs = self.process_pacs(self.create_pacs(elements[-1][1:-1]))
                deslines.append(doi+"\t"+pacs_id+"\t"+repr(pacs)+"\t"+elements[2]+"\n")
              
              except:
                self.errors.append(line+"\n")
          writer = open(dest_path, "w", encoding="utf-8", errors='ignore')
          writer.writelines(deslines) 
          writer.close()
          
          writer = open("error_lines.txt", "w", encoding="utf-8", errors='ignore')
          writer.writelines(self.errors)
          writer.close()
          
      def create_pacs(self, pacs):
          numbers = pacs.split(",")
          pacset = set()
          newlist = []
          for num in numbers:
              element = int(num)
              if element not in pacset:
                 newlist.append(element)
                 pacset.add(element)
          return newlist           
      
      def process_pacs(self, pacs):
          pacs_string = sorted([str(pac) for pac in pacs])
          return "|".join(sorted(pacs_string)), set(pacs_string)