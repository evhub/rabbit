from rabbit.all import *

if __name__ == "__main__":
    main = mathbase()
    print("Running Tests...")
    try:
        main.evalfile("Tests.txt")
    finally:
        print("Tests Complete.")
        main.start()
