class Chromosome:

    """Default length for a chromosome"""

    LENGTH = 8

    """param = chromosome"""

    def __init__(self, chromosome=None):
        if(chromosome != None):
            self.chromosome = chromosome
        else:
            self.chromosome=[]

    def set_chromosome(self, chromosome: []):
        self.chromosome = chromosome

    def get_chromosome(self):
        return self.chromosome

    def __str__(self):
        chromosome = ""
        for i in self.chromosome:
            chromosome+= str(i)
        return chromosome
