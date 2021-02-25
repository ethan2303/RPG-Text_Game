import cmd
import textwrap
import sys
import os
import time
import random
screen_width = 100

################
# Player Setup #
################
class player:
    def __init__(self):
        self.name = ''
        self.feeling = ''
        self.astrological = ''
        self.position = 'ground'
        self.won = False
        self.solves = 0
player1 = player()

#Sets up constant variables
DESCRIPTION = 'description'
INFO = 'info'
PUZZLE = 'puzzle'
SOLVED = False
SIDE_UP = 'up', 'forward'
SIDE_DOWN = 'down', 'back'
SIDE_LEFT = 'left',
SIDE_RIGHT = 'right',

room_solved = {'top': False, 'north': False, 'ground': False, 'east': False, 'west': False, 'south': False,}

cube = {
    'top': {
        DESCRIPTION: "You have made it to the top of the cube.",
        INFO: "off in the distance is a sign. \non it is a riddle.\n",
        PUZZLE: "it reads, one word in this sentence is misspelled. What word is it?'",
        SOLVED: "misspelled",
        SIDE_UP: 'north',
        SIDE_DOWN: 'south',
        SIDE_LEFT: 'east',
        SIDE_RIGHT: 'west',
    },
    'north': {
        DESCRIPTION: "You find yourself in a frigid artic valley.\nA campfire glows brightly in a nearby cave.",
        INFO: "You now stand face-to-face with an old man.",
        PUZZLE: "he asks you one simple question. \nWhat Has Four Fingers And A Thumb, But Is Not Living?'", 
        SOLVED: "a glove",
        SIDE_UP: 'top',
        SIDE_DOWN: 'ground',
        SIDE_LEFT: 'west',
        SIDE_RIGHT: 'east',
    },
    'ground': {
        DESCRIPTION: "You find yourself in a rather pretty, generic grassy field.\nSomething feels amiss, as if this the core of the world.",
        INFO: "A rather large, though easily overlookable golden key\nstands vertical in the field.\nHow odd.",
        PUZZLE: "The key stands within respectively sized keyhole obscured\nby dirt and grass.  It doesn't seem to turn.",
        SOLVED: False, #Will work after you solve all other puzzles.
        SIDE_UP: 'north',
        SIDE_DOWN: 'south',
        SIDE_LEFT: 'west',
        SIDE_RIGHT: 'east',
    },
    'east': {
        DESCRIPTION: "ah yes a very welcoming dark black wall with sporadic letters on it.",
        INFO: "You suddenly see the letters on the wall start to rearrange, \nah yes a riddle.",
        PUZZLE: "I Have Keys But No Locks. I Have A Space But No Room. You Can Enter, But Can’t Go Outside. What Am I?",
        SOLVED: "a keyboard",
        SIDE_UP: 'north',
        SIDE_DOWN: 'south',
        SIDE_LEFT: 'ground',
        SIDE_RIGHT: 'top',
    },
    'west': {
        DESCRIPTION: 'hmm, very interesting.\na wall of water, i wonder what this riddle is',
        INFO: 'Splash! a bottle with a note in it flys out of the water and \nhits you in the face. I wonder what it could say.',
        PUZZLE: "What Gets Wet When Drying?'",
        SOLVED: "a towel",
        SIDE_UP: 'north',
        SIDE_DOWN: 'south',
        SIDE_LEFT: 'top',
        SIDE_RIGHT: 'ground',
    },
    'south': {
        DESCRIPTION: "you are greeted by a nice starry night .",
        INFO: "as you gaze at the stars they form 12 symbols.",
        PUZZLE: "Each of them are an unique symbol, though all are familar to you.\nWhich symbol do you choose by \nHint: You already answered this in the beginning?",
        SOLVED: "",# your astrological sign.
        SIDE_UP: 'ground',
        SIDE_DOWN: 'top',
        SIDE_LEFT: 'west',
        SIDE_RIGHT: 'east',
    }
}


################
# Title Screen #
################
def title_screen_options():
    #Allows the player to select the menu options, case-insensitive.
    option = input("> ")
    if option.lower() == ("play"):
        setup_game()
    elif option.lower() == ("quit"):
        sys.exit()
    elif option.lower() == ("help"):
        help_menu()
    while option.lower() not in ['play', 'help', 'quit']:
        print("Invalid command, please try again.")
        option = input("> ")
        if option.lower() == ("play"):
            setup_game()
        elif option.lower() == ("quit"):
            sys.exit()
        elif option.lower() == ("help"):
            help_menu()

