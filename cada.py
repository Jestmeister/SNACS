# This code is an extention of the cada code available at
# https://github.com/thomashelling/cada
#
# coding=utf-8

import networkx as nx
from networkx.algorithms.community import asyn_fluidc
from networkx.algorithms.community import greedy_modularity_communities as gmc
import random
import numpy as np
import community
import time
import infomap
import igraph as ig
import leidenalg

class cada():
	def __init__(self, graph, algorithm='louvain', resolution=0.1):
		
		# First do community detection
		if algorithm == 'louvain':
			partition = community.best_partition(graph, resolution=resolution)
		elif algorithm == 'leiden':
			partition = self.run_leiden(graph,resolution=resolution)
		elif algorithm == 'fluid':
			partition = self.run_fluid(graph)
		elif algorithm == 'greedy':
			partition = self.run_greedy(graph,resolution)
		else:
			partition = self.run_infomap(graph)
		
		communities = set()
		for node in graph.nodes():
			if node in partition:
				communities.add(partition[node])

		anom_score = {}

		# Compute anomaly score for each node
		for node in graph.nodes():
			comms = {}
			for neighbor in graph.neighbors(node):
				if neighbor != node:
					if partition[neighbor] not in comms:
						comms[partition[neighbor]] = 0

					comms[partition[neighbor]] += 1

			if len(comms) > 0:
				# The number of communities it is connected to. 
				comms = np.array(list(comms.values()))
				# print('nr communities connected', comms)
				max_com = np.max(comms)
				# print('Maxcommunity', max_com)
				comms = comms / max_com
				# print('Communities normalized', comms)
				anom_score[node] = np.sum(comms)		
				# print('Anomaly score., ', anom_score[node])

		self.anomaly_scores = sorted(anom_score.items(), key=lambda x: x[1])[::-1]
		self.n_nodes = graph.number_of_nodes()

	def clf(self,n_injections):
		"""
		Predicts n_injections anomaly nodes 
		"""
		pred = np.zeros(self.n_nodes,dtype=int)
		#worst_nodes = self.anomaly_scores[:n_injections][0]
		for ind,anomaly in enumerate(self.anomaly_scores):
			if(ind>=n_injections):
				break
			pred[anomaly[0]] = 1
			
		return pred

	def run_leiden(self,graph,resolution):
		"""
		Creates partitions with the Leiden algorithm
		"""
		h = ig.Graph.from_networkx(graph)
		#part = leidenalg.find_partition(h, leidenalg.ModularityVertexPartition)
		#part = leidenalg.find_partition(h, leidenalg.RBConfigurationVertexPartition,resolution_parameter = 0.5)
		part = leidenalg.find_partition(h, leidenalg.CPMVertexPartition,resolution_parameter = resolution)
		partition = {}

		for ind,com in enumerate(part):
			for node in com:
				partition[node] = ind

		return partition

	def run_greedy(self,graph,resolution):
		"""
		Creates partitions with Clauset-Newman-Moore greedy modularity maximization
		"""
		best_n = int(graph.number_of_nodes()/10)
		communities = gmc(graph,resolution=resolution,best_n=best_n)
		partition = {}
		print(f"nr of coms={len(communities)}")
		for ind,com in enumerate(communities):
			for node in com:
				partition[node] = ind
		
		return partition

	def run_fluid(self,graph):
		"""
		Creates partitions with async_fluidc
		"""
		k = int(graph.number_of_nodes()/100)
		it = asyn_fluidc(graph,k=k)
		partition = {}

		for ind,com in enumerate(it):
			for node in com:
				partition[node] = ind

		return partition

	def run_infomap(self, graph):
		"""
		Runs Infomap with infomap package 
		"""
		infomapSimple = infomap.Infomap("--two-level --silent")
		network = infomapSimple.network
		
		for e in graph.edges():
			network.addLink(e[0], e[1])

		partition = {}
		infomapSimple.run()
		for node in infomapSimple.iterTree():
			if node.isLeaf():
				partition[node.physicalId] = node.moduleIndex()

		return partition

	def get_anomaly_scores(self, nr_anomalies=None):
		"""
		Returns tuple (node, anomaly_score) for either nr_anomalies or all
		"""
		if nr_anomalies:
			return self.anomaly_scores[:nr_anomalies]
		else:
			return self.anomaly_scores 

	def get_top_anomalies(self, nr_anomalies=100):
		"""
		Returns highest scoring anomalies
		"""					
		anomalies = []
		for anomaly in self.anomaly_scores[:nr_anomalies]:
			anomalies.append(anomaly[0])

		return anomalies

	def get_anomalies_threshold(self, threshold):
		"""
		Returns anomalies that are above a certain threshold.
		"""
		anomalies = []

		for anomaly in self.anomaly_scores:
			if anomaly[1] > threshold:
				anomalies.append(anomaly[0])
			else:
				break

		return anomalies