from math_functions import jaccard

class Node_Sim:

      def __init__(self):
          pass
          
      def compare_sim(self, root, child):
          r_set, c_set = root.pac_set, child.pac_set
          if len(r_set) > len(c_set):
             r_set, c_set = c_set, r_set
          sim = jaccard(r_set, c_set)
          return sim