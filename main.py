"""
Main Script


Revision History

- 7/2 -   Sean -  Minor edit for directory structure


To Do

- Backfill revision history

"""

from CobraBankApp import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
