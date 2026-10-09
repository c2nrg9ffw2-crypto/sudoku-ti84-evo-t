# Sudoku for the TI-84 Evo-T

**Sudoku** for the **TI-84 Evo-T** graphing calculator, written in Python.

> **Made with AI:** this game and this README were created with the help of AI (Claude by Anthropic).
> Everything was tested on a real TI-84 Evo-T.

## Features

- 3 levels: **Easy**, **Medium** and **Hard**
- Every puzzle has **exactly one solution**
- Puzzles are mixed every game (numbers, rows and columns), so they look different each time
- Your numbers are **blue**, and turn **red** if the same number is twice in a row, column or box
- The black starting numbers can't be changed by mistake
- Solved puzzles per level stay saved after you quit

## What you need

- A **TI-84 Evo-T** calculator
- A USB cable to connect it to your computer
- **Google Chrome** or **Microsoft Edge** (Safari and Firefox do not work with the TI tool)
- The file [`sudoku.py`](sudoku.py) from this repo

## Setup

1. Download [`sudoku.py`](sudoku.py) to your computer.
2. Connect the calculator to your computer with the USB cable.
   Leave the calculator on the **home screen**.
3. Open **https://connectevo.ti.com** in **Chrome** or **Edge**.
4. Connect to your calculator in the page and allow access when the browser asks.
5. Drag `sudoku.py` onto the page to send it to the calculator.
6. **Choose RAM** to play right away.
   The Python app on the Evo-T only shows files that are in RAM.
   (Want to keep the game safe? See [Don't lose the game](#dont-lose-the-game).)

> **Already sent it to Archive?** On the **home screen** (not in the Python app) press **2nd → mem → Mem Management**,
> find **SUDOKU** and press **enter**. The `*` in front of the name disappears, which means
> it is now in RAM.

## Start the game

1. Open the **Python** app on the calculator.
2. Choose **SUDOKU** and run it.
3. Choose **Easy**, **Medium** or **Hard** with ▲ ▼ and press **enter**.

## Don't lose the game

The Evo-T **deletes RAM** when it stays turned off for a while.
A normal turn-off is fine, but after some time the game is gone.

**Best way:**

1. Keep the game in **Archive**. Archive is never deleted.
2. Go to the **home screen**. If you are in the Python app, leave it with **2nd → quit**
   (quit is above the **mode** key). In the Python app, **2nd → mem** does nothing.
3. Press **2nd → mem** (mem is above the **+** key) and choose **2: Mem Management**.
4. Choose the list with Python programs (or **All**).
5. Find **SUDOKU** and press **enter**. The `*` disappears, which means the game is now in RAM.
6. Open the **Python** app and play.

Programs can't move files between Archive and RAM by themselves, so this step can't be automatic.
The solved list **SUDOK** is in RAM too, so it can be deleted the same way.

## Keys

| Key | What it does |
|---|---|
| ◀ ▶ ▲ ▼ | Move the yellow frame |
| 1 – 9 | Write that number |
| enter | Count up: 1 → 2 → … → 9 → empty |
| del or 0 | Erase the number |
| clear | Quit |

## Rules

- Fill every empty square with a number from **1 to 9**.
- Each **row**, each **column** and each **3 × 3 box** must have every number **once**.
- When all squares are filled and nothing is red, the puzzle is **solved**.

## Levels

| Level | Starting numbers |
|---|---|
| Easy | about 40 |
| Medium | about 32 |
| Hard | about 26 |

## Solved puzzles

The number of solved puzzles per level is saved in a calculator list called **SUDOK**
(Easy, Medium, Hard), so it stays after you quit. The start screen shows them.

- To reset them, delete the list **SUDOK** in **2nd → mem → Mem Management** (on the home screen).
- A calculator reset (RAM clear) also resets them.

## Good to know

- Keep `sudoku.py` on your computer too, so you can always send it again.
- Made for the TI-84 Evo-T. Other TI-84 models are not tested.
