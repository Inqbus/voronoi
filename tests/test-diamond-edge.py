from algorithm import Algorithm
from graph.bounding_box import BoundingBox
from graph.point import Point

points = [
    Point(5, 10),
    Point(0, 5),
    Point(10, 5),
    Point(5, 0),
]

v = Algorithm(BoundingBox(0, 10, 0, 10))
v.create_diagram(points=points, visualize_steps=True, verbose=True, visualize_result=True)

for point in v.points:
    print(point.cell_size(2), end=",")