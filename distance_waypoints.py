"""
~/Code/GPX % gpxinfo 28998_Orange_to_Wyong.gpx                                                                                      [Wed 20240228-170019.8]
File: 28998_Orange_to_Wyong.gpx
    Waypoints: 0
    Routes: 0
    Length 2D: 531.593km
    Length 3D: 532.855km
    Moving time: 22:41:00
    Stopped time: 00:07:10
    Max speed: 12.34m/s = 44.43km/h
    Avg speed: 6.52m/s = 23.49km/h
    Total uphill: 10406.88m
    Total downhill: 11257.68m
    Started: 2024-02-25 22:17:10+00:00
    Ended: 2024-02-26 21:05:20+00:00
    Points: 8202
    Avg distance between points: 64.81m

"""

import gpxpy
import itertools

gpx = gpxpy.parse(open("28998_Orange_to_Wyong.gpx"))
points = gpx.tracks[0].segments[0].points

# ---- Distance markers ----
# 500km, say 20 markers is good, so 25 km

# between points
distances = [0] + [p2.distance_2d(p1) for p1,p2 in zip(points[:-1], points[1:])]
cum_distances = list(itertools.accumulate(distances))

# generate marker points; grab every point from the list that is at least 25km from the previous one
distance_marker_step = 25000 # m, ie 25km
distance_marker_points = [points[0]] # start with the first one

for pt, cum_distance in zip(points, cum_distances):
    if cum_distance >= (distance_marker_step * len(distance_marker_points)):
        distance_marker_points.append(pt)

dist_waypoints = []
distance_values = range(0,len(distance_marker_points)*distance_marker_step, distance_marker_step)
for pt, dist in zip(distance_marker_points, distance_values):
    wpt = gpxpy.gpx.GPXWaypoint(pt.latitude, pt.longitude, pt.elevation, name=f"{dist/1000:.0f}km")
    dist_waypoints.append(wpt)
# add end
pt = points[-1]
dist = cum_distances[-1]
wpt = gpxpy.gpx.GPXWaypoint(pt.latitude, pt.longitude, pt.elevation, name=f"{dist/1000:.0f}km")
dist_waypoints.append(wpt)

# write out
wayptgpx = gpxpy.gpx.GPX()
wayptgpx.waypoints.extend(dist_waypoints)
open("distance_markers.gpx","w").write(wayptgpx.to_xml())


# ---- Elevation markers ----
# Uphill approx 11'000m, so every 500m

# elevation gain, not smoothed. our distances are reasonably long anyway and this probably undershoots
climbing = [0] + [max(p2.elevation-p1.elevation,0) for p1, p2 in zip(points[:-1], points[1:])]
cum_climbing = list(itertools.accumulate(climbing))

climb_marker_step = 500 # m
climb_marker_points = [points[0]] # start with the first one

for pt, cum_climb in zip(points, cum_climbing):
    if cum_climb >= (climb_marker_step * len(climb_marker_points)):
        climb_marker_points.append(pt)

ele_waypoints = []
elevation_values = range(0,len(climb_marker_points)*climb_marker_step, climb_marker_step)
for pt, ele in zip(climb_marker_points, elevation_values):
    wpt = gpxpy.gpx.GPXWaypoint(pt.latitude, pt.longitude, pt.elevation, name=f"{ele:.0f}m")
    ele_waypoints.append(wpt)
# add end
pt = points[-1]
ele = cum_climbing[-1]
wpt = gpxpy.gpx.GPXWaypoint(pt.latitude, pt.longitude, pt.elevation, name=f"{ele:.0f}m")
ele_waypoints.append(wpt)

# write out
wayptgpx = gpxpy.gpx.GPX()
wayptgpx.waypoints.extend(ele_waypoints)
open("elevation_markers.gpx","w").write(wayptgpx.to_xml())

## refactor because it's fun!!
def progress_marker_waypoints(
    points,
    distance_fn,        # lambda(p1, p2): distance_2d(p1, p2)
    distance_step,      # metres
    label_fn            # lambda p, dist: f"{dist/1000:.0f}km"
    ):
    """ Generate waypoints that mark progress along a GPX track at regular intervals.
    """
    # first distance is zero, then calculate distance between each pair of points
    # replaced distance accumulations with itertools, probably not necessary
    # [0] + [p2.distance_2d(p1) for p1,p2 in zip(points[:-1], points[1:])]
    distances = itertools.chain([0], (distance_fn(p1, p2) for p1, p2 in itertools.pairwise(points)))
    cum_distances = list(itertools.accumulate(distances))

    # generate marker points; grab every point from the list that is at least distance_step from the previous one
    distance_marker_points = [(points[0], 0)] # start with the first point, which has distance zero
    for pt, cum_distance in zip(points, cum_distances):
        if cum_distance >= (step_value := distance_step * len(distance_marker_points)):
            distance_marker_points.append((pt,step_value)) # step_value is to use as the label
    # add the last trackpoint
    distance_marker_points.append((points[-1], cum_distances[-1]))

    # generate the marker waypoints
    dist_waypoints = [gpxpy.gpx.GPXWaypoint(
            pt.latitude, pt.longitude, pt.elevation, name=label_fn(pt, dist)
        ) for pt, dist in distance_marker_points]

    return dist_waypoints

# distance v2
distance_waypoints = progress_marker_waypoints(
    points,
    lambda p1, p2: p1.distance_2d(p2),
    25000, # 25 km
    lambda p, dist: f"{dist/1000:.0f}km"
)
# write out
wayptgpx = gpxpy.gpx.GPX()
wayptgpx.waypoints.extend(dist_waypoints)
open("distance_markers_v2.gpx","w").write(wayptgpx.to_xml())

# climb v2
climbing_waypoints = progress_marker_waypoints(
    points,
    lambda p1, p2: max(p2.elevation-p1.elevation, 0),
    500, # 500m
    lambda p, dist: f"{dist/1000:,.1f}vkm"
)
# write out
wayptgpx = gpxpy.gpx.GPX()
wayptgpx.waypoints.extend(climbing_waypoints)
open("elevation_markers_v2.gpx","w").write(wayptgpx.to_xml())