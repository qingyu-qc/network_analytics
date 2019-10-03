
class Article:

      def __init__(self, doi):
          self.doi = doi
          self.fields = []
          self.cites_papers = []
          self.cited_by_papers = []

      def __hash__(self):
          return hash(self.doi)

      def __eq__(self, other):
          return self.doi == other.doi

      def __cmp__(self,other):
          return cmp(self.doi, other.doi)

      def cites_paper(self, paper):
          self.cites_papers.append(paper)
   
      def cited_by_paper(self, paper):
          self.cited_by_papers.append(paper)

      def set_pac_id(self, pac_id):
          self.pac_id = pac_id
          
      def set_pac_set(self, pac_set):
          self.pac_set = pac_set

      def set_fields(self, file_content):          
          self.fields = file_content.keys()
      
      def __repr__(self):
          return self.doi
          
      
      def debug(self):
          print ("paper doi: "+self.doi)
          print ("cites papers: "+str(self.cites_papers))
          print ("cited by papers: "+str(self.cited_by_papers))
          print ("pac_id: "+str(self.pac_id))
          print ("pac_set: "+str(self.pac_set))
          
