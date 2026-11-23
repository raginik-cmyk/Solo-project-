from psychopy import visual, core, event, gui
import random
import csv
import os

# ==========================================
# PARTICIPANT INFORMATION
# ==========================================

info = {
    "Participant ID": ""
}

dialog = gui.DlgFromDict(
    info,
    title="Serial Position Effect Experiment"
)

if not dialog.OK:
    core.quit()

participant = info["Participant ID"]

# ==========================================
# WINDOW
# ==========================================

win = visual.Window(
    size=(1200, 800),
    fullscr=False,
    color="black",
    units="height"
)

# ==========================================
# EXPERIMENT SETTINGS
# ==========================================

NUM_LISTS = 8
WORDS_PER_LIST = 12

WORD_DURATION = 1.5
RECALL_DURATION = 45

# ==========================================
# WORD DATABASE
# ==========================================

word_pool = [
    "APPLE", "CHAIR", "RIVER", "TABLE",
    "MANGO", "CLOCK", "BREAD", "CLOUD",
    "HOUSE", "PLANT", "OCEAN", "PENCIL",
    "FLOWER", "WINDOW", "BOTTLE", "GARDEN",
    "MIRROR", "ORANGE", "SCHOOL", "POCKET",
    "CAMERA", "MONKEY", "LADDER", "MARKET",
    "CASTLE", "BANANA", "FOREST", "PILLOW",
    "BASKET", "CANDLE", "TICKET", "JACKET",
    "BUTTON", "CARPET", "DOCTOR", "PLANET",
    "HAMMER", "SILVER", "GUITAR", "BUTTER",
    "PAPER", "CIRCLE", "BRIDGE", "POTATO",
    "BIRD", "MOUNTAIN", "LANTERN", "CUP",
    "BICYCLE", "SANDWICH", "CAMEL", "RIBBON",
    "LION", "SHADOW", "PUMPKIN", "TRAIN",
    "BELL", "SPOON", "DIAMOND", "PILOT",
    "ROCKET", "JUNGLE", "COOKIE", "TOWER",
    "FINGER", "LAPTOP", "WALLET", "LEMON",
    "PANDA", "SNAKE", "CROWN", "GLOBE",
    "BOTTLE", "DRUM", "PIZZA", "RABBIT",
    "PARK", "SHIRT", "CAMERA", "SHEEP",
    "FORK", "GRAPES", "HORSE", "KEY",
    "DESERT", "CUPBOARD", "COW", "STONE",
    "KETTLE", "SHOES", "TIGER", "BAG",
    "SPOON", "BROOM", "STAR", "MOUSE",
    "PAPER", "FAN", "BOAT", "FROG",
    "RING", "SCALE", "MILK", "BOOK",
    "BRUSH", "SALT", "RADIO", "CORN",
    "TRUCK", "GLASS", "BEE", "CUSHION",
    "DOOR", "PEAR", "CUP", "SOCK"
]

# Remove duplicates
word_pool = list(set(word_pool))

# ==========================================
# VISUAL STIMULI
# ==========================================

word_stim = visual.TextStim(
    win,
    text="",
    color="white",
    height=0.08
)

fixation = visual.TextStim(
    win,
    text="+",
    color="white",
    height=0.08
)

instruction = visual.TextStim(
    win,
    text="""
SERIAL POSITION EFFECT

You will see a series of 12 words.

Each word will appear individually
on the screen.

Try to remember as many words as possible.

After all the words have been presented,
you will have 45 seconds to type the words
you remember.

You do not need to remember the order.

Press SPACE to begin.
""",
    color="white",
    height=0.035,
    wrapWidth=1.2
)

# ==========================================
# RECALL SCREEN
# ==========================================

recall_instruction = visual.TextStim(
    win,
    text="Type all the words you remember.\nPress ENTER when finished.",
    color="white",
    pos=(0, 0.25),
    height=0.045
)

typed_text = visual.TextStim(
    win,
    text="",
    color="yellow",
    pos=(0, 0),
    height=0.04,
    wrapWidth=1.2
)

timer_text = visual.TextStim(
    win,
    text="",
    color="white",
    pos=(0, -0.35),
    height=0.04
)

# ==========================================
# WORD LIST GENERATION
# ==========================================

all_words = random.sample(
    word_pool,
    NUM_LISTS * WORDS_PER_LIST
)

word_lists = []

for i in range(NUM_LISTS):

    start = i * WORDS_PER_LIST

    word_list = all_words[
        start:start + WORDS_PER_LIST
    ]

    word_lists.append(word_list)

# ==========================================
# RECALL FUNCTION
# ==========================================

def collect_recall():

    response = ""

    recall_clock = core.Clock()

    while recall_clock.getTime() < RECALL_DURATION:

        remaining = int(
            RECALL_DURATION - recall_clock.getTime()
        )

        recall_instruction.draw()

        typed_text.text = response
        typed_text.draw()

        timer_text.text = "Time remaining: " + str(remaining)
        timer_text.draw()

        win.flip()

        keys = event.getKeys()

        for key in keys:

            if key == "return":
                return response

            elif key == "backspace":
                response = response[:-1]

            elif key == "space":
                response += " "

            elif key == "escape":
                win.close()
                core.quit()

            elif len(key) == 1 and key.isalpha():
                response += key.upper()

    return response


# ==========================================
# START EXPERIMENT
# ==========================================

instruction.draw()
win.flip()

event.waitKeys(keyList=["space"])

results = []

recall_results = []

# ==========================================
# MAIN EXPERIMENT
# ==========================================

for list_number, word_list in enumerate(word_lists, start=1):

    # Fixation screen

    fixation.draw()
    win.flip()
    core.wait(1)

    # Present words individually

    for position, word in enumerate(word_list, start=1):

        word_stim.text = word
        word_stim.draw()

        win.flip()

        core.wait(WORD_DURATION)

        # Blank screen between words

        win.flip()
        core.wait(0.3)

    # ======================================
    # RECALL PHASE
    # ======================================

    recall_instruction.draw()
    win.flip()

    recall_response = collect_recall()

    # ======================================
    # PROCESS RECALL
    # ======================================

    recalled_words = [
        word.strip().upper()
        for word in recall_response.split()
    ]

    recalled_words = list(set(recalled_words))

    correct_recalled = [
        word for word in recalled_words
        if word in word_list
    ]

    recall_results.append([
        participant,
        list_number,
        " ".join(word_list),
        " ".join(recalled_words),
        len(correct_recalled)
    ])

    # ======================================
    # SAVE WORD-LEVEL DATA
    # ======================================

    for position, word in enumerate(word_list, start=1):

        recalled = int(word in correct_recalled)

        results.append([
            participant,
            list_number,
            position,
            word,
            recalled
        ])

    # Break between lists

    break_text = visual.TextStim(
        win,
        text="Next round is starting.\n\nPress SPACE to continue.",
        color="white",
        height=0.05
    )

    break_text.draw()
    win.flip()

    event.waitKeys(keyList=["space"])


# ==========================================
# SAVE DATA
# ==========================================

os.makedirs("Serial_Position_Data", exist_ok=True)

filename = os.path.join(
    "Serial_Position_Data",
    f"Participant_{participant}_SerialPosition.csv"
)

with open(filename, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Participant",
        "List",
        "Serial_Position",
        "Word",
        "Recalled"
    ])

    writer.writerows(results)


# ==========================================
# SAVE RECALL SUMMARY
# ==========================================

summary_filename = os.path.join(
    "Serial_Position_Data",
    f"Participant_{participant}_RecallSummary.csv"
)

with open(summary_filename, "w", newline="") as file:

    writer = csv.writer(file)

    writer.writerow([
        "Participant",
        "List",
        "Presented_Words",
        "Recalled_Words",
        "Correct_Recall_Count"
    ])

    writer.writerows(recall_results)


# ==========================================
# END SCREEN
# ==========================================

end_text = visual.TextStim(
    win,
    text="""
EXPERIMENT COMPLETED!

Thank you for participating.

Your responses have been saved.

Press SPACE to exit.
""",
    color="white",
    height=0.05
)

end_text.draw()
win.flip()

event.waitKeys(keyList=["space"])

win.close()
core.quit()