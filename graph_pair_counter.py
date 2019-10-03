import math_functions as math
import sys, os
from collections import deque
from multiprocessing  import Process
import numpy as np
from file_writer import PairWriter

class GraphPair(Process):

      def __init__(self, t_id, tasks, queue):
          Process.__init__(self)
          
          self.t_id = t_id
          self.local_cache = {}
          self.folder = "thread_pairs"
          self.prefix = "thread_pairs_"+str(t_id)+"_"      
          self.queue = queue
          self.depth_results = {}
          self.summary_writers = [PairWriter(os.path.join(self.folder,self.prefix+"pairs.txt"))]
                
      def run(self):
          print ("Thread "+str(self.t_id)+" starts processing "+str(len(self.queue))+" papers...")
          condition = True
          paper_count = 0
          while condition:
                paper = self.queue.pop()
                paper_count += 1
                if paper_count % 100 == 0:
                   print("Thread "+str(self.t_id)+" finished processing "+str(paper_count)+" remaining size: "+str(len(self.queue)))
                print ("Thread "+str(self.t_id)+" start processing "+paper.doi+" remaining size: "+str(len(self.queue)))
                self.traverse(paper)   
                
          print ("Thread "+str(self.t_id)+" start writing...")           
          for summary_writer in self.summary_writers:
              summary_writer.writelines()
              
          
                  
      def traverse(self,paper):
          
          root = paper
          children = []
          stack = deque()
          stack.append([paper, 0])
          first = True
          uniques = set()
          while stack:              
              current, depth = stack.popleft()

              if current not in uniques: 
                 if not first:

                    for summary_writer in self.summary_writers:
                      summary_writer.calculate(root.doi, current.doi)
                    uniques.add(current)
              else:
                  first = False
              subchildren = current.cited_by_papers
              for subchild in subchildren:
                    stack.append([subchild, depth+1])  
          

    
              
      
              
          
