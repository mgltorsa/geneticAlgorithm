from src.genetic.chromosome import Chromosome

class Member:
    def __init__(self, chromosome:Chromosome):
        self.chromosome=chromosome
    
    def get_chromosome(self):
        return self.chromosome