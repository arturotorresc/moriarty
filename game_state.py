import random
import json

GAME_STATE_FILE = './backend/game_states/game_state.json'

class GameState:
  # ================ ATTRIBUTES =====================

  # Our Singleton instance
  __instance = None

  @classmethod
  def get_instance(self):
    if GameState.__instance is None:
      GameState()
    return GameState.__instance
  
  # Initializes the first player at (0, 0) and then tries to assign players
  # to in the next (0, x) position
  def initialize_player(self, player_id):
    player_idx, player_exists = self.__find_player(player_id)
    if player_exists:
      return
    if self.__next_player_x >= self.__map[0]:
      raise Exception('Initialized more players than allowed: {}'.format(self.__next_player_x + 1))
    self.__players.append([player_id, [self.__next_player_x, 0]])
    self.__players_direction.append('N')
    # First element is ammo and second element is whether the gun is charged
    self.__ammo.append([len(self.__enemies), True])
    self.__next_player_x += 1
  
  # Attempts to move a player in the direction they are facing
  def move_player(self, player_id):
    player_idx, player_to_move = self.__find_player(player_id)
    if player_to_move is None:
      raise Exception("Tried to move player {} but {} does not exist".format(player_id, player_id))
    
    # Calculating next position
    player_direction = self.__players_direction[player_idx]
    new_position = self.__get_position_in_front(player_to_move[1].copy(), player_direction)

    if self.__out_of_bounds(new_position):
      return False
    # Checking if there are any obstacles or enemies in the way
    if self.__enemy_at_position(new_position)[1] or self.__obstacle_at_position(new_position)[1]:
      return False
    
    self.__players[player_idx][1] = new_position
    # Adding action to action queue
    self.__add_action(['MOVE', player_id, new_position])
    return True
  
  def rotate_player(self, player_id):
    player_idx, player_to_rotate = self.__find_player(player_id)
    if not player_to_rotate:
      raise Exception('Trying to rotate player but {} does not exist'.format(player_id))
    
    direction = self.__players_direction[player_idx]
    if direction == 'N':
      direction = 'W'
    elif direction == 'W':
      direction = 'S'
    elif direction == 'S':
      direction = 'E'
    elif direction == 'E':
      direction = 'N'
    self.__players_direction[player_idx] = direction
    self.__add_action(['ROTATE', player_id, direction])
    return True
  
  def shoot_enemy(self, player_id):
    player_idx, player_shooting = self.__find_player(player_id)
    if not player_shooting:
      raise Exception('Tried to shoot with player but {} does not exist'.format(player_shooting))
    
    # Check if we have ammo
    if self.__ammo[player_idx][0] <= 0:
      return False
    
    # Check if our gun is loaded
    if not self.__ammo[player_idx][1]:
      return False

    # Check if we have an enemy in front of the player
    player_direction = self.__players_direction[player_idx]
    front_position = self.__get_position_in_front(player_shooting[1].copy(), player_direction)
    enemy_pos = self.__enemy_at_position(front_position)
    if not enemy_pos[1]:
      return False
    
    # Shoot the enemy and lose 1 ammo and set reloaded? to False
    del self.__enemies[enemy_pos[0]]
    self.__ammo[player_idx][0] -= 1
    self.__ammo[player_idx][1] = False
    self.__add_action(['SHOOT', player_id, front_position])
    return True
  
  def gun_loaded(self, player_id):
    player_idx, player = self.__find_player(player_id)
    if not player:
      raise Exception('Trying to check if gun is loaded but {} does not exist'.format(player_id))
    if self.__ammo[player_idx][0] > 0 and self.__ammo[player_idx][1]:
      self.__add_action(['GUN_LOADED?', player_id, True])
      return True
    self.__add_action(['GUN_LOADED?', player_id, False])
    return False
  
  def reload_gun(self, player_id):
    player_idx, player = self.__find_player(player_id)
    if not player:
      raise Exception('Trying to reload gun but {} does not exist'.format(player_id))
    if self.__ammo[player_idx][0] > 0:
      self.__add_action(['RELOAD_GUN', player_id, True])
      self.__ammo[player_idx][1] = True
      return True
    return False
  
  def speak(self, player_id, expr):
    self.__add_action(['SPEAK', player_id, expr])
  
  def enemy_in_front(self, player_id):
    player_idx, player = self.__find_player(player_id)
    if not player:
      raise Exception('Trying to check if enemy is in front but {} does not exist'.format(player_id))
    player_direction = self.__players_direction[player_idx]
    front_position = self.__get_position_in_front(player[1].copy(), player_direction)
    if self.__enemy_at_position(front_position):
      self.__add_action(['ENEMY?', player_id, True])
      return True
    self.__add_action(['ENEMY?', player_id, False])
    return False
  
  def jump(self, player_id):
    player_idx, player_to_move = self.__find_player(player_id)
    if not player_to_move:
      raise Exception('Trying to jump obstacle but {} does not exist'.format(player_id))
    
    player_direction = self.__players_direction[player_idx]
    front_position = self.__get_position_in_front(player_to_move[1].copy(), player_direction)
    if self.__obstacle_at_position(front_position):
      jump_position = self.__get_position_in_front(front_position.copy(), player_direction)
      if self.__out_of_bounds(jump_position):
        return False
      self.__players[player_idx][1] = jump_position
      self.__add_action(['JUMP', player_id, jump_position])
      return True
    return False
  
  def write_game_state(self):
    with open(GAME_STATE_FILE, 'w') as outfile:
      data = {
        'map': self.__map,
        'players': self.__players,
        'ammo': self.__ammo,
        'players_direction': self.__players_direction,
        'enemies': self.__enemies,
        'obstacles': self.__obstacles,
        'actions': self.__actions,
        'goal': self.__goal
      }
      json.dump(data, outfile)

  # Print Game internal state
  def print(self):
    print('====== GAME STATE ======')
    print('map dimensions =>')
    print(self.__map)
    print('players =>')
    print(self.__players)
    print('ammo =>')
    print(self.__ammo)
    print('players_direction =>')
    print(self.__players_direction)
    print('enemies =>')
    print(self.__enemies)
    print('obstacles =>')
    print(self.__obstacles)
    print('actions =>')
    print(self.__actions)
    print('goal =>')
    print(self.__goal)
  
  # ================ PRIVATE INTERFACE =====================
  def __init__(self):
    if GameState.__instance is not None:
      raise Exception("GameState is a Singleton! Access the instance through: GameState.get_instance()")
    else:
      GameState.__instance = self
      # Represents the next [x] coordinate in which to instantiate a player
      self.__next_player_x = 0
      with open(GAME_STATE_FILE) as file:
        game_state = json.load(file)
        # Map dimensions (width, height) where width is [x] coord and
        # height is [y] coord
        self.__map = game_state['map']
        # Initializes an empty list of players
        self.__players = game_state['players']
        # Initializes an empty list of player ammo
        self.__ammo = game_state['ammo']
        # Initializes an empty list of where players are facing (N, E, W, S)
        self.__players_direction = game_state['players_direction']
        # Initializes the enemies in the map
        self.__enemies = game_state['enemies']
        # Initializes the obstacles in the map
        self.__obstacles = game_state['obstacles']
        # Initializes an empty list with all the actions to take
        self.__actions = []
        # Initializes the coordiante where the players have to get
        self.__goal = game_state['goal']
  
  def __find_player(self, player_id):
    for idx, player in enumerate(self.__players):
      if player[0] == player_id:
        return (idx, player)
    return (None, None)
  
  def __enemy_at_position(self, position):
    for idx, coord in enumerate(self.__enemies):
      if position[0] == coord[0] and position[1] == coord[1]:
        return (idx, True)
    return (None, False)
  
  def __obstacle_at_position(self, position):
    for idx, coord in enumerate(self.__obstacles):
      if position[0] == coord[0] and position[1] == coord[1]:
        return (idx, True)
    return (None, False)
  
  def __out_of_bounds(self, position):
    if position[0] >= self.__map[0] or position[0] < 0:
      return True
    if position[1] >= self.__map[1] or position[1] < 0:
      return True
    return False
  
  def __get_position_in_front(self, position, direction):
    if direction == 'N':
      position[1] = position[1] + 1
    elif direction == 'W':
      position[0] = position[0] - 1
    elif direction == 'S':
      position[1] = position[1] - 1
    elif direction == 'E':
      position[0] = position[0] + 1
    return position
  
  def __add_action(self, action):
    self.__actions.append(action)
