#!/usr/bin/env python
# coding: utf-8

# In[2]:


import random
import time
import argparse

#Die class that simulates rolling a die

class Die:
    def __init__(self, seed=0):
        random.seed(seed)
    
    def roll(self):
        return random.randint(1, 6)

#Player class that simulates a basic player with a name and score

class Player:
    def __init__(self, name):
        self.name = name
        self.score = 0
    
    def add_to_score(self, points):
        self.score += points
    
    def reset_score(self):
        self.score = 0

#ComputerPlayer class that inherits from Player class and adds computer strategy

class ComputerPlayer(Player):
    def __init__(self, name):
        super().__init__(name)
    
    #Strategy: rolls until score reaches 25 or 100 minus current score
    def decide(self, current_score):
        if current_score < 100:
            return min(25, 100 - current_score)
        return 0

#PlayerFactory class that creates either human or computer players

class PlayerFactory:        
    def create_player(self, player_type, name):
        if player_type == "human":
            return Player(name)
        elif player_type == "computer":
            return ComputerPlayer(name)
        else:
            raise ValueError(f"Unknown player type: {player_type}")

# Game class that runs the game with two players

class Game:
    def __init__(self, target_score=100):
        self.target_score = target_score
        self.die = Die(seed=0)
        self.players = [Player("Player 1"), Player("Player 2")]
        self.current_player_idx = 0
    
    #Switches to the other player's turn
    def switch_turn(self):
        self.current_player_idx = 1 - self.current_player_idx  #Toggles between 0 and 1
    
    def play_turn(self):
        player = self.players[self.current_player_idx]
        turn_total = 0
        
        while True:
            roll = self.die.roll()
            print(f"{player.name} rolled: {roll}")
            
            if roll == 1:
                print(f"{player.name} loses this turn's points!")
                break  #Ends turn without adding points if 1 rolled
            
            
            turn_total += roll
            print(f"{player.name}'s turn total: {turn_total}, Current score: {player.score}")
            
            
            if isinstance(player, ComputerPlayer):  #If the player is a computer, decides automatically!
                decision = 'h' if turn_total >= player.decide(player.score) else 'r'
            else:
                decision = input("Roll again (r) or hold (h)? ").lower()
                
            if decision == 'h':
                player.add_to_score(turn_total)
                break
                
        
        print(f"{player.name}'s total score: {player.score}\n")
        self.switch_turn()
       
    
    #Main game loop
    def play_game(self):
        print("Welcome to Pig!")
        while all(player.score < self.target_score for player in self.players):
            self.play_turn()
        
        winner = max(self.players, key=lambda p: p.score)
        print(f"{winner.name} wins with {winner.score} points!")

#TimedGameProxy class that adds a timer to the game to limit it to 60 seconds

class TimedGameProxy(Game):
    def __init__(self, target_score=100):
        super().__init__(target_score)
        self.start_time = None
    
    def start_timer(self):
        self.start_time = time.time()
    
    def time_left(self):
        return time.time() - self.start_time < 60  #60 seconds limit that ends game once reached
     
    #Runs the game with a timer if chosen
    def play_game(self):
        print("Welcome to Pig!")
        self.start_timer()
        
        while all(player.score < self.target_score for player in self.players) and self.time_left():
            self.play_turn()
        
        if not self.time_left():
            print("Time's up! The winner is determined by the highest score.")
        
        winner = max(self.players, key=lambda p: p.score)
        print(f"{winner.name} wins with {winner.score} points!")

#Main function to start the game

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Play the game of Pig with human or computer players.")
    
    #Adds command-line arguments
    parser.add_argument("--player1", choices=["human", "computer"], required=True, help="Type of player 1 (human/computer)")
    parser.add_argument("--player2", choices=["human", "computer"], required=True, help="Type of player 2 (human/computer)")
    parser.add_argument("--player1_name", type=str, required=True, help="Name of player 1")
    parser.add_argument("--player2_name", type=str, required=True, help="Name of player 2")
    parser.add_argument("--timed", action="store_true", help="If set, the game will be timed (1 minute limit)")

    args = parser.parse_args()
    
    player_factory = PlayerFactory()

    #Creates players based on input arguments
    player1 = player_factory.create_player(args.player1, args.player1_name)
    player2 = player_factory.create_player(args.player2, args.player2_name)
    
    #Decides whether to use the timed game or regular game
    game = TimedGameProxy() if args.timed else Game()
    
    game.players = [player1, player2]  #Sets the players
    game.play_game()


# In[ ]:




