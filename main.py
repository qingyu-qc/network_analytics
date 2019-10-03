from preprocessor import Preprocessor
from pac_read import PAC_Reader
from citation_read import Citation_Reader
from node_sim import Node_Sim
import sys, time, os
from graph_traverse import GraphHandler
import random

def generate_random_graph():
       parameters = sys.argv
       pac_reader = PAC_Reader()
       year_map, paper_map = pac_reader.year_map(parameters[1])
       
       cit_reader = Citation_Reader([])
       cit_reader.generate_mapping(parameters[2], year_map, paper_map, parameters[3])

def produce_final_data():
       parameters = sys.argv
       folder = parameters[1]
       dest_folder = parameters[2]
       names = ['average', 'first', 'median', 'size', 'std']
       number = 16 
       for name in names:
              final_lines = []
              for thread_num in range(number):
                     file_name = 'Thread_'+str(thread_num)+'_'+name+'.csv'
                     file_path = os.path.join(folder, file_name)
                     lines = open(file_path).readlines()
                     final_lines.extend(lines)
              dest_file = name+'.csv'
              dest_path = os.path.join(dest_folder, dest_file)
              writer = open(dest_path, 'w')
              writer.writelines(final_lines)
              writer.close()

parameters = sys.argv

#preprocess pacs file

pac_processor = Preprocessor(parameters[1], parameters[2])

#read preprocessed pacs file

pac_reader = PAC_Reader()

pac_map = pac_reader.process(parameters[1])

#create citation network 
start_time = time.time()
cit_reader = Citation_Reader(pac_map)
papers = cit_reader.process(parameters[2])

#compute each path in multi-thread
random.shuffle(papers)
THREAD_SIZE = 16

batch_size = len(papers) // THREAD_SIZE

batches = []

start_batch = 0

for i in range(THREAD_SIZE):
    if i == THREAD_SIZE - 1:
       batches.append(papers[start_batch:])
    else:
       batches.append(papers[start_batch:start_batch+batch_size])
    start_batch += batch_size

start = 0
thread_list = []

while start < THREAD_SIZE:
      thread = GraphHandler(str(start), papers, batches[start])
      thread_list.append(thread)
      start += 1

for thread in thread_list:
    thread.start()
    
for thread in thread_list:     
    thread.join()


