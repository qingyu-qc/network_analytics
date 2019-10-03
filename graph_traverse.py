import math_functions as math
import sys, os
from collections import deque
from multiprocessing  import Process
import numpy as np
from file_writer import AverageJaccard_Writer, MedianJaccard_Writer, StdJaccard_Writer, ChildSize_Writer, FirstChild_Writer
class GraphHandler(Process):

      CACHE = {}
      BUFFER_SIZE = 10000
      def __init__(self, t_id, tasks, queue):
          Process.__init__(self)
          
          self.t_id = t_id
          self.local_cache = {}
          self.folder = "Threads"
          self.prefix = "Thread_"+str(t_id)+"_"      
          self.queue = queue
          self.depth_results = {}
          self.summary_writers = [AverageJaccard_Writer(os.path.join(self.folder,self.prefix+"average.csv")), MedianJaccard_Writer(os.path.join(self.folder,self.prefix+"median.csv")), 
          StdJaccard_Writer(os.path.join(self.folder,self.prefix+"std.csv")), ChildSize_Writer(os.path.join(self.folder,self.prefix+"size.csv"))]
          self.detail_writers = [FirstChild_Writer(os.path.join(self.folder,self.prefix+"first.csv"), 1)]
                
      def run(self):
          print ("Thread "+str(self.t_id)+" starts processing "+str(len(self.queue))+" papers...")
          condition = True
          paper_count = 0
          while condition:
            try:
                paper = self.queue.pop()
                paper_count += 1
                if paper_count % 1000 == 0:
                   print("Thread "+str(self.t_id)+" finished processing "+str(paper_count)+" remaining size: "+str(len(self.queue)))
                self.traverse(paper)   
                
            except Exception as e:
                condition = False
                print(e)

          print ("Thread "+str(self.t_id)+" start writing...")           
          for summary_writer in self.summary_writers:
              summary_writer.writelines()
              
          for detail_writer in self.detail_writers:
              detail_writer.writelines()
                  
      def traverse(self,paper):
          
          root = paper
          children = []
          stack = deque()
          stack.append([paper, 0])
          uniques = set()
          first = True
          
          while stack:              
              current, depth = stack.popleft()
              if current not in uniques: 
                if not first:
                   r_id, c_id, sim = self.compare_sim(root, current)  
                   
                   for detail_writer in self.detail_writers:
                       detail_writer.calculate(root.doi, depth, [sim], [current.doi])
                
                   if r_id not in self.local_cache:
                      self.local_cache[r_id] = {}
                      self.local_cache[r_id][c_id] = sim
                   
                   if root.doi not in self.depth_results:
                      self.depth_results[root.doi] = {}
                   if depth not in self.depth_results[root.doi]:
                      self.depth_results[root.doi][depth] = []
                   self.depth_results[root.doi][depth].append(sim)
                   
                   uniques.add(current)
                else:
                   first = False
               
                subchildren = current.cited_by_papers
                for subchild in subchildren:
                   if subchild not in uniques:
                    stack.append([subchild, depth+1])  
          for r_id in self.depth_results:
              for depth in sorted(self.depth_results[r_id].keys()):
                  depth_values = self.depth_results[r_id][depth]
                  for summary_writer in self.summary_writers:
                      summary_writer.calculate(r_id, depth, depth_values)           
          self.depth_results = {}

      def retrive_batch(self,N):
          batch = []
          start = 0
          while not self.queue.empty() and start < N:
                batch.append(self.queue.get()) 
                start += 1
          return batch 
              
      def compare_sim(self, root, child):
      
          r_id , c_id = math.compare(root.pac_id, child.pac_id)
             
          if r_id in self.local_cache and c_id in self.local_cache[r_id]:            
             return (r_id, c_id, self.local_cache[r_id][c_id])
      
          r_set, c_set = root.pac_set, child.pac_set
          
          if len(r_set) > len(c_set):
             r_set, c_set = c_set, r_set
          
          sim = math.jaccard(r_set, c_set)
          return (r_id, c_id, sim)
              
          
