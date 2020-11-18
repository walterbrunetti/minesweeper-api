# minesweeper-api

### Local setup:

* python3 -m venv minesweeper-api
* cd minesweeper-api
* source bin/activate
* git clone git@github.com:walterbrunetti/minesweeper-api.git
* cd minesweeper-api
* pip install -r requirements.txt
* cd minesweeper_api
* python manage.py test

### Run terminal-based version
```python engine/minesweeper_engine_terminal_based.py```

### Run web-based version
* python manage.py runserver
* Go to game home page http://127.0.0.1:8000/home and follow instructions there


### How the game engine works
* Create a new board with given number of rows, number of columns and number of mines
* Create it after the first cell is selected to avoid placing mines on it or adjacent cells
* For each mined cell, add 1 to the quantity of adjacent cells
* When a cell is uncovered, if it's a mine the game ends
* Otherwise, uncovered cell displays a number indicating the quantity of mines adjacent to it
* If it's a blank cell (with number 0), uncover all the adjacent cells
* Repeat the process for each blank cell uncovered
