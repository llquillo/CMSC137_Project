# CMSC 137: Data Communication and Networking Project Documentation


## Group Members:
* John Russel M. Garcia  
* Lois Jane L. Quillo


## Description of the Game:
```
  A 1-2-3 Pass Card game where the objective of the game is for a player to get all four (4) matching cards in order to win. The user interface will only be a command-line interface/text-based. 

  The game consists of a Server and Client python files. The game will start once 3 or more clients (players) are connected to the running server. The client and server will then communicate using the network. 

  The game will end once the server confirms that one player has four matching cards.
```


## Programming Language to be used:
The programming language used in the project is Python.


## External libraries to be used, if applicable:
Not applicable.


## Integrated Development Environments (IDEs) to be used:
The IDE used in this project is PyCharm which is the recommended IDE for creating Python applications.


## Link of Github repository:
<https://github.com/llquillo/CMSC137_Project>

## Protocol:
### Data Flow Diagram:
	

### Structure of the data to be exchanged:
* The server broadcasts the initial randomized cards to clients (socket.send).
* The client then shows the cards to the respective player and asks for user input.
* The user input will be converted to a bitstream (through pickle) and will be sent back to the server using the network.
* The server will receive the bitstream and will convert it back to object (pickle_loads).
* The server will update the state and will send it back to clients (socket.sendall).

