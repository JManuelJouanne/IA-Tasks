import numpy as np
from flappy_bidoof import FlappyBidoofEnv

# Crear el entorno
env = FlappyBidoofEnv()

# Parámetros del agente
num_episodes = 1
learning_rate = 0.1   # alpha
discount_rate = 0.99  # gamma
exploration_rate = 1  # épsilon

# Inicializar Q-table
number_of_states = np.prod(env.observation_space.nvec)
number_of_actions = env.action_space.n
q_table = np.zeros((number_of_states, number_of_actions))

class Agent:
    def __init__(self, learning_rate: float, discount_rate: float, 
                 exploration_rate: float):
        self.learning_rate = learning_rate
        self.discount_rate = discount_rate
        self.exploration_rate = exploration_rate
        ### MODIFICAR ###

    def choose_action(self, *args, **kwargs):
        ### MODIFICAR ###
        return np.random.randint(number_of_actions) # Full random
    
    def learn(self, *args, **kwargs):
        ### MODIFICAR ###
        pass

bidoof_the_brave = Agent(learning_rate, discount_rate, exploration_rate)

# # Esta línea te permite controlar la velocidad de la animación
# env.metadata["render_fps"] = 3  # por defecto es 3

for episode in range(num_episodes):
    state = env.reset()
    done = False

    # Comenta esto si vas a entrenar
    env.render(window_size=(600, 600), done=done)

    while not done:
        # Agente aleatorio
        action = bidoof_the_brave.choose_action(state)
        
        new_state, reward, done, _, _ = env.step(action)

        bidoof_the_brave.learn(reward, new_state)
        
        # Comenta esto si vas a entrenar
        env.render(window_size=(600, 600), done=done)

        state = new_state
