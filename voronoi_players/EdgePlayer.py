import math

from voronoi_players.abstract_player import Player
from algorithm import Algorithm
from nodes.bounding_box import BoundingBox
from nodes.diagram import HalfEdge


from nodes.point import Point


def calculate_distance(point_1, point_2):
    dist = math.sqrt((point_2.x - point_1.x) ** 2 + (point_2.y - point_1.y) ** 2)
    return dist


def point_along_edge(point_1, point_2, fraction_of_distance):
    point = Point()
    point.x = point_1.x + ((point_2.x - point_1.x) * fraction_of_distance)
    point.y = point_1.y + ((point_2.y - point_1.y) * fraction_of_distance)
    return point


def point_perpendicular_intersection(point_1, point_2, point_perpendicular):
    point_intersection = Point()

    print(type(point_1))
    print(type(point_2))
    print(type(point_perpendicular))


    k = ((point_2.y - point_1.y) * (point_perpendicular.x - point_1.x) -
         (point_2.x - point_1.x) * (point_perpendicular.y - point_1.y)) / \
        (math.pow((point_2.y - point_1.y),2) + math.pow((point_2.x - point_1.x),2))
    point_intersection.x = point_perpendicular.x - k * (point_2.y - point_1.y)
    point_intersection.y = point_perpendicular.y + k * (point_2.x - point_1.x)

    return point_intersection


class EdgePlayer(Player):

    # Set Default values for EdgePlayer
    weight_edge_length = 1
    weight_inner_point_distance = 1
    fraction_between_player_points = 0.0    # Between -1 and 1
    fraction_between_edge_nodes = 0.0       # Between -1 and 1

    @property
    def place_points(self):
        # Check whether currently player 2 is playing (if not then return error)
        if self.player_nr != 2:
            print('The EDGE-PLAYER STRATEGY only works for Player 2')
        else:
            print('testerdetest')
            # Create a list with only points for player 1
            points_player1 = list(filter((lambda point: point.player == 1), self.state.points))

            # Construct a Voronoi for the points of player 1
            voronoi = Algorithm(BoundingBox(-1, 26, -1, 26))
            voronoi.create_diagram(points_player1, visualize_steps=False)

            # Check all edges in Voronoi of player 1
            edges_seen = []
            points_desirability = []
            for half_edge in voronoi.edges:
                print('if this doesnt show. there are no edges in voronoi edges')
                # Check whether halfedge's twin has already been seen before
                if half_edge not in edges_seen:
                    print('test')

                    edge = half_edge

                    # Determine which edge is A and which is B
                    if not edge.incident_point is None:
                        half_edge_A = edge
                        half_edge_B = edge.twin
                        if edge.twin.incident_point is None:
                            print('A')
                            boundary_edge = True
                        else:
                            print('B')
                            boundary_edge = False
                    else:
                        print('C')
                        half_edge_A = edge.twin
                        half_edge_B = edge
                        boundary_edge = True

                    # Find the coordinates of the start and end point of the edge, in the direction of edge A
                    edge_start = half_edge_A.origin.position
                    edge_end = half_edge_A.twin.origin.position
                    incident_point = half_edge_A.incident_point
                    twin_incident_point = half_edge_A.twin.incident_point

                    # Find midway and halfway-point for edge
                    edge_halfwaypoint = point_along_edge(edge_start, edge_end, 0.5)
                    edge_midpoint = point_perpendicular_intersection(edge_start, edge_end, incident_point)

                    # If both half-edges (A and B) of edge have incident points, check to make sure that
                    #   edge_halfwaypoint comes before edge_midpoint with regards from the direction of edge A.
                    # If this does not hold, swap A and B.
                    if not boundary_edge:
                        if calculate_distance(edge_midpoint, edge_start) \
                                < calculate_distance(edge_halfwaypoint, edge_start):
                            half_edge_A, half_edge_B = half_edge_B, half_edge_A
                            edge_start, edge_end = edge_end, edge_start
                            incident_point, twin_incident_point = twin_incident_point, incident_point

                    # Find the length of the edge, and the distance between the corresponding player points
                    edge_length = calculate_distance(edge_start, edge_end)
                    inner_point_distance = 2 * calculate_distance(incident_point, edge_midpoint)

                    # Calculate the desirability of the edge
                    desirability_of_point = self.weight_edge_length * edge_length \
                                            + self.weight_inner_point_distance * inner_point_distance

                    # If there exists no incident-point for the twin edge, take the absolute value of
                    #   self.fraction_between_player_points
                    if boundary_edge:
                        self.fraction_between_player_points = math.fabs(self.fraction_between_player_points)

                    # Calculate Point Placement
                    if self.fraction_between_player_points >= 0:
                        calculate_location_incident_point = incident_point
                    else:
                        calculate_location_incident_point = twin_incident_point

                    if self.fraction_between_player_points >= 0:
                        calculate_location_vertex_point = edge_start
                    else:
                        calculate_location_vertex_point = edge_end

                    print("point added")

                    point_placement = point_along_edge(
                        point_along_edge(edge_halfwaypoint, calculate_location_incident_point, math.fabs(self.fraction_between_player_points)),
                            calculate_location_vertex_point,
                            math.fabs(self.fraction_between_edge_nodes))
                    point_placement.player = 2

                    # Store point in points_desirability
                    points_desirability.append({'point': point_placement, 'desirability': desirability_of_point})

                    # insert edge and edge's twin in list of seen edges.
                    edges_seen.append(edge)
                    edges_seen.append(edge.twin)

            # Sort list of points based on their desirability
            points_desirability_sorted = sorted(points_desirability, key=lambda item: item['desirability'])

            # Store points for player 2
            for i in range(self.state.m if self.player_nr == 1 else self.state.n):
                self.state.points.append(points_desirability_sorted[i].get('point'))
        return self.state
