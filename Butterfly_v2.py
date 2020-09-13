# Copyright (c) 2010 Advanced Micro Devices, Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Steve Reinhardt

from m5.params import *
from m5.objects import *

from BaseTopology import SimpleTopology

class Butterfly_v2(SimpleTopology):
    description='Butterfly_v2'

    def __init__(self, controllers):
        self.nodes = controllers

    def makeTopology(self, options, network, IntLink, ExtLink, Router):

        # default values for link latency and router latency.
        # Can be over-ridden on a per link/router basis
        link_latency = options.link_latency # used by simple and garnet
        router_latency = options.router_latency # only used by garnet
        num_rows = options.mesh_rows
        # num_routers = k**mesh_rows
        print(len(self.nodes))

        k=4
        n=3
        num_routers_in_network = n*(k**(n-1))

        # print(num_routers_in_network)
        routers = [Router(router_id=i, latency = router_latency) for i in range(num_routers_in_network)]
        # print(len(routers))
        routers_each_stage = k**(n-1)
        # print(routers_each_stage)
        network.routers = routers

        link_count = 0
        ext_links = []

        for (i, n) in enumerate(self.nodes[:len(self.nodes)/2]):
            # print('i: ', i )
            # print('n: ', n )
            cntrl_level, router_id = divmod(i, routers_each_stage)
            # print('cntrl_level: ', cntrl_level)
            # print('router_id: ', router_id)
            ext_links.append(ExtLink(link_id=link_count, ext_node=n,
                                    int_node=routers[router_id],
                                    latency = link_latency))
            link_count += 1
            # print('END OF ITERATION')


        for (i, n) in enumerate(self.nodes[len(self.nodes)/2:]):
            # print('i: ', i )
            # print('n: ', n )
            cntrl_level, router_id = divmod(i, routers_each_stage)
            # print('cntrl_level: ', cntrl_level)
            # print('router_id: ', 32+router_id)
            ext_links.append(ExtLink(link_id=link_count, ext_node=n,
                                    int_node=routers[32+router_id],
                                    latency = link_latency))
            link_count += 1
            # print('END OF ITERATION')          
        network.ext_links = ext_links

        int_links = []

        print('INTERNAL LINKS START')
        print('Stage 1 Quarter 1 Links')
        for i in range(routers_each_stage/4):
            for j in range(routers_each_stage/4):
                print('Link Count: ', link_count) 
                print('Link Starts: ')
                print('Link Source Node: ', get_id(routers[i]))
                print('Link Destination Node: ', get_id(routers[i + routers_each_stage + (j*routers_each_stage/4)]))           
                int_links.append(IntLink(link_id=(link_count),
                                     src_node=routers[i],
                                     dst_node=routers[i + routers_each_stage + (j*routers_each_stage/4)],
                                     latency = link_latency,weight=1))
                link_count += 1

        print('\n\nStage 1 Quarter 2 Links')
        for i in range(routers_each_stage/4, routers_each_stage/2):
            for j in range(-1,3):
                print('Link Count: ', link_count) 
                print('Link Starts: ')
                print('Link Source Node: ', get_id(routers[i]))
                print('Link Destination Node: ', get_id(routers[i + routers_each_stage + (j*routers_each_stage/4)]))           
                int_links.append(IntLink(link_id=(link_count),
                                     src_node=routers[i],
                                     dst_node=routers[i + routers_each_stage + (j*routers_each_stage/4)],
                                     latency = link_latency,weight=1))
                link_count += 1


        print('\n\nStage 1 Quarter 3 Links')
        for i in range(routers_each_stage/2, 3*routers_each_stage/4):
            for j in range(-2,2):
                print('Link Count: ', link_count) 
                print('Link Starts: ')
                print('Link Source Node: ', get_id(routers[i]))
                print('Link Destination Node: ', get_id(routers[i + routers_each_stage + (j*routers_each_stage/4)]))           
                int_links.append(IntLink(link_id=(link_count),
                                     src_node=routers[i],
                                     dst_node=routers[i + routers_each_stage + (j*routers_each_stage/4)],
                                     latency = link_latency,weight=1))
                link_count += 1


        print('\n\nStage 1 Quarter 4 Links')
        for i in range(3*routers_each_stage/4, routers_each_stage):
            for j in range(-3,1):
                print('Link Count: ', link_count) 
                print('Link Starts: ')
                print('Link Source Node: ', get_id(routers[i]))
                print('Link Destination Node: ', get_id(routers[i + routers_each_stage + (j*routers_each_stage/4)]))           
                int_links.append(IntLink(link_id=(link_count),
                                     src_node=routers[i],
                                     dst_node=routers[i + routers_each_stage + (j*routers_each_stage/4)],
                                     latency = link_latency,weight=1))
                link_count += 1





        print('\n\nStage 2 Quarter 1 Links')
        for i in [0,4,8,12]:
            for j in range(routers_each_stage/4):
                print('Link Count: ', link_count) 
                print('Link Starts: ')
                print('Link Source Node: ', get_id(routers[i+ routers_each_stage]))
                print('Link Destination Node: ', get_id(routers[i + 2*routers_each_stage + j]))           
                int_links.append(IntLink(link_id=(link_count),
                                     src_node=routers[i],
                                     dst_node=routers[i + 2*routers_each_stage + j],
                                     latency = link_latency,weight=1))
                link_count += 1    



        print('\n\nStage 2 Quarter 2 Links')
        for i in [1,5,9,13]:
            for j in range(-1,3):
                print('Link Count: ', link_count) 
                print('Link Starts: ')
                print('Link Source Node: ', get_id(routers[i+ routers_each_stage]))
                print('Link Destination Node: ', get_id(routers[i + 2*routers_each_stage + j]))           
                int_links.append(IntLink(link_id=(link_count),
                                     src_node=routers[i],
                                     dst_node=routers[i + 2*routers_each_stage + j],
                                     latency = link_latency,weight=1))
                link_count += 1  



        print('\n\nStage 2 Quarter 3 Links')
        for i in [2,6,10,14]:
            for j in range(-2,2):
                print('Link Count: ', link_count) 
                print('Link Starts: ')
                print('Link Source Node: ', get_id(routers[i+ routers_each_stage]))
                print('Link Destination Node: ', get_id(routers[i + 2*routers_each_stage + j]))           
                int_links.append(IntLink(link_id=(link_count),
                                     src_node=routers[i],
                                     dst_node=routers[i + 2*routers_each_stage + j],
                                     latency = link_latency,weight=1))
                link_count += 1       


        print('\n\nStage 2 Quarter 4 Links')
        for i in [3,7,11,15]:
            for j in range(-3,1):
                print('Link Count: ', link_count) 
                print('Link Starts: ')
                print('Link Source Node: ', get_id(routers[i+ routers_each_stage]))
                print('Link Destination Node: ', get_id(routers[i + 2*routers_each_stage + j]))           
                int_links.append(IntLink(link_id=(link_count),
                                     src_node=routers[i],
                                     dst_node=routers[i + 2*routers_each_stage + j],
                                     latency = link_latency,weight=1))
                link_count += 1  
        network.int_links = int_links   


def get_id(node):
    return str(node).split('.')[3].split('routers')[1]            