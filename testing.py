from gmplot import gmplot

# Place map
gmap = gmplot.GoogleMapPlotter(0, 0, 13)

latitudes, longitudes = zip(*[
    (37.771269, -122.511015),
    (37.773495, -122.464830),
    (37.774797, -122.454538),
    (37.771988, -122.454018),
    (37.773646, -122.440979),
    (37.772742, -122.440797),
    (37.771096, -122.453889),
    (37.768669, -122.453518),
    (37.766227, -122.460213),
    (37.764028, -122.510347),
    (37.771269, -122.511015)
    ])

gmap.plot(latitudes, longitudes, 'cornflowerblue', edge_width=10)

# Marker
hidden_gem_lat, hidden_gem_lon = 37.770776, -122.461689
gmap.marker(hidden_gem_lat, hidden_gem_lon, 'cornflowerblue')

hidden_gem_lat, hidden_gem_lon = 40.770776, -130.461689
gmap.marker(hidden_gem_lat, hidden_gem_lon, 'cornflowerblue')

# Draw
gmap.draw("my_map.html")
