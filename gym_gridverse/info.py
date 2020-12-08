from __future__ import annotations

from copy import deepcopy
from typing import Callable, Iterable, Optional, Sequence, Set, Type

import numpy as np

from .geometry import (
    Area,
    DeltaPosition,
    Orientation,
    Position,
    PositionOrTuple,
    Shape,
)
from .grid_object import Floor, GridObject, Hidden, NoneGridObject

ObjectFactory = Callable[[], GridObject]
"""Signature for a function that generates grid objects on call"""


class Grid:
    """The state of the environment (minus the agent): a two-dimensional board of objects

    A container of :py:class:`~gym_gridverse.grid_object.GridObject`. This is
    basically a two-dimensional array, with some additional functions to
    simplify interacting with the objects, such as getting areas
    """

    def __init__(self, height: int, width: int):
        """Constructs a `height` x `width` grid of :py:class:`~gym_gridverse.grid_object.Floor`

        Args:
            height (int):
            width (int):

        """
        self.shape = Shape(height, width)
        self._grid = np.array(
            [[Floor() for _ in range(width)] for _ in range(height)]
        )

    @property
    def height(self):
        return self.shape.height

    @property
    def width(self):
        return self.shape.width

    @staticmethod
    def from_objects(objects: Sequence[Sequence[GridObject]]) -> Grid:
        """constructor from matrix of GridObjects

        Args:
            objects (Sequence[Sequence[GridObject]]): initialized grid objects
        Returns:
            Grid: Grid containing those objects
        """
        # verifies input is shaped as a matrix
        array = np.array(objects)

        grid = Grid(*array.shape)
        for pos in grid.positions():
            grid[pos] = array[pos]

        return grid

    def __eq__(self, other) -> bool:
        if not isinstance(other, Grid):
            return NotImplemented

        if self.shape != other.shape:
            return False

        for pos in self.positions():
            if self[pos] != other[pos]:
                return False

        return True

    @property
    def area(self) -> Area:
        return Area((0, self.height - 1), (0, self.width - 1))

    # TODO remove;  Grid is not a collection of positions
    def __contains__(self, position: PositionOrTuple) -> bool:
        """checks if position is in the grid"""
        position = Position.from_position_or_tuple(position)
        return 0 <= position.y < self.height and 0 <= position.x < self.width

    def _check_contains(self, position: PositionOrTuple):
        """raises value error if position is not in the grid"""
        position = Position.from_position_or_tuple(position)
        if position not in self:
            raise ValueError(f'Position {position} ')

    def positions(self) -> Iterable[Position]:
        """iterator over positions"""
        return self.area.positions()

    def positions_border(self) -> Iterable[Position]:
        """iterator over border positions"""
        return self.area.positions_border()

    def positions_inside(self) -> Iterable[Position]:
        """iterator over inside positions"""
        return self.area.positions_inside()

    def get_position(self, x: GridObject) -> Position:
        for position in self.positions():
            if self[position] is x:
                return position

        raise ValueError(f'GridObject {x} not found')

    def object_types(self) -> Set[Type[GridObject]]:
        """returns object types currently in the grid"""
        return set(type(self[position]) for position in self.positions())

    def __getitem__(self, position: PositionOrTuple) -> GridObject:
        position = Position.from_position_or_tuple(position)
        return self._grid[position]

    def __setitem__(self, position: PositionOrTuple, obj: GridObject):
        if not isinstance(obj, GridObject):
            TypeError('grid can only contain entities')

        position = Position.from_position_or_tuple(position)
        self._grid[position] = obj

    def swap(self, p: Position, q: Position):
        """swap the objects at two positions"""
        self._check_contains(p)
        self._check_contains(q)
        self[p], self[q] = self[q], self[p]

    def subgrid(self, area: Area) -> Grid:
        """returns grid sliced at a given area

        Cells included in the area but outside of the grid are represented as
        Hidden objects.

        Args:
            area (Area): The area to be sliced
        Returns:
            Grid: New instance, sliced appropriately
        """
        subgrid = Grid(area.height, area.width)

        for pos_to in subgrid.positions():
            pos_from = Position.add(pos_to, area.top_left)
            subgrid[pos_to] = (
                deepcopy(self[pos_from]) if pos_from in self else Hidden()
            )

        return subgrid

    def change_orientation(self, orientation: Orientation) -> Grid:
        """returns grid as seen from someone facing the given direction

        E.g. for orientation E, the grid

        AB
        CD

        becomes

        BD
        AC

        Args:
            orientation (Orientation): The orientation of the viewer
        Returns:
            Grid: New instance rotated appropriately
        """
        times = {
            Orientation.N: 0,
            Orientation.S: 2,
            Orientation.E: 1,
            Orientation.W: 3,
        }
        objects = np.rot90(self._grid, times[orientation]).tolist()
        objects = deepcopy(objects)
        return Grid.from_objects(objects)


class Agent:
    """The agent part of the state in an environment

    A container for the:
        - :py:class:`~gym_gridverse.geometry.Position` of the agent
        - :py:class:`~gym_gridverse.geometry.Orientation` of the agent
        - :py:class:`~gym_gridverse.grid_object.GridObject` of the agent

    Adds some API functionality
    """

    def __init__(
        self,
        position: PositionOrTuple,
        orientation: Orientation,
        obj: Optional[GridObject] = None,
    ):
        """Creates the agent on `position` with `orientation` and holding `obj`

        Args:
            position (PositionOrTuple):
            orientation (Orientation):
            obj (Optional[GridObject]):
        """

        if obj is None:
            obj = NoneGridObject()

        self.position = position  # type: ignore
        self.orientation = orientation
        self.obj: GridObject = obj

    @property
    def position(self) -> Position:
        return self._position

    @position.setter
    def position(self, position: PositionOrTuple):
        self._position = Position.from_position_or_tuple(position)

    def __eq__(self, other):
        if isinstance(other, Agent):
            return (
                self.position == other.position
                and self.orientation == other.orientation
                and self.obj == other.obj
            )

        return NotImplemented

    def position_relative(self, dpos: DeltaPosition) -> Position:
        """get the absolute position from a delta position relative to the agent"""
        dpos_absolute = dpos.rotate(self.orientation)
        return Position(
            self.position.y + dpos_absolute.y, self.position.x + dpos_absolute.x
        )

    def position_in_front(self) -> Position:
        """get the position in front of the agent"""
        return self.position_relative(Orientation.N.as_delta_position())

    def get_pov_area(self, relative_area: Area) -> Area:
        """gets absolute area corresponding to given relative area

        The relative ares is relative to the agent's POV, with position (0, 0)
        representing the agent's position.  The absolute area is the relative
        ares translated and rotated such as to indicate the agent's POV in
        absolute state coordinates.
        """
        return relative_area.rotate(self.orientation).translate(self.position)
