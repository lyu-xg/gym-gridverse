from typing import Sequence

import pytest

from gym_gridverse.envs.visibility_functions import (
    factory,
    full_visibility,
    minigrid_visibility,
    partial_visibility,
    raytracing_visibility,
)
from gym_gridverse.geometry import Position
from gym_gridverse.grid import Grid
from gym_gridverse.grid_object import Floor, GridObject, Wall


@pytest.mark.parametrize(
    'objects',
    [
        [
            [Floor(), Floor(), Floor()],
            [Floor(), Floor(), Floor()],
            [Floor(), Floor(), Floor()],
        ],
        [
            [Wall(), Wall(), Wall()],
            [Wall(), Wall(), Wall()],
            [Wall(), Wall(), Wall()],
        ],
    ],
)
def test_full_visibility(objects: Sequence[Sequence[GridObject]]):
    grid = Grid.from_objects(objects)
    for position in grid.positions():
        visibility = full_visibility(grid, position)

        assert visibility.dtype == bool
        assert visibility.all()


@pytest.mark.parametrize(
    'objects,position,expected_int',
    [
        (
            [
                [Floor(), Floor(), Floor(), Floor(), Floor()],
                [Floor(), Floor(), Floor(), Floor(), Floor()],
                [Floor(), Floor(), Floor(), Floor(), Floor()],
            ],
            Position(2, 2),
            [
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
            ],
        ),
        (
            [
                [Floor(), Floor(), Floor(), Floor(), Floor()],
                [Floor(), Wall(), Wall(), Wall(), Floor()],
                [Floor(), Wall(), Floor(), Wall(), Floor()],
            ],
            Position(2, 2),
            [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
            ],
        ),
        (
            [
                [Floor(), Floor(), Floor(), Floor(), Floor()],
                [Floor(), Wall(), Floor(), Wall(), Floor()],
                [Floor(), Wall(), Floor(), Wall(), Floor()],
            ],
            Position(2, 2),
            [
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
            ],
        ),
        (
            [
                [Floor(), Floor(), Floor(), Floor(), Floor()],
                [Floor(), Wall(), Wall(), Wall(), Floor()],
                [Floor(), Floor(), Floor(), Wall(), Floor()],
            ],
            Position(2, 2),
            [
                [1, 0, 0, 0, 0],
                [1, 1, 1, 1, 0],
                [1, 1, 1, 1, 0],
            ],
        ),
    ],
)
def test_partial_visibility(
    objects: Sequence[Sequence[GridObject]],
    position: Position,
    expected_int: Sequence[Sequence[int]],
):
    grid = Grid.from_objects(objects)
    visibility = partial_visibility(grid, position)
    assert visibility.dtype == bool
    assert (visibility == expected_int).all()


@pytest.mark.parametrize(
    'objects,position,expected_int',
    [
        (
            [
                [Floor(), Floor(), Floor(), Floor(), Floor()],
                [Floor(), Floor(), Floor(), Floor(), Floor()],
                [Floor(), Floor(), Floor(), Floor(), Floor()],
            ],
            Position(2, 2),
            [
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
            ],
        ),
        (
            [
                [Floor(), Floor(), Floor(), Floor(), Floor()],
                [Floor(), Wall(), Wall(), Wall(), Floor()],
                [Floor(), Wall(), Floor(), Wall(), Floor()],
            ],
            Position(2, 2),
            [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
            ],
        ),
        (
            [
                [Floor(), Floor(), Floor(), Floor(), Floor()],
                [Floor(), Wall(), Floor(), Wall(), Floor()],
                [Floor(), Wall(), Floor(), Wall(), Floor()],
            ],
            Position(2, 2),
            [
                [1, 1, 1, 1, 1],
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
            ],
        ),
        (
            [
                [Floor(), Floor(), Floor(), Floor(), Floor()],
                [Floor(), Wall(), Wall(), Wall(), Floor()],
                [Floor(), Floor(), Floor(), Wall(), Floor()],
            ],
            Position(2, 2),
            [
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 0],
                [1, 1, 1, 1, 0],
            ],
        ),
    ],
)
def test_minigrid_visibility(
    objects: Sequence[Sequence[GridObject]],
    position: Position,
    expected_int: Sequence[Sequence[int]],
):
    grid = Grid.from_objects(objects)
    visibility = minigrid_visibility(grid, position)
    assert visibility.dtype == bool
    assert (visibility == expected_int).all()


@pytest.mark.parametrize(
    'objects,position,expected_int',
    [
        (
            [
                [Floor(), Floor(), Floor(), Floor(), Floor()],
                [Floor(), Floor(), Floor(), Floor(), Floor()],
                [Floor(), Floor(), Floor(), Floor(), Floor()],
            ],
            Position(2, 2),
            [
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
                [1, 1, 1, 1, 1],
            ],
        ),
        (
            [
                [Floor(), Floor(), Floor(), Floor(), Floor()],
                [Floor(), Wall(), Wall(), Wall(), Floor()],
                [Floor(), Wall(), Floor(), Wall(), Floor()],
            ],
            Position(2, 2),
            [
                [0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
            ],
        ),
        (
            [
                [Floor(), Floor(), Floor(), Floor(), Floor()],
                [Floor(), Wall(), Floor(), Wall(), Floor()],
                [Floor(), Wall(), Floor(), Wall(), Floor()],
            ],
            Position(2, 2),
            [
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
                [0, 1, 1, 1, 0],
            ],
        ),
        (
            [
                [Floor(), Floor(), Floor(), Floor(), Floor()],
                [Floor(), Wall(), Wall(), Wall(), Floor()],
                [Floor(), Floor(), Floor(), Wall(), Floor()],
            ],
            Position(2, 2),
            [
                [0, 0, 0, 0, 0],
                [1, 1, 1, 1, 0],
                [1, 1, 1, 1, 0],
            ],
        ),
    ],
)
def test_raytracing_visibility(
    objects: Sequence[Sequence[GridObject]],
    position: Position,
    expected_int: Sequence[Sequence[int]],
):
    grid = Grid.from_objects(objects)
    visibility = raytracing_visibility(grid, position)
    assert visibility.dtype == bool
    assert (visibility == expected_int).all()


@pytest.mark.parametrize(
    'name',
    [
        'full_visibility',
        'partial_visibility',
        'minigrid_visibility',
        'raytracing_visibility',
        'stochastic_raytracing_visibility',
    ],
)
def test_factory_valid(name: str):
    factory(name)


@pytest.mark.parametrize(
    'name,exception',
    [
        ('invalid', ValueError),
    ],
)
def test_factory_invalid(name: str, exception: Exception):
    with pytest.raises(exception):  # type: ignore
        factory(name)
