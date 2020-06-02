# Moriarty
Moriarty is a language meant to teach people how to program in an interactive way.

## Introduction

Hello Detective,
I come to you with unbearable news.
The president's son has been kidnapped and his whereabouts are unknown.
We suspect the crime family Moriarty was in charge of the kidnapping, but we don’t know for sure.
That’s why I came to you, we need your help locating the Moriarty family so we can get to the president’s son. We need your coding abilities.

Your mission, if you choose to accept it, starts now.
 
 ## Index

## Code Example

    player jugadorUno;
	

## Game Specific

You will need the following knowledge to get to the location of the Moriarty family.

### Stating a player
At the beginning of the file, state your player’s name as the following:

    player player_name;

where player_name is your name without spaces.

### Moving and Jumping
Your player operates on a map, you can move and rotate by calling the following functions with your player name.

    move(player_name);
    rotate(player_name);

Your player starts by facing north, and it can only move one step forward at a time.

There will be obstacles along the way, to surpass them you must jump over them by calling the function jump with your player name.

    jump(player_name);

### Enemies
You might encounter enemies along the way agent, that why we have provided you with a gun. 
To shoot a gun you must call the function 'shoot' with your player name:

    shoot(player_name);

But be careful, you can only shoot towards the direction you're facing, and you must be sure your gun is loaded.
To check if your gun is loaded, you must call the following function:

    gun_loaded?(player_name);
If your gun isn't loaded, you can load it by calling:

    reload_gun(player_name);
But be careful, you can run out of ammo and still have enemies near, be sure not to miss.
Enemies can be found anywhere on the map. To check if an enemy is facing you, call the following:

    enemy?(player_name);

Each one of this `special functions` returns a `boolean` value, stating whether or not the action could be completed.

### Speaking
If your player requires in any way to speak, you must do so like the following:

    speak(player_name, "The thing you wish to speak");
  or if you want to speak the answer of an equation:
  

    var eq : int = 40 / 4;
    speak(player_name, eq);

## Basics

To do all that, you will need to solve equations using your coding abilities. For that we provide you with the following.

### Variables
There are three possible types of variables: integers, booleans and strings. It is also possible to declare one-dimension arrays.

    var i : int = 1;
    var b : bool;
    var s : string = "this is a string";
    
    var i_array[10] : int;
    var b_array[2] : bool = [true, false];
    var s_array[1] : string;
    s_array[0] = "another string";

### Expressions
To complete certain tasks, and move your player, and use your ammo efficiently against your enemies, you must be able to complete certain mathematical expressions. The following expressions are valid:
|Operation||
|--|--|
|Sum | + 
|Subtraction | - 
|Multiplication | *
|Division | /
|Relop | >, <, >=, <=, ==, !=
|Logical | and, or
|Not | not

### Conditionals
You can state whether or not to do something by making use of the conditionals.

    # In here we check if an enemy is in front of the player
    if (enemy?(player_name) {
	    # If they are, we shoot
	    shoot(player_name);
	} else {
		# If they are not, we move forward
		move(player_name);
	}

### Loops
You can also repeat an action over and over again with loops.

    var count : int = 0;
    # If our player is able to move
    loop(move(player_name)) {
	    # We count the steps
	    count = count + 1;
	}
	# If not, we check out surroundings
	var rotator : int = 4;
	loop(rotator >= 0) {
		if (not enemy?(player_one)) {
			rotate(player_one);
		}
		rotator = rotator - 1;
	}
 
### Function Declaration
It is also possible to declare functions. It is very important to remember they must be before the `main` function. The functions can be void or can have a return type of int, string or bool. They can receive any number of parameters, including whole arrays.

    # In here we are going to create a function
    # that automatically jumps if there is an obstacle
    # and speaks saying they overcame an obstacle.
    function jump_obstacle() : void {
	    jump(player_name);
	    speak(player_name, "I jumped over an obstacle");
    }
    #
    # And to call the function we place it on the main()
    main() {
	    var player_can_move : bool = move(player_name);
	    var enemy_near : bool = enemy?(player_name);
	    if (player_can_move and not enemy_near) {
		    jump_obstacle();
		}    
    }


#
## How to install the project

## Commands

Compile and execute code
```./moriarty.sh [file_path].txt```

Test lexer
```make test_lex```

Test parser
```make test file=[file_path].txt```

Start frontend client
```make run-frontend```
* Before running make sure to `cd front-end && npm install`

Start backend server
```make run-backend```
* Before running make sure to `cd backend && npm install`

## Team
|Ana Paola Treviño |Arturo Torres |
|--|--|
|![ana](https://avatars1.githubusercontent.com/u/23621205?s=460&u=ddb3b6bec101e3a7005d42501bd3e433d6de4c60&v=4&s=200)  |![arturo](https://avatars3.githubusercontent.com/u/12913550?s=460&u=2cab58d3acd094354cdb64907d08e2de27d15b33&v=4&s=200)  |