# Authors: Mayank Parasar
from m5.params import *
from m5.objects import *

from BaseTopology import SimpleTopology

class FlattenedButterfly(SimpleTopology):
	description = 'FlattenedButterfly'

	def __init__(self, controllers):
		self.nodes = controllers

	# Makes a generic FlattenedButterfly assuming an equalt number of cache and
	# directory cntrls
	#TODO: Since there will be links of unequal length, therefore thus each link will
	# assign an increasing number of latency based on the distance from it's neighour

	def makeTopology(self, options, network, IntLink, ExtLink, Router):
		nodes = self.nodes
		# These parameters will be set form the command line
		link_latency = options.link_latency # used by simple and garnet
		router_latency = options.router_latency # only used by garnet
		num_routers = options.num_cpus
		num_rows = options.mesh_rows
		# There must be an evenly divisible number of cntrls to routers
		# Also, obviously the number of rows must be <= the number of routers
		cntrls_per_router, remainder = divmod(len(nodes), num_routers)
		assert(num_rows <= num_routers)
		num_columns = int(num_routers/num_rows)
		assert(num_columns * num_rows == num_routers)

		#  Create the router in the FlattenedButterfly
		routers = [Router(router_id=i) for i in range (num_routers)]
		network.routers = routers

		# link counter to set unique link ids (we have numbered links like one
			# taught in the class.. this help in enforcing routing algorithm)
		link_count = 0

		# Add all but the remainder nodes to the list of nodes to be uniformly
		# distributed across the network
		network_nodes = []
		remainder_nodes = []
		for node_index in xrange(len(nodes)):
			if node_index < (len(nodes) - remainder):
				network_nodes.append(nodes[node_index])
			else:
				remainder_nodes.append(nodes[node_index])

		# Connect each node to the appropriate router
		ext_links = []
		for (i, n) in enumerate(network_nodes):
			cntrl_level, router_id = divmod(i, num_routers)
			assert(cntrl_level < cntrls_per_router)
			ext_links.append(ExtLink(link_id=link_count, ext_node=n,
																int_node=routers[router_id]))
			link_count +=1

		network.ext_links = ext_links
		# Create the FlattenedButterfly links. First row (east-west) links then
		# column (north-south) links
		# columns links are given higher weights to implement XY routing
		int_links = []
		# print 'Creating from east(out)-west(in) links here:'
		# print 'num_columns %d' %(num_columns)
		# print 'num_rows %d' %(num_rows)
		for row in xrange(num_rows):
			for col in xrange(num_columns): # assign proper value to west_id and east_id and Each iteration connects them
				# print '(row: %d, col: %d)' %(row, col)
				west_in = col + (row*num_columns) #Change here
				for i in xrange((col+1)+(row*num_columns) ,(row*num_columns + num_columns)):
					assert(i<(row*num_columns + num_columns)) #basic assertion
					east_out = i
					# print "Router(east_out) " + str(east_out) + " created a link to router(west_id)" + str(west_in)
					int_links.append(IntLink(link_id=link_count,
											src_node=routers[east_out],
											dst_node=routers[west_in],
											src_outport="East",
											dst_inport="West",
											latency=1,
											weight=1))
					link_count += 1

		# print 'Creating from west(out)-east(in) links here:'
		# print 'num_columns %d' %(num_columns)
		# print 'num_rows %d' %(num_rows)
		for row in xrange(num_rows):
			for col in xrange(num_columns): # assign proper value to west_id and east_id and Each iteration connects them
				# print '(row: %d, col: %d)' %(row, col)
				west_out = col + (row*num_columns) #Change here
				for i in xrange((col+1)+(row*num_columns) ,(row*num_columns + num_columns)):
					assert(i<(row*num_columns + num_columns)) #basic assertion
					east_in = i
					# print "Router(east_out) " + str(east_out) + " created a link to router(west_id)" + str(west_in)
					int_links.append(IntLink(link_id=link_count,
											src_node=routers[west_out],
											dst_node=routers[east_in],
											src_outport="West",
											dst_inport="East",
											latency=1,
											weight=1))
					link_count += 1
		# assert(0)
		# (north-south) connections...
		# print 'Creating north-south links here:'
		for col in xrange(num_columns):
			for row in xrange(num_rows):
				# print '(row: %d, col: %d)' %(row, col)
				north_out = col + (row * num_columns)
				i = col
				while (i<north_out):
					south_in = i
					i += num_columns
					# print "Router(north_out) " + str(north_out) + " created a link to(south_in) " + str(south_in)
					int_links.append(IntLink(link_id=link_count,
											src_node=routers[north_out],
											dst_node=routers[south_in],
											src_outport="North",
											dst_inport="South",
											latency=1,
											weight=2))
					link_count += 1

		# print 'Creating north-south links here:'
		for col in xrange(num_columns):
			for row in xrange(num_rows):
				# print '(row: %d, col: %d)' %(row, col)
				north_in = col + (row * num_columns)
				i = col
				while (i<north_in):
					south_out = i
					i += num_columns
					# print "Router(north_in) " + str(north_in) + " created a link to(south_out) " + str(south_out)
					int_links.append(IntLink(link_id=link_count,
											src_node=routers[south_out],
											dst_node=routers[north_in],
											src_outport="South",
											dst_inport="North",
											latency=1,
											weight=2))
					link_count += 1
		# assert(0)
		network.int_links = int_links