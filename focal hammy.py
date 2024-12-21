"""
Hamurabi Python 3.13 port. December 2024. M Lauderdale
Much credit to Doug Dyment - the original author of this legendary program
The intent of this python code is to mimic the original as closely as is practical
I have included much of the August, 1968 FOCAL source here (with line nums) for history
Doug's original code has 45 lines and the PDP-8 he ran on had only 4KB user space
Also, FOCAL has only one conditional statement (IF) and it's really clunky
Thus Doug created quite a bit of code smell to work within the limitations
of the tiny memory and FOCALs IF statements... so hat's off to him! The original
FOCAL is https://svn.so-much-stuff.com/svn/trunk/pdp8/src/decus/focal8-5/f0005.fc
"""
import random as rnd

# ---------------------------
def focal_fran():
    """
    simulate the old 1968 FOCAL random number function
    according to the DEC FOCAL programming manual:
    The random number generator function (FRAN) computes a
    nonstatistical pseudo-random number between ±1.
    """
    return(rnd.uniform(-0.99999999999999999,0.99999999999999999))    

# ---------------------------
def input_num(prompt):
    """
    prompt the user for a numeric input
    prompt again if the input is not numeric
    return an integer or a float
    """
    answer = None
    while answer == None:
        try:
            answer = int(input(prompt))
        except:
            pass
    return(answer)    

# ---------------------------
def buy_land(currentGrain,landCost):
    """
    Input routine for annual land purchase
    Returns the price paid in grain and acres purchased
    """
    while True:
        acresBought = input_num("How many acres do you wish to buy?")
        amtPaid = acresBought * landCost
        if acresBought < 0:
            print("Hamurabi: I cannot do what you wish!")
        elif amtPaid > currentGrain:
            print("Hamurabi: Think again. You have only",currentGrain,"bushels of grain.")
        else:
            break
    return(acresBought,amtPaid)

# ---------------------------
def sell_land(currentAcres,landCost):
    """
    Input routine for annual land sale
    Returns the earnings in grain and acres sold
    """
    while True:
        acresSold = input_num("How many acres do you wish to sell?")
        amt_earned = acresSold * landCost
        if acresSold < 0:
            print("Hamurabi: I cannot do what you wish!")
        elif acresSold > currentAcres:
            print("Hamurabi: Think again. You have only",currentAcres,"acres of land.")
        else:
            break
    return(acresSold,amt_earned)
 
# ---------------------------
def feed_people(currentGrain):
    """
    Input routine for annual food allocation
    Returns the food bushels used
    """
    while True:
        foodUsed = input_num("How many bushels do you wish to feed your people?")
        if foodUsed < 0:
            print("Hamurabi: I cannot do what you wish!")
        elif foodUsed > currentGrain:
            print("Hamurabi: Think again. You have only",currentGrain,"bushels of grain.")
        else:
            break
    return(foodUsed)
 
# ---------------------------
def plant_crops(currentGrain,currentAcres,currentPop):
    """
    Input routine for annual planting
    Each peasant can tend up to 10 acres
    Seed required is .5 bushel per acre
    Returns the seed used and acres planted
    """
    while True:
        acresPlanted = input_num("How many acres do you wish to plant with seed?")
        if acresPlanted < 0:
            print("Hamurabi: I cannot do what you wish!")
        elif acresPlanted > currentAcres:
            print("Hamurabi: Think again. You have only",currentAcres,"acres of land.")
        elif currentGrain < int(acresPlanted/2):
            print("Hamurabi: Think again. You have only",currentGrain,"bushels of grain for seed.")
        elif currentPop * 10 < acresPlanted:
            print("Hamurabi: Think again. You have only",currentPop,"people to tend the fields.")
        else:
            break
    return(int(acresPlanted/2),acresPlanted)

# ---------------------------
def user_says():
    """
    Input routine to ask the user if they want to continue
    Returns the user decision
    """
    print()
    while True:
        userInput = input("Do you wish to continue? (Y) or (N) >")
        if userInput in ("Y","y"):
            return(True)
        elif userInput in ("N","n"):
            return(False)
        else:
            pass

# ---------------------------  
#begin main
rnd.seed()
keepGoing=True

#FOCAL source group 1 (initialization):
#1.10 S P=95;S S=2800;S H=3000;S E=200;S Y=3;S A=1000;S I=5;S Q=1

P=95 #population
S=2800 #stores - total grain on hand
H=3000 #harvest - grain harvested
E=200 #eaten - grain destroyed by rats
Y=3 #yield - harvest yield bushels/acre
A=1000 #acres - total acres
I=5 #immigration - total people coming/departing 
Q=1 #question - multiuse variable for input from user

#FOCAL source group 2 (annual report):
#2.10 S D=0
#2.20 D 6;T "I BEG TO REPORT THAT LAST YEAR"D," DIED OF STARVATION,
#2.25 T !I," PEOPLE CAME INTO THE CITY,";S P=P+I;I (-Q)2.3
#2.27 S P=FITR(P/2);T !"HALF THE PEOPLE DIED FROM A PLAGUE EPIDEMIC,
#2.30 T !"AND THE POPULATION IS NOW"P,!!"THE CITY NOW OWNS
#2.35 T A," ACRES OF LAND."!!;I (H-1)2.5;T "WE HARVESTED
#02.40 D 3.2;T " THE HARVEST WAS"H," BUSHELS."!E
#02.50 T " BUSHELS OF GRAIN WERE DESTROYED BY RATS AND YOU NOW HAVE
#02.60 T !S," BUSHELS IN STORE."!!!"DO YOU WISH TO CONTINUE?
#02.70 A " (ANSWER YES OR NO)"Q,!;I (Q-0NO)2.8,7.4
#02.80 I (Q-0YES)2.7,3.1,2.7

D = 0
while keepGoing:
    #these vars are for our python functions
    spent = 0
    acresSown = 0
    seed = 0
    food = 0
    print("\nHamurabi:")
    print("I beg to report that last year {0:,d} died of starvation,".format(D))
    print("{0:,d} people came to the city,".format(I),end='')
    P=P+I
    #2.25 Focal tests Q like this: IF (-Q)2.3 this translates to if -Q < 0 then goto 2.3
    if Q==0:
        #there is a 10% chance of plague
        #2.27
        P=int(P/2)
        print("\nhalf the people died from a plague epidemic,")
    else:
        #2.30
        print("and the population is now",P)
        print("\nThe city now owns {0:,d} acres of land.".format(A))
        print()
    #2.35 Focal: IF (H-1)2.5 this translates to if H-1 < 0 then goto 2.5 
    if H>0:
        print("We harvested {0:,d} bushels per acre; ".format(Y),end='')
        C=1
        print("the harvest was {0:,d} bushels.".format(H))
    #2.5
    print("{0:,g} bushels of grain were destroyed by rats and you now have".format(E))
    print("{0:,g} bushels in store.".format(S))
    #2.7
    keepGoing=user_says()
    if not keepGoing:
        break
    
    #FOCAL source group 3 (land trading):
    #03.10 D 6;D 8;S Y=C+17;T "THIS YEAR, LAND MAY BE TRADED FOR
    #03.20 T Y," BUSHELS PER ACRE;";S C=1
    #03.30 A !"HOW MANY ACRES DO YOU WISH TO BUY?"!Q;I (Q)7.2,3.8
    #03.40 I (Y*Q-S)3.9,3.6;D 4.6;G 3.3
    #03.50 D 4.5;G 3.3
    #03.60 D 3.9;G 4.8
    #03.70 S A=A+Q;S S=S-Y*Q;S C=0
    #03.80 A !"TO SELL?"!Q;I (Q)7.2,3.9;S Q=-Q;I (A+Q)3.5
    #03.90 S A=A+Q;S S=S-Y*Q;S C=0
       
    #3.1
    C = int(5*abs(focal_fran()))+1
    Y = C + 17
    print("\nThis year land may be traded for {0:,d} bushels per acre;".format(Y))
    C = 1
    
    if S>=Y: #buy land
        #3.3
        nLand,spent = buy_land(S,Y)
        S -= spent
        A += nLand
        C = 0
    
    if A > 0 and not spent: #sell land (if you didn't buy any)
        #3.8 
        nLand,proceeds = sell_land(A,Y)
        S += proceeds
        A -= nLand
        C = 0
 
    #FOCAL source group 4 (feeding and planting):
    #04.10 T !"HOW MANY BUSHELS OF GRAIN DO YOU WISH TO DISTRIBUTE
    #04.11 A " AS FOOD?"!Q;I (Q)7.2;I (Q-S)4.2,4.7;D 4.6;G 4.1
    #04.20 S S=S-Q;S C=1
    #04.30 A !"HOW MANY ACRES OF LAND DO YOU WISH TO PLANT WITH SEED?"!D
    #04.40 I (D)7.2;I (A-D)4.45;I (FITR(D/2)-S-1)4.65;D 4.6;G 4.3
    #04.45 D 4.5;G 4.3
    #04.50 D 7;T A," ACRES."!
    #04.60 D 7;T S," BUSHELS IN STORE."!
    #04.65 I (D-10*P-1)5.1;D 7;T P," PEOPLE."!;G 4.3
    #04.70 D 4.2
    #04.80 D 6;T "YOU NOW HAVE NO GRAIN LEFT IN STORE, SO YOU HAVE
    #04.90 T !"NONE LEFT TO USE AS SEED THIS YEAR."!;S D=0
    
    if S == 0:
        #4.8
        print("Hamurabi: you now have no grain left in store, so you have")
        print("none left to use as food or seed.")
        D = 0
    else:
        #4.1 how much to feed?
        food = feed_people(S)
        #4.2
        Q = food
        S -= food
        C = 1
        if  S > 0:
            #so far, so good
            #4.3 how much to plant?
            seed,acresSown = plant_crops(S,A,P)
            D = acresSown    
            S -= seed
        else:
            print("Hamurabi: you now have no grain left in store, so you have")
            print("none left to use as seed.")
            D = 0

    #FOCAL source group 5 (calculate annual results):
    #05.10 S S=S-FITR(D/2);D 8;S Y=C;S H=D*Y
    #05.20 D 8;S E=0;I (FITR(C/2)-C/2)5.3;S E=S/C
    #05.30 S S=S-E+H;D 8;S I=FITR(C*(20*A+S)/P/100+1);S C=FITR(Q/20)
    #05.40 S Q=FITR(10*FABS(FRAN()));I (P-C)2.1;S D=P-C;S P=C;G 2.2

    #5.1
    C = int(5*abs(focal_fran()))+1
    Y = C
    H = D * Y
    #5.2
    C = int(5*abs(focal_fran()))+1
    E = 0
    if int(C/2)-C/2 >= 0:
        #coin toss if rats invade
        E = int(S / C)
    #5.3
    S = S - E + H
    C = int(5*abs(focal_fran()))+1
    I = int(C*(20*A+S)/P/100+1)
    C = int(food/20)
    #5.4
    Q = int(10*abs(focal_fran()))
    if P-C < 0:
        D = 0 #no starvation
    else:
        D = P-C
        P = C
#end main loop        
