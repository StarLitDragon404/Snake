from snake_game import SnakeGame, Point, Direction
import pickle, torch
net = None
import numpy as np
with open('model/model.pickle', 'rb') as f:
    net = pickle.load(f)
def get_state(game):
        head = game.snake[0]
        point_l = Point(head.x-20, head.y)
        point_r = Point(head.x+20, head.y)
        point_u = Point(head.x, head.y-20)
        point_d = Point(head.x, head.y+20)
        
        dir_l = game.direction == Direction.LEFT
        dir_r = game.direction == Direction.RIGHT
        dir_u = game.direction == Direction.UP
        dir_d = game.direction == Direction.DOWN
        
        state = [
            (dir_r and game.is_collision(point_r)) or
            (dir_l and game.is_collision(point_l)) or
            (dir_u and game.is_collision(point_u)) or
            (dir_d and game.is_collision(point_d)),
            (dir_u and game.is_collision(point_r)) or
            (dir_d and game.is_collision(point_l)) or
            (dir_l and game.is_collision(point_u)) or
            (dir_r and game.is_collision(point_d)),
            (dir_d and game.is_collision(point_r)) or
            (dir_u and game.is_collision(point_l)) or
            (dir_r and game.is_collision(point_u)) or
            (dir_l and game.is_collision(point_d)),
            dir_l,
            dir_r,
            dir_u,
            dir_d,
            
            game.food.x < game.head.x,
            game.food.x > game.head.x,
            game.food.y < game.head.y,
            game.food.y > game.head.y,
            
        ]
        return np.array(state, dtype=int)
while True:
    loop = SnakeGame()
    while True:
        action = [0, 0, 0]
        action[net(torch.tensor(get_state(loop), dtype=torch.float)).argmax()] = 1
        reward, game_over, score = loop.play_step(action)
        if game_over:
            break

