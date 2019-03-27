from src.genetic.member import Member
from src.genetic.chromosome import Chromosome
from random import Random
import sys
import types

debug = len(sys.argv) > 1 and sys.argv[1] == '-debug'
csv_mode = len(sys.argv) > 1 and sys.argv[1] == "-csv"
if not csv_mode:
    csv_mode = len(sys.argv) > 2 and sys.argv[2] == "-csv"
if not debug:
    debug = len(sys.argv) > 2 and sys.argv[2] == '-debug'


mem = Member(Chromosome([]))


class Manager:

    PC = 0.8
    PM = 0.03
    MINIMUM_ITERATIONS = 10
    CSV_FILE = open(
        "C:/Users/mgltorsa/Documents/Workspace/python/genetic_algorithms/genetic.csv", "w")

    def default_evaluate_function(self, x: int):
        x1 = self.transform(x)
        return (1 - (x1 ** 2))

    def transform(self, x):
        y = float(x)-127.5
        y = float(y/127.5)
        return y

    def __init__(self):
        self.chromosome_length = Chromosome.LENGTH
        self.ancient_population = []
        self.random = Random()
        self.population = []
        self.evaluate = self.default_evaluate_function
        self.pc = Manager.PC
        self.pm = Manager.PM
        self.minimum_iteration = Manager.MINIMUM_ITERATIONS
        self.current_iteration = 0

    def set_population(self, population: []):
        self.population = population
        for member in population:
            if(type(member) == type(Member)):
                pass

    def set_evaluate_function(self, evaluate: types.FunctionType):
        self.evaluate = evaluate

    def set_pc(self, pc):
        self.pc = pc

    def set_pm(self, pm):
        self.pm = pm

    """Initialize manager with random population
        Param=number of init members

    """

    def init_random_population(self, init_members=4):
        pop = self.population
        for i in range(0, init_members):
            array_chromosome = []
            for j in range(0, Chromosome.LENGTH):
                random = self.random.randint(0, 1)
                array_chromosome.append(random)
            chromosome = Chromosome(array_chromosome)
            member = Member(chromosome)
            pop.append(member)

    def evolve(self):

        self.__evolve__()
        while(not self.finish()):
            self.__evolve__()
        self.step_1(self.population)

        # TODO Realizar while hasta convergencia
        return True

    def __evolve__(self):
        if(self.population == None or len(self.population) == 0):
            raise Exception("There is no population")
        if(csv_mode):
            self.export("")
            self.export("Iteracion #%s" % (len(self.ancient_population)+1))
            self.export("")
        self.print_population(self.population)
        table = self.step_1(self.population)
        pairs = self.step_2(table)
        new_population = self.step_3(pairs)
        mutated_population = self.step_4(new_population)
        self.ancient_population.append(self.population)
        self.population = mutated_population
        print("")
        print("new population...")
        self.print_population(self.population)

    def finish(self):
        self.current_iteration += 1
        finished = self.current_iteration >= self.minimum_iteration
        if(debug):
            option = str(input("continue? (y/n) : "))
            if(option == "n"):
                print("finished")
                return True
            else:
                print("continue")
                return False
        else:
            return finished

    def print_population(self, population):
        print("population is:")
        i = 0
        for member in self.population:
            print("%s -> %s" % (i, member.get_chromosome().get_chromosome()))
            i += 1
        print("")

    def str_of_chromosome(self, chromosome: []):
        str_chromosome = "'"
        for i in chromosome:
            str_chromosome += str(i)
        return str_chromosome

    def export(self, line):
        Manager.CSV_FILE.write(line+"\n")

    def step_1(self, population: []):
        if(debug):
            print("step 1")
        if(csv_mode):
            self.export("Informacion:;PC:;%.3f;PM:;%.3f" % (self.pc, self.pm))
            self.export("")
            self.export("")
            self.export("Paso 1")
            self.export("")
            self.export("")
        meta_population = []
        total_fx = 0
        for i in range(0, len(population)):
            member: Member
            member = population[i]
            chromosome = str(member.get_chromosome())
            x = int(chromosome, 2)
            fx = self.evaluate(x)
            meta_population.append([i, chromosome, x, fx])
            total_fx += fx
        # TODO Falta sacar los porcentajes para eleccion
        return self.calculate_step_1_table(meta_population, total_fx)

    def calculate_step_1_table(self, meta_population, total_fx):
        table = []
        fix_amount = 0
        if(debug):
            print("each member has this attributes")
        if(csv_mode):
            self.export(
                "Id;Cromosoma;x;valor real;fx;probabilidad de aparicion;probabilidad acumulada;")
        for meta_member in meta_population:
            i = meta_member[0]
            chromosome = meta_member[1]
            x = meta_member[2]
            fx = meta_member[3]
            fix = float(fx)/float(total_fx)
            fix_total = fix+fix_amount
            fix_amount = fix_total
            meta_info = [i, chromosome, x, fx, fix, fix_total]
            if(debug):
                print("id:%s, attrib: %s, x: %s, f(x): %.3f, fix: %.3f, fix_amount: %.3f " %
                      (i+1, chromosome, x, fx, fix, fix_total))
            table.append(meta_info)
            if(csv_mode):
                self.export("%s;'%s;%s;%.3f;%.3f;%.3f;%.3f" % (
                    i+1, chromosome, x, self.transform(x), fx, fix, fix_amount))
        if(debug):
            print("total fx -> %s" % (total_fx))
            print("")
        if(csv_mode):
            self.export("")
            self.export(";;;Fx Total:;%.3f;;;" % (total_fx))
            self.export("")
        return table

    def step_2(self, table: []):
        if(debug):
            print("step 2")
        if(csv_mode):
            self.export("")
            self.export("")
            self.export("Paso 2")
            self.export("")
            self.export("")
        n_members = len(table)
        total_pairs = int(n_members/2)
        pairs = []
        if(debug):
            print("selected pairs are:")
        for i in range(0, total_pairs):
            if(csv_mode):
                self.export("pareja #%s" % (i+1))
            ran_fix_amount_1 = self.random.random()
            ran_fix_amount_2 = self.random.random()
            id_member1 = self.get_random_id_member(table, ran_fix_amount_1)
            id_member2 = self.get_random_id_member(table, ran_fix_amount_2)
            if(csv_mode):
                self.export("Se genera el numero:;%.3f;Fue escogido el miembro;#%s" % (
                    ran_fix_amount_1, id_member1+1))

            while(id_member2 == id_member1):
                ran_fix_amount_2 = self.random.random()
                id_member2 = self.get_random_id_member(table, ran_fix_amount_2)
            if(debug):
                print("pair %s are meber_%s and member_%s" %
                      (i+1, id_member1+1, id_member2+1))
            if(csv_mode):
                self.export("Se genera el numero:;%.3f;Fue escogido el miembro;#%s" % (
                    ran_fix_amount_2, id_member2+1))
                self.export("")
            pairs.append((id_member1, id_member2))
        if(debug):
            print("")

        return pairs

    def get_random_id_member(self, table: [], ran_fix_amount):

        for meta_info in table:
            if(ran_fix_amount <= meta_info[5]):
                return meta_info[0]
        return -1

    def step_3(self, pairs: []):
        if(debug):
            print("step 3")
        if(csv_mode):
            self.export("")
            self.export("")
            self.export("Paso 3")
            self.export("")
            self.export("")
        new_population = []
        # TODO Falta verificar el PC
        if(debug):
            print("pc: %s" % (self.pc))
        for member_id_1, member_id_2 in pairs:
            random = self.random.random()
            if(csv_mode):
                self.export("pareja formada por;%s;%s" %
                            (member_id_1+1, member_id_2+1))
                self.export("el numero aleatorio fue:;%.3f;Con PC;%.3f" %
                            (random, self.pc))
            member_1 = self.population[member_id_1]
            member_2 = self.population[member_id_2]
            if(random < self.pc):
                # TODO Punto de corte desde 0 hasta length-2 (ejemplo si chromosome es 8 entonces el
                # corte se hace hasta 6 para no coger todos los bits)
                cut_point = self.random.randint(0, self.chromosome_length-2)
                if(csv_mode):
                    self.export("punto de cruze:;%s" % (cut_point+1))
                new_chromosome_1 = self.extract_sub_chromosome(member_1, 0, cut_point)+self.extract_sub_chromosome(
                    member_2, cut_point, self.chromosome_length)
                new_chromosome_2 = self.extract_sub_chromosome(member_2, 0, cut_point)+self.extract_sub_chromosome(
                    member_1, cut_point, self.chromosome_length)
                if(debug):
                    print("between %s and %s" % (member_id_1+1, member_id_2+1))
                    print("cut point = %s with new members: \n new member : %s \n new member : %s"
                          % (cut_point+1, str(new_chromosome_1), str(new_chromosome_2)))
                    print("")
                if(csv_mode):
                    self.export("Nuevo miembro 1:;%s" %
                                (self.str_of_chromosome(new_chromosome_1)))
                    self.export("Nuevo miembro 2:;%s" %
                                (self.str_of_chromosome(new_chromosome_2)))
                    self.export("")
                member_1 = Member(Chromosome(new_chromosome_1))
                member_2 = Member(Chromosome(new_chromosome_2))
            else:
                if(debug):
                    print("there are no new members, cloning old members")
                    print("new member: %s" %
                          (member_1.get_chromosome().get_chromosome()))
                    print("new member: %s" %
                          (member_2.get_chromosome().get_chromosome()))
                if(csv_mode):
                    self.export("Se clonaron los miembros")
                    self.export("Nuevo miembro 1:;%s" % (self.str_of_chromosome(
                        member_1.get_chromosome().get_chromosome())))
                    self.export("Nuevo miembro 2:;%s" % (self.str_of_chromosome(
                        member_2.get_chromosome().get_chromosome())))

            new_population.append(member_1)
            new_population.append(member_2)
        return new_population

    def extract_sub_chromosome(self, member: Member, init, last):
        chromosome = member.get_chromosome().get_chromosome()
        sub_chromosome = []
        i = init
        while(i < last):
            sub_chromosome.append(chromosome[i])
            i += 1
        return sub_chromosome

    def step_4(self, new_population):
        if(debug):
            print("step 4")
        if(csv_mode):
            self.export("")
            self.export("")
            self.export("Paso 4")
            self.export("")
            self.export("")
        mutated_population = []
        id_current_member = 0
        for member in new_population:
            print("for member %s " % (id_current_member+1))
            if(csv_mode):
                self.export("Para el miembro #;%s" % (id_current_member+1))
                self.export("Con cromosoma; %s" % (self.str_of_chromosome(
                    member.get_chromosome().get_chromosome())))
                self.export("Con PM;%.3f" % (self.pm))
            array_chromosome = member.get_chromosome().get_chromosome()
            array_chromosome = self.mutate(array_chromosome, self.pm)
            if(debug):
                print("new chromosome for %s is %s" %
                      (id_current_member+1, array_chromosome))
                print("")
            if(csv_mode):
                self.export("Generando el nuevo cromosoma:;%s" %
                            (self.str_of_chromosome(array_chromosome)))
                self.export("")
            mutated_member = Member(Chromosome(array_chromosome))
            mutated_population.append(mutated_member)
            id_current_member += 1
        if(csv_mode):
            self.export("")
        return mutated_population

    def mutate(self, chromosome, pm):
        mutated_chromosome = []
        id_current_member = 0
        random_numbers = []
        i = 0
        for allele in chromosome:
            random_number = self.random.random()
            random_numbers.append(random_number)
            if(debug):
                print("random number was %s for meber #%s in chromosome #%s" % (
                    random_number, id_current_member+1, i+1))
            new_allele = int(not allele)
            mutated_chromosome.append(new_allele)
        if(csv_mode):
            parsed_numbers = ""
            i = 0
            while(i < len(random_numbers)):
                if(i < len(random_numbers)-1):
                    parsed_numbers += "%.3f; " % random_numbers[i]
                else:
                    parsed_numbers += "%.3f" % random_numbers[i]
                i += 1
            self.export("fueron generados los numeros random:;%s" %
                        (parsed_numbers))
        return mutated_chromosome
