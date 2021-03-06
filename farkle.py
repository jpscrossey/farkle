# farkle

'''
FARKLE PYTHON GAME

Where players attempt to reach 5,000 points using x6 dice.
Scoring using 'ONE' and 'FIVE' or a combination of die such as x3 or more of the same number, striaghts, triplets etc...

Single Scoring Dice:

    'FIVE' = 50
    'ONE' = 100

<Combination Scoring Dice>:

    x3 of the same dice = (number on dice * 100) [example: x3 of 3 = 300]
    x4 of any number = 1,000
    x5 of any number = 2,000
    x6 of any number = 3,000
    1-6 straight = 1,500
    three pairs = 1,500
    x4 of any number with a pair = 1,500
    two triplets = 2,500 

'''

import random

'''
GLOBAL VARIABLES
'''
sides = ("ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX")
numbers = {"ONE":1, "TWO":2, "THREE":3, "FOUR":4, "FIVE":5, "SIX":6}
# {die:{count:value, ...}, ...}
scores = {1:{1:100,2:200,3:300,4:1000,5:2000}, 2:{3:200,4:1000,5:2000}, 3:{3:300,4:1000,5:2000}, 4:{3:400,4:1000,5:2000}, 5:{1:50,2:100,3:500,4:1000,5:2000}, 6:{3:600,4:1000,5:2000}}

playing = True

'''
CLASSES
'''
# Generate rolling of dice.
class Dice():
    
    # Create a list for a six sided die.
    def __init__(self):
        self.die = []
        for side in sides:
            self.die.append(side)
            
    # Rolls 'n' amount of dies 
    def rolled(self,dice=6):
        self.dice = dice
        self.rolled = []
        count = 0
        while count < self.dice:
            self.rolled.append(random.choice(self.die))
            count += 1
        print(self.rolled)
        return self.rolled


# As the player rolls they can hold scoring die on each roll.
class Holds():
    
    def __init__(self):
        pass
        
    # Asks the player what die from the roll they wish to hold onto for scoring. 
    def hold_die(self,list):
        self.convert_holding = []
        while True:
            try:
                self.select = [int(self.select) for self.select in input("\nWhich die would you like to hold on to? Furthest left die is '1'. \nUse a space between each die number you're holding and then press 'Enter': ").split()]
            except:
                # this returns an error message if someone enters something other than an integer - and allows them to try again. 
                print("\nYou must enter an integer that corresponds to the number of dice rolled.  If you cannot hold a scoring die, just press 'Enter'")
                continue
            else:
                break
        
        try:
            self.selection = []
            for n in self.select:
                self.selection.append(n-1)

            self.hold = [list[i] for i in self.selection]
        except:
            # this returns an error message the user entered an incorrect index number - and they forefit their turn.
            print("\nUnfortunately you held an invalid die - mistakes can be costly!!!")
            return []
        else:
            # Creates list for scoring die being held, and converts into integer for sorting.
            for i in self.hold:
                self.convert_holding.append(numbers[i])
            return sorted(self.convert_holding)

'''
FUNCTIONS
'''
# Checks for each possible scoring roll
def scoring_rolls(list):
    roll = list
    total = 0
    length = len(roll)
    
    try:
        # Check for 6 die combination rolls.
        if length == 6:
            # x6 of any number.
            if roll[0]==roll[1] and roll[0]==roll[2] and roll[0]==roll[3] and roll[0]==roll[4] and roll[0]==roll[5]:
                total += 3000
            # x2 triplets.
            elif roll[0]==roll[1] and roll[0]==roll[2] and roll[3]==roll[4] and roll[3]==roll[5]:
                total += 2500
            # x4 of any number with a pair.
            elif roll[0]==roll[1] and roll[0]==roll[2] and roll[0]==roll[3] and roll[4]==roll[5] or roll[0]==roll[1] and roll[2]==roll[3] and roll[2]==roll[4] and roll[2]==roll[5]:
                total += 1500
            # Three pairs.
            elif roll[0]==roll[1] and roll[2]==roll[3] and roll[4]==roll[5]:
                total += 1500
            # 1-6 straight.
            elif roll[0] == 1 and roll[1] == 2 and roll[2] == 3 and roll[3] == 4 and roll[4] == 5 and roll[5] == 6:
                total += 1500
            # Checks for all remaining 6 die scoring combinations.
            else:
                dup_1 = []
                dup_2 = []
                for die in roll:
                    dup_1.append(die)
                    counts = roll.count(die)
                    dup_2.append(counts)
                merged_list = [(dup_1[i],dup_2[i]) for i in range(0,len(dup_1))]
                count_set = set(merged_list)
                for a,b in count_set:
                    total += scores[a][b]
        

        # Checks for all <6 die scoring combinations.
        elif length <6:
            dup_1 = []
            dup_2 = []
            for die in roll:
                dup_1.append(die)
                counts = roll.count(die)
                dup_2.append(counts)
            merged_list = [(dup_1[i],dup_2[i]) for i in range(0,len(dup_1))]
            count_set = set(merged_list)
            for a,b in count_set:
                total += scores[a][b]
                
        return total
    except:
        print("\nBUST! - You have not held any or only scoring dice!")
        return 0

# play another game of Farkle.
def replay():
    return input("\nWould you like to play again... Y / N ? ").upper().startswith("Y")

# scoreboard display.
def display_board(player1_total,player2_total):
    print("\nPoint Totals:")
    print("Player 1:",player1_total)
    print("Player 2:",player2_total)
    
# decide who goes first.
def first_turn():
    if random.randint(0,1) == 0:
        return "Player 2"
    else:
        return "Player 1"

# banking stats.
def bank_stats():
	p1_avg = player1_total / p1_bank_count
	p2_avg = player2_total / p2_bank_count
	print("\nPlayer 1 banked {} times, averageing {} per bank." .format(p1_bank_count,p1_avg))
	print("Player 2 banked {} times, averageing {} per bank." .format(p2_bank_count,p2_avg))

    
'''
GAMEPLAY
'''

while True:
    print("\nWelcome to Farkle! The first person to bank over 5,000 points wins the game.\nYou can score on a single die or a combination of die:\n\nSingle Scoring Dice:\n'FIVE' = 50\n'ONE' = 100\n\nCombination Scoring Dice:\nx3 of the same dice = (number on dice * 100) [example: x3 of 3 = 300]\nx4 of any number = 1,000\nx5 of any number = 2,000\nx6 of any number = 3,000\n1-6 straight = 1,500\nthree pairs = 1,500\nx4 of any number with a pair = 1,500\ntwo triplets = 2,500")
    play_game = str(input("\nAre you ready to play...Y / N ? ").upper())

        
    if play_game == "Y":
        game_on = True
    else:
        game_on = False
    
    player1_total = 0
    player2_total = 0
    rolling_total = 0 
    p1_bank_count = 0
    p2_bank_count = 0
	    
    turn = first_turn()
    print("\n"+turn+" will go first.")
       
    while game_on:
        
        while True:

            if turn == "Player 1":
                # player 1's turn
                display_board(player1_total,player2_total)
                p1_holding_count = 6
                p1_rolling_total= 0
                p1_rolls = True

                # player 1 rolls
                while p1_rolls:
                    dice = Dice()
                    holds = Holds()
                    print("\n< Player 1 >")
                    print("\nRolling Total:",p1_rolling_total)
                    roll = dice.rolled(p1_holding_count)
                    holding = holds.hold_die(roll)
                    p1_holding_count -= len(holding)
                    rolled_score = scoring_rolls(holding)
                    if rolled_score == 0:
                        print("\nBUST! - You have not held any or only scoring dice!")
                        p1_rolls = False
                        turn = "Player 2"
                        break
                    p1_rolling_total += rolled_score
                    if p1_holding_count == 0:
                        p1_holding_count = 6
                    print("\nThe current rolling total is: ",p1_rolling_total)
                    decision = str(input("Press 'Enter' to continue rolling or type 'Bank' to bank the above amount... ").capitalize())
                    if decision == "Bank":
                        player1_total += p1_rolling_total
                        p1_bank_count += 1
                        if player1_total >= 5000:
                            print("\n\nPlayer 1 is the winner!!!")
                            display_board(player1_total,player2_total)
                            bank_stats()
                            turn = ""
                            break
                        else:
                            p1_rolls = False
                            turn = "Player 2"
                            break
                    else:
                        continue

            elif turn == "Player 2":
                # player 2's turn
                display_board(player1_total,player2_total)
                p2_holding_count = 6
                p2_rolling_total= 0
                p2_rolls = True

                # player 2 rolls
                while p2_rolls:
                    dice = Dice()
                    holds = Holds()
                    print("\n< Player 2 >")
                    print("\nRolling Total:",p2_rolling_total)
                    roll = dice.rolled(p2_holding_count)
                    holding = holds.hold_die(roll)
                    p2_holding_count -= len(holding)
                    rolled_score = scoring_rolls(holding)
                    if rolled_score == 0:
                        print("\nBUST! - You have not held any or only scoring dice!")
                        p2_rolls = False
                        turn = "Player 1"
                        break
                    p2_rolling_total += rolled_score
                    if p2_holding_count == 0:
                        p2_holding_count = 6
                    print("\nThe current rolling total is: ",p2_rolling_total)
                    decision = str(input("Press 'Enter' to continue rolling or 'Bank' to bank the above amount... ").capitalize())
                    if decision == "Bank":
                        player2_total += p2_rolling_total
                        p2_bank_count += 1
                        if player2_total >= 5000:
                            print("\n\nPlayer 2 is the winner!!!")
                            display_board(player1_total,player2_total)
                            bank_stats()
                            turn = ""
                            break
                        else:
                            p2_rolls = False
                            turn = "Player 1"
                            break
                    else:
                        continue
                        
            else:
                game_on = False
                break
        
    if not replay():
        break

