**About the project**
This project is about implementing Q-learning on simple maze problems.

**Action**
The agent can only do four directions: up, down, left and right.

**Reward Policy**
No move: Reach the wall or the boundary. That is, the next state is the same as this state(now). Reward is "-10".
Forward: You can move, but you have not reached the goal. Reward is "-1".
Goal: Reach the goal. Reward is "100".
