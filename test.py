from kaggle_environments.envs.football.helpers import *

@human_readable_agent
def agent(obs):
    #Make sure player is running
    if Action.Sprint not in obs['sticky_actions']:
        return Action.Sprint

    # We always control left team (obs and actions are mirrored appropriately by the env)
    controlled_player_pos = obs['left_team'][obs['active']]

    #Does the player we control have the ball?
    if obs['ball_owned_player'] == obs['active'] and obs['ball_owned_team'] == 0:
        #Shot if we are close to the goal
        if controlled_player_pos[0] > 0.5:
            return Action.Shot
        
        return Action.Right
    else:
        #Run towards the ball
        if obs['ball'][0] > controlled_player_pos[0] + 0.05:
            return Action.Right
        if obs['ball'][0] < controlled_player_pos[0] - 0.05:
            return Action.Left
        if obs['ball'][0] > controlled_player_pos[1] + 0.05:
            return Action.Bottom
        if obs['ball'][0] < controlled_player_pos[1] - 0.05:
            return Action.Top
        
        #Try to take over the ball if close to the ball
        return Action.Slide

from kaggle_environments import make
env = make("football", configuration={"save_video": True, "logdir": './output' ,"scenario_name": "11_vs_11_kaggle", "render": True})
output = env.run([agent, "do_nothing"])[-1]
print('Left player: reward = %s, status = %s, info = %s' % (output[0]['reward'], output[0]['status'], output[0]['info']))
print('Right player: reward = %s, status = %s, info = %s' % (output[1]['reward'], output[1]['status'], output[1]['info']))
env.render(mode="human", width=800, height=600)