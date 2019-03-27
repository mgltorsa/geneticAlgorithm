import sys
from src.genetic.manager import Manager


manager = Manager()


args = sys.argv

debug = False
csv_mode=False

if(len(args) >1 ):
    if(args[1] == "-debug"):
        debug = True
        print("in debug mode")
    if(len(args)>2):
        csv_mode=args[2] == "-csv"

init_population = 4

if(debug):
    try:
        init_population = int(input("type init population : "))
        print("number was -> %s" % (init_population) )
        while(init_population <= 0):
            print("number must be greater than 0")
            init_population = int(input("type init population : "))
    except Exception:
        init_population=4
        print("incorrect input, init_population will be %s" % (init_population) )


manager.init_random_population(init_population)
manager.evolve()
print("Finished Example")
