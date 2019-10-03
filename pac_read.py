import random
random.seed(0)
from collections import OrderedDict

class PAC_Reader:

      def __init__(self):
          pass
          
      def process(self, path):
          lines = open(path, "r").readlines()
          print ("create maps from processed pacs file...")
          pacs_map = {}
          for line in lines[1:]:
              line = line.strip()
              elements = line.split("\t")
              pacs_map[elements[0]] = (elements[1], elements[2])
              
          print (str(len(pacs_map))+" pacs entry created...")
          return pacs_map

      def year_map(self, path):
          lines = open(path, "r").readlines()
          print ("create maps from processed pacs file...")
          year_map = {}
          paper_map = OrderedDict()
          for line in lines[1:]:
              line = line.strip()
              elements = line.split("\t")
              paper_doi, paper_year = '"'+elements[0]+'"', int(elements[-1])
              if paper_year not in year_map:
                  year_map[paper_year] = []
              year_map[paper_year].append(paper_doi)
        
          for year in year_map:
              papers = year_map[year]
              random.shuffle(papers)
              year_map[year] = papers

              for i in range(len(papers)):
                  paper_map[papers[i]] = (i, year)

          print('year statistics')
          for year in sorted(year_map.keys()):
              print(year, len(year_map[year]))
          return year_map, paper_map
          