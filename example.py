import sys
from src.genetic.manager import Manager


CSV_FILE = open("./genetic.csv","w")
POPULATION = open("./population.population","r")



manager = Manager()

manager.set_csv_file(CSV_FILE)

manager.set_population_file(POPULATION)




iterations = int(input("ingrese el numero de iteraciones que desea ejecutar : "))
manager.set_iterations(iterations)

manager.evolve()
print("Finished Example")
