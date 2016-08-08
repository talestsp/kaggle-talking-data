from math import sqrt

class GeoPath:

	edges = None

	def __init__(self, sorted_locations):
		points_seq = self.build_points(sorted_locations)
		self.edges = self.build_path(points_seq)

	def build_points(self, sorted_locations):
		points_seq = []

		for row in sorted_locations.iterrows():
			row = row[1]
			lon = row["longitude"]
			lat = row["latitude"]
			points_seq.append( (lon, lat) )

		return points_seq

	def distinct_days(self, timestamps):
		days = []
		for item in timestamps.iteritems():
			item = item[1]
			ts = item.split(" ")[0]
			days.append(ts)

		return set(days)

	def distance(self, p1, p2, method="euclidean"):
		if (method == "euclidean"):
			dist = sqrt( float( (p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 ) )
		else:
			raise Exception("Method not implemented")
		return dist

	def build_path(self, points_seq, decimal_precision=6, skip_if_bellow=0.03):
		last_point = points_seq[0]
		path = []

		for point in points_seq:
			edge_weight = self.distance(point, last_point)
		
			if (edge_weight > skip_if_bellow):
				edge_weight = round(edge_weight, decimal_precision)
				edge = last_point, point, edge_weight
				path.append(edge)
				last_point = point

		return path

	def path_weight(self):
		path_weight = 0
		
		for edge in self.edges:
			edge = edge[2]
			path_weight = path_weight + edge
		
		return float(path_weight)