def title_screen():
    #Prints the title.
    print('#' * 45)
    print('#            Welcome to THE BOX             #')
    print('#' * 45)
    print("                 .: Play :.                  ")
    print("                 .: Help :.                  ")
    print("                 .: Quit :.                  ")
    title_screen_options()


#############
# Help Menu #
#############
def help_menu():
    print("Type a command such as 'move' then 'left'")
    print("to nagivate the map of the cube puzzle.\n")
    print("Inputs such as 'look' or 'examine' will")
    print("let you interact with puzzles in rooms.\n")
    print("Puzzles will require various input and ")
    print("possibly answers from outside knowledge.\n")
    print("Please ensure to type in lowercase for ease.\n")
    print('#' * 45)
    print("\n")
    print('#' * 45)
    print("    Please select an option to continue.     ")
    print('#' * 45)
    print("                 .: Play :.                  ")
    print("                 .: Help :.                  ")
    print("                 .: Quit :.                  ")
    title_screen_options()


#################
# Game Handling #
#################
quitgame = 'quit'

def print_location():
    #Makes a pretty picture when printed and prints the cube floor information for the player.
    print('\n' + ('#' * (4 +len(player1.position))))
    print('# ' + player1.position.upper() + ' #')
    print('#' * (4 +len(player1.position)))
    print('\n' + (cube[player1.position][DESCRIPTION]))

def prompt():
    if player1.solves == 5:
        print("Something in the world seems to have changed. Hmm...")
    print("\n~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print("What would you like to do?")
    action = input("> ")
    acceptable_actions = ['move', 'go', 'travel', 'walk', 'quit', 'inspect', 'examine', 'look', 'search']
    #Forces the player to write an acceptable sign, as this is essential to solving a puzzle later.
    while action.lower() not in acceptable_actions:
        print("Unknown action command, please try again.\n")
        action = input("> ")
    if action.lower() == quitgame:
        sys.exit()
    elif action.lower() in ['move', 'go', 'travel', 'walk']:
        move(action.lower())
    elif action.lower() in ['inspect', 'examine', 'look', 'search']:
        examine()

def move(myAction):
    askString = "Where would you like to "+myAction+" to?\n> "
    destination = input(askString)
    if destination == 'forward':
        move_dest = cube[player1.position][SIDE_UP] #if you are on ground, should say north
        move_player(move_dest)
    elif destination == 'left':
        move_dest = cube[player1.position][SIDE_LEFT]
        move_player(move_dest)
    elif destination == 'right':
        move_dest = cube[player1.position][SIDE_RIGHT]
        move_player(move_dest)
    elif destination == 'back':
        move_dest = cube[player1.position][SIDE_DOWN]
        move_player(move_dest)
    else:
        print("Invalid direction command, try using forward, back, left, or right.\n")
        move(myAction)

def move_player(move_dest):
    print("\nYou have moved to the " + move_dest + ".")
    player1.position = move_dest
    print_location()

def examine():
    if room_solved[player1.position] == False:
        print('\n' + (cube[player1.position][INFO]))
        print((cube[player1.position][PUZZLE]))
        puzzle_answer = input("> ")
        checkpuzzle(puzzle_answer)
    else:
        print("There is nothing new for you to see here.")

def checkpuzzle(puzzle_answer):
    if player1.position == 'ground':
        if player1.solves >= 5:
            endspeech = ("Without you having done anything, the key begins to rotate.\nIt begins to rain.\nAll of the sides of the box begin to crumble inwards.\nLight begins to shine through the cracks in the walls.\nA blinding flash of light hits you.\nYou have escaped!")
            for character in endspeech:
                sys.stdout.write(character)
                sys.stdout.flush()
                time.sleep(0.05)
            print("\nCONGRATULATIONS!")
            title_screen()
        else:
            print("Nothing seems to happen still...")
    elif player1.position == 'south':
        if puzzle_answer == (player1.astrological):
            room_solved[player1.position] = True
            player1.solves += 1
            print("You have solved the puzzle. Onwards!")
            print("\nPuzzles solved: " + str(player1.solves))
        else:
            print("Wrong answer! Try again.\n~~~~~~~~~~~~~~~~~~~~~~~~~~")
            examine()
    else:
        if puzzle_answer == (cube[player1.position][SOLVED]):
            room_solved[player1.position] = True
            player1.solves += 1
            print("You have solved the puzzle. Onwards!")
            print("\nPuzzles solved: " + str(player1.solves))
        else:
            print("Wrong answer! Try again.\n~~~~~~~~~~~~~~~~~~~~~~~~~~")
            examine()

def main_game_loop():
    total_puzzles = 6
    while player1.won is False:
        #print_location()
        prompt()


################
# Execute Game #
################
def setup_game():
    #Clears the terminal for the game to start.
    #os.system('clear')

    #QUESTION NAME: Obtains the player's name.
    question1 = "Hello there, what is your name?\n"
    for character in question1:
        #This will occur throughout the intro code.  It allows the string to be typed gradually - like a typerwriter effect.
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_name = input("> ")
    player1.name = player_name

    #QUESTION FEELING: Obtains the player's feeling.
    question2 = "My dear friend " + player1.name + ", how are you feeling?\n"
    for character in question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    feeling = input("> ")
    player1.feeling = feeling.lower()

    #Creates the adjective vocabulary for the player's feeling.
    good_adj = ['good', 'great', 'rohit', 'happy', 'aight', 'understanding', 'great', 'alright', 'calm', 'confident', 'not bad', 'courageous', 'peaceful', 'reliable', 'joyous', 'energetic', 'at', 'ease', 'easy', 'lucky', 'k', 'comfortable', 'amazed', 'fortunate', 'optimistic', 'pleased', 'free', 'delighted', 'swag', 'encouraged', 'ok', 'overjoyed', 'impulsive', 'clever', 'interested', 'gleeful', 'free', 'surprised', 'satisfied', 'thankful', 'frisky', 'content', 'receptive', 'important', 'animated', 'quiet', 'okay', 'festive', 'spirited', 'certain', 'kind', 'ecstatic', 'thrilled', 'relaxed', 'satisfied', 'wonderful', 'serene', 'glad', 'free', 'and', 'easy', 'cheerful', 'bright', 'sunny', 'blessed', 'merry', 'reassured', 'elated', '1738', 'love', 'interested', 'positive', 'strong', 'loving']
    hmm_adj = ['idk', 'concerned', 'lakshya', 'eager', 'impulsive', 'considerate', 'affected', 'keen', 'free', 'affectionate', 'fascinated', 'earnest', 'sure', 'sensitive', 'intrigued', 'intent', 'certain', 'tender', 'absorbed', 'anxious', 'rebellious', 'devoted', 'inquisitive', 'inspired', 'unique', 'attracted', 'nosy', 'determined', 'dynamic', 'passionate', 'snoopy', 'excited', 'tenacious', 'admiration', 'engrossed', 'enthusiastic', 'hardy', 'warm', 'curious', 'bold', 'secure', 'touched', 'brave', 'sympathy', 'daring', 'close', 'challenged', 'loved', 'optimistic', 'comforted', 're', 'enforced', 'drawn', 'toward', 'confident', 'hopeful', 'difficult']
    bad_adj = ['bad', 'meh', 'sad', 'hungry', 'unpleasant', 'feelings', 'angry', 'depressed', 'confused', 'helpless', 'irritated', 'lousy', 'upset', 'incapable', 'enraged', 'disappointed', 'doubtful', 'alone', 'hostile', 'discouraged', 'uncertain', 'paralyzed', 'insulting', 'ashamed', 'indecisive', 'fatigued', 'sore', 'powerless', 'perplexed', 'useless', 'annoyed', 'diminished', 'embarrassed', 'inferior', 'upset', 'guilty', 'hesitant', 'vulnerable', 'hateful', 'dissatisfied', 'shy', 'empty', 'unpleasant', 'miserable', 'stupefied', 'forced', 'offensive', 'detestable', 'disillusioned', 'hesitant', 'bitter', 'repugnant', 'unbelieving', 'despair', 'aggressive', 'despicable', 'skeptical', 'frustrated', 'resentful', 'disgusting', 'distrustful', 'distressed', 'inflamed', 'abominable', 'misgiving', 'woeful', 'provoked', 'terrible', 'lost', 'pathetic', 'incensed', 'in', 'despair', 'unsure', 'tragic', 'infuriated', 'sulky', 'uneasy', 'cross', 'bad', 'pessimistic', 'dominated', 'worked', 'up', 'a', 'sense', 'of', 'loss', 'tense', 'boiling', 'fuming', 'indignant', 'indifferent', 'afraid', 'hurt', 'sad', 'insensitive', 'fearful', 'crushed', 'tearful', 'dull', 'terrified', 'tormented', 'sorrowful', 'nonchalant', 'suspicious', 'deprived', 'pained', 'neutral', 'anxious', 'pained', 'grief', 'reserved', 'alarmed', 'tortured', 'anguish', 'weary', 'panic', 'dejected', 'desolate', 'bored', 'nervous', 'rejected', 'desperate', 'preoccupied', 'scared', 'injured', 'pessimistic', 'cold', 'worried', 'offended', 'unhappy', 'disinterested', 'frightened', 'afflicted', 'lonely', 'lifeless', 'timid', 'aching', 'grieved', 'shaky', 'victimized', 'mournful', 'restless', 'heartbroken', 'dismayed', 'doubtful', 'agonized', 'threatened', 'appalled', 'cowardly', 'humiliated', 'quaking', 'wronged', 'menaced', 'alienated', 'wary']

    #Identifies what type of feeling the player is having and gives a related-sounding string.
    if player1.feeling in good_adj:
        feeling_string = "I am glad you feel"
    elif player1.feeling in hmm_adj:
        feeling_string = "that is interesting you feel"
    elif player1.feeling in bad_adj:
        feeling_string = "I am sorry to hear you feel"
    else:
        feeling_string = "I do not know what it is like to feel"

    #Combines all the above parts.
    question3 = "Well then, " + player1.name + ", " + feeling_string + " " + player1.feeling + ".\n"
    for character in question3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)

    #QUESTION SIGN: Obtains the player's astrological sign for a later puzzle.
    question4 = "Now tell me, what is your astrological sign?\n"
    for character in question4:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)

    #Prints the astrological sign guide for the player.  Also converts text to be case-insensitive, as with most inputs.
    print("#####################################################")
    print("# Please print the proper name to indicate your sign.")
    print("# ♈ Aries (The Ram)")
    print("# ♉ Taurus (The Bull)")
    print("# ♊ Gemini (The Twins)")
    print("# ♋ Cancer (The Crab)")
    print("# ♌ Leo (The Lion)")
    print("# ♍ Virgo (The Virgin)")
    print("# ♎ Libra (The Scales)")
    print("# ♏ Scorpio (The Scorpion)")
    print("# ♐ Sagittarius (Centaur)")
    print("# ♑ Capricorn (The Goat)")
    print("# ♒ Aquarius (The Water Bearer)")
    print("# ♓ Pisces (The Fish)")
    print("#####################################################")
    astrological = input("> ")
    acceptable_signs = ['aries', 'taurus', 'gemini', 'cancer', 'leo', 'virgo', 'libra', 'scorpio', 'sagittarius', 'capricorn', 'aquarius', 'pisces']
    #Forces the player to write an acceptable sign, as this is essential to solving a puzzle later.  Also stores it in class.

    while astrological.lower() not in acceptable_signs:
        print("That is not an acceptable sign, please try again.")
        astrological = input("> ")
    player1.astrological = astrological.lower()

    #Leads the player into the cube puzzle now!
    speech1 = "Ah, " + player1.astrological + ", how interesting.  Well then.\n"
    speech2 = "It seems this is where we must part, " + player1.name + ".\n"
    speech3 = "How unfortunate.\n"  
    speech4 = "Oh, you don't know where you are?  Well...\n"
    speech5 = "Luckily, I've left you in a little puzzle.  Hopefully you can escape this box.\n"
    speech6 = "Heh. Heh.. Heh...\n"
    for character in speech1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in speech2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in speech3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.1)
    for character in speech4:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in speech5:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in speech6:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.2)
    time.sleep(1)

    #os.system('clear')
    print("################################")
    print("#  Your Puzzle has started...  #")
    print("################################\n")
    print("You find yourself in the center of a strange place.\nSeems like you are trapped in a little box.\n")
    print("Every inside face of the box seems to have a different riddle.\nHow can you get out of this...\n")
    main_game_loop()


title_screen()