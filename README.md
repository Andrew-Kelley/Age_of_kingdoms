## Age of Kingdoms
This is a turn-based, text-based strategy game inspired by Age of Empires.

### Potential employers, please read
I started this project before I knew the basics of OOP. In particular, I had
never even heard of information hiding. Right now, player.commands should be
encapsulated (as should player.messages). While I have fixed other issues,
I haven't fixed this yet. Also, I should have made more unit tests. For
lessons I've learned since starting this project, see lessons_learned.txt

### Purpose
Build a major project in Python, one that is significantly more
substantial than anything I've done before. Also, I want to practice
doing some object-oriented programming.

### Game manual
For a description of how to use this program, read manual.txt

### Dependency
This game uses the Python package colorama. If you don't want to install that
package for some reason, then if you are using macOS or Linux, then just
open the file colors.py (in a text editor) and delete these two lines:

- from colorama import init
- init()

### Initially limiting the scope
I intend to implement the most essential features first, leaving some of the other
features for later, in case I have the time at some point. Here are some major
features not yet implemented that I intend to get to:
 - the ability to attack other players (This feature is absolutely essential.)
 - a random map generator
 - an AI
 - the ability to play over a network
