from typing import Iterable

import pytest

from gym_gridverse.design import (
    draw_area,
    draw_cartesian_product,
    draw_line_horizontal,
    draw_line_vertical,
    draw_room,
    draw_room_grid,
    draw_wall_boundary,
)
from gym_gridverse.geometry import Area
from gym_gridverse.grid import Grid
from gym_gridverse.grid_object import Floor, Wall


@pytest.mark.parametrize(
    'grid',
    [
        Grid(2, 3),
        Grid(4, 5),
        Grid(5, 6),
    ],
)
def test_draw_wall_boundary(grid: Grid):
    draw_wall_boundary(grid)

    for y in range(grid.height):
        assert isinstance(grid[y, 0], Wall)
        assert isinstance(grid[y, grid.width - 1], Wall)

    for x in range(grid.width):
        assert isinstance(grid[0, x], Wall)
        assert isinstance(grid[grid.height - 1, x], Wall)

    for y in range(1, grid.height - 1):
        for x in range(1, grid.width - 1):
            assert isinstance(grid[y, x], Floor)


@pytest.mark.parametrize(
    'grid,area,expected_num_walls',
    [
        (Grid(4, 5), Area((0, 3), (0, 4)), 14),
        (Grid(4, 5), Area((1, 2), (1, 3)), 6),
    ],
)
def test_draw_room(grid: Grid, area: Area, expected_num_walls: int):
    positions = draw_room(grid, area, Wall)
    assert len(positions) == len(set(positions))

    num_walls = sum(isinstance(grid[pos], Wall) for pos in grid.positions())
    assert len(positions) == num_walls == expected_num_walls


@pytest.mark.parametrize(
    'grid,ys,xs,expected_num_walls',
    [
        (Grid(3, 5), [0, 2], [0, 2, 4], 13),
        (Grid(5, 7), [0, 2, 4], [0, 2, 4, 6], 29),
    ],
)
def test_draw_room_grid(
    grid: Grid, ys: Iterable[int], xs: Iterable[int], expected_num_walls: int
):
    positions = draw_room_grid(grid, ys, xs, Wall)
    assert len(positions) == len(set(positions))

    num_walls = sum(isinstance(grid[pos], Wall) for pos in grid.positions())
    assert len(positions) == num_walls == expected_num_walls


@pytest.mark.parametrize(
    'grid,area,fill,expected_num_walls',
    [
        (Grid(4, 5), Area((0, 3), (0, 4)), True, 20),
        (Grid(4, 5), Area((0, 3), (0, 4)), False, 14),
        (Grid(4, 5), Area((1, 2), (1, 3)), True, 6),
        (Grid(4, 5), Area((1, 2), (1, 3)), False, 6),
    ],
)
def test_draw_area(grid: Grid, area: Area, fill: bool, expected_num_walls: int):
    positions = draw_area(grid, area, Wall, fill=fill)
    assert len(positions) == len(set(positions))

    num_walls = sum(isinstance(grid[pos], Wall) for pos in grid.positions())
    assert len(positions) == num_walls == expected_num_walls


@pytest.mark.parametrize(
    'grid,y,xs,expected_num_walls',
    [
        (Grid(4, 5), 1, range(0, 5), 5),
        (Grid(4, 5), 1, range(1, 4), 3),
    ],
)
def test_draw_line_horizontal(
    grid: Grid, y: int, xs: Iterable[int], expected_num_walls: int
):
    positions = draw_line_horizontal(grid, y, xs, Wall)
    assert len(positions) == len(set(positions))

    num_walls = sum(isinstance(grid[pos], Wall) for pos in grid.positions())
    assert len(positions) == num_walls == expected_num_walls


@pytest.mark.parametrize(
    'grid,ys,x,expected_num_walls',
    [
        (Grid(4, 5), range(0, 4), 1, 4),
        (Grid(4, 5), range(1, 3), 1, 2),
    ],
)
def test_draw_line_vertical(
    grid: Grid, ys: Iterable[int], x: int, expected_num_walls: int
):
    positions = draw_line_vertical(grid, ys, x, Wall)
    assert len(positions) == len(set(positions))

    num_walls = sum(isinstance(grid[pos], Wall) for pos in grid.positions())
    assert len(positions) == num_walls == expected_num_walls


@pytest.mark.parametrize(
    'grid,ys,xs,expected_num_walls',
    [
        (Grid(4, 5), range(0, 4), range(0, 5), 20),
        (Grid(4, 5), range(1, 3), range(1, 4), 6),
    ],
)
def test_draw_cross_product(
    grid: Grid, ys: Iterable[int], xs: Iterable[int], expected_num_walls: int
):
    positions = draw_cartesian_product(grid, ys, xs, Wall)
    assert len(positions) == len(set(positions))

    num_walls = sum(isinstance(grid[pos], Wall) for pos in grid.positions())
    assert len(positions) == num_walls == expected_num_walls
