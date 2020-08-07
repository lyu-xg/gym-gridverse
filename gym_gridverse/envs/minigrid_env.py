import copy
from typing import Tuple

from gym_gridverse.actions import Actions
from gym_gridverse.envs import Environment
from gym_gridverse.envs.observation_functions import ObservationFunction
from gym_gridverse.envs.reset_functions import ResetFunction
from gym_gridverse.envs.reward_functions import RewardFunction
from gym_gridverse.envs.state_dynamics import StateDynamics
from gym_gridverse.envs.terminating_functions import TerminatingFunction
from gym_gridverse.observation import Observation
from gym_gridverse.spaces import DomainSpace
from gym_gridverse.state import State


# TODO find better name
class Minigrid(Environment):
    def __init__(  # pylint: disable=too-many-arguments
        self,
        domain_space: DomainSpace,
        reset_function: ResetFunction,
        step_function: StateDynamics,
        observation_function: ObservationFunction,
        reward_function: RewardFunction,
        termination_function: TerminatingFunction,
    ):

        self._functional_reset = reset_function
        self._functional_step = step_function
        self._functional_observation = observation_function
        self.reward_function = reward_function
        self.termination_function = termination_function

        super().__init__(
            domain_space.state_space,
            domain_space.action_space,
            domain_space.observation_space,
        )

    def functional_reset(self) -> State:
        return self._functional_reset()

    def functional_step(
        self, state: State, action: Actions
    ) -> Tuple[State, float, bool]:

        next_state = copy.deepcopy(state)
        self._functional_step(next_state, action)

        reward = self.reward_function(state, action, next_state)
        terminal = self.termination_function(state, action, next_state)

        return (next_state, reward, terminal)

    def functional_observation(self, state: State) -> Observation:
        return self._functional_observation(state)