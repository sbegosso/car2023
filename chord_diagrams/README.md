Directions to use Chord Diagarams Code.

1. Create a csv file listing out all the entities in the first column. Do not add a title to this column. Pay attention to the order to which you list the entities. Name this file 'index.csv'. (An example 'index.csv' file has been provided).
2. Next create a new csv file with three columns named 'Source', 'Target', and 'Strength'. For each row of the column, input the source node as a number. The number corresponds with the entities index (which order it is listed) in the 'index.csv'. Then, input the target node for the chord under the 'Target' column (as a number again), and finally input the strength of the chord under the 'Strength' column. Start with inputing '100' for the strength of each chord before adjusting later. Make as many of these rows as you would like chords. Name this file 'input.csv'.
3. Copy the code from 'holoviews_chord.py' to a new python file in a code editor that is connected to GitHub like Jupyter Notebook. Name it something appropriate.
4. Add the 'index.csv', 'input.csv', and 'holoviews_chord.py' files to the same folder.
5. Run the code, then push it to GitHub using the 'git add <file name>', 'git commit -m"adding <file name>"', and 'git push' commands (in that order).
6. Using GitHub's pages feature, publish the page as a .html file publicly.
