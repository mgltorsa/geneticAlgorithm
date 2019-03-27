import sys
from src.genetic.manager import Manager


manager = Manager()


args = sys.argv

debug = len(sys.argv) > 1 and sys.argv[1] == '-debug'
csv_mode = len(sys.argv) > 1 and sys.argv[1] == "-csv"
if not csv_mode:
    csv_mode = len(sys.argv) > 2 and sys.argv[2] == "-csv"
if not debug:
    debug = len(sys.argv) > 2 and sys.argv[2] == '-debug'

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
