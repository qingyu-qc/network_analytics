import numpy as np
import pickle
from collections import deque, OrderedDict

class FileWriter:
      def __init__(self, path, heading):
         self.path = path
         self.heading = heading
         self.lines = []
         self.mapping = {}
         self.buffer = 1000
      
      def check_limit(self):
          if len(self.lines) > self.buffer:
             self.writelines()
             self.lines = []
             self.mapping = {}
      
      def calculate(self, doi, depth, items, keys=None):
         self.check_limit()
         
         
      def writelines(self):
         self.writer = open(self.path, 'a')
         self.writer.writelines(self.lines)
         self.writer.close()
         self.lines = []
         self.mapping = {}

class AverageJaccard_Writer(FileWriter):

     def __init__(self, path):
         FileWriter.__init__(self, path, 'Doi,Depth,AverageJaccard\n')
      
     def calculate(self, doi, depth, items, keys=None):
         avg = "{0:.5f}".format(np.mean(items))
         if doi not in self.mapping:
            if len(self.mapping):
               self.lines[-1] += "\n"
               FileWriter.calculate(self, doi, depth, items)
            self.lines.append(doi+","+str(avg))
            self.mapping[doi] = len(self.lines)-1
         else:
            self.lines[self.mapping[doi]] += ","+str(avg)
   
     def calculate(self, doi, depth, items, keys=None):
         avg = "{0:.5f}".format(np.mean(items))
         if doi not in self.mapping:
            if len(self.mapping):
               self.lines[-1] += "\n"
               FileWriter.calculate(self, doi, depth, items)
            self.lines.append(doi+","+str(avg))
            self.mapping[doi] = len(self.lines)-1
         else:
            self.lines[self.mapping[doi]] += ","+str(avg)
         
          
class MedianJaccard_Writer(FileWriter):

     def __init__(self, path):
         FileWriter.__init__(self, path, 'Doi,Depth,MedianJaccard\n')
         
     def calculate(self, doi, depth, items, keys=None):
         median = "{0:.5f}".format(np.median(items))
         if doi not in self.mapping:
            if len(self.mapping):
               self.lines[-1] += "\n"
               FileWriter.calculate(self, doi, depth, items)
            self.lines.append(doi+","+str(median))
            self.mapping[doi] = len(self.lines)-1
         else:
            self.lines[self.mapping[doi]] += ","+str(median)
      

class StdJaccard_Writer(FileWriter):

     def __init__(self, path):
         FileWriter.__init__(self, path, 'Doi,Depth,StdJaccard\n')
         
     def calculate(self, doi, depth, items, keys=None):
         std = "{0:.5f}".format(np.std(items))
         if doi not in self.mapping:
            if len(self.mapping):
               self.lines[-1] += "\n"
               FileWriter.calculate(self, doi, depth, items)
         
            self.lines.append(doi+","+str(std))
            self.mapping[doi] = len(self.lines)-1
         else:
            self.lines[self.mapping[doi]] += ","+str(std)
         
class ChildSize_Writer(FileWriter):
   
     def __init__(self, path):
         FileWriter.__init__(self, path, 'Doi,Depth,ChildSize\n')
         
     def calculate(self, doi, depth, items, keys=None):    
         if doi not in self.mapping:
            if len(self.mapping):
               self.lines[-1] += "\n"
               FileWriter.calculate(self, doi, depth, items)
                 
            self.lines.append(doi+","+str(len(items)))
            self.mapping[doi] = len(self.lines)-1
         else:
            self.lines[self.mapping[doi]] += ","+str(len(items))
         
class FirstChild_Writer(FileWriter):
   
     def __init__(self, path, limit):
         FileWriter.__init__(self, path, 'Doi,Child,Jaccard\n')
         self.depth_limit = limit
         
     def calculate(self, doi, depth, items, keys=None):   
         if depth <= self.depth_limit:
            if doi not in self.mapping:
               if len(self.mapping):
                   self.lines[-1] += "\n"
                   FileWriter.calculate(self, doi, depth, items)
               self.lines.append(doi+","+str(keys[0])+"_"+"{0:.5f}".format(items[0]))
               self.mapping[doi] = len(self.lines)-1
            else:
               self.lines[self.mapping[doi]] += ","+str(keys[0])+"_"+"{0:.5f}".format(items[0])
                
            
