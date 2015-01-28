# -*- coding: utf8 -*-
from __future__ import unicode_literals
__author__ = 'tsunami_team'
"""
Util geo functions
"""

import pandas as pd
from geopy.distance import vincenty


"""
Transform longitude & latitude into (longitude,latitude)
"""
def calc_coord(row):
    row['coordinates'] = (row['latitude'], row['longitude'])
    return row

"""
Calculate the coordinates of the centers of different GSM Zones
"""
def generate_GSM_zone_coordinates_CSV(data):
    GSM_Coord = data.groupby('GSM_code').mean()
    GSM_Coord = GSM_Coord.drop(['tel_num', 'timestamp','timeslot_cassandra'],axis=1)
    GSM_Coord = GSM_Coord.apply(lambda x : calc_coord(x), axis = 1)
    GSM_Coord.to_csv('../../dataset/GSM_Coord.csv', encoding='utf-8')


"""
Calculate distance between seism and a given coordinate
"""
def get_distance_to_seism(row, impact_coordinates):
    row['dist_from_seism'] = vincenty(row['coordinates'], impact_coordinates).miles
    return row

"""
Get all the GSM codes near the epicentre
"""
def get_GSM_codes_close_to_impact(latitude, longitude, km_range):
    GSMZone_dist = pd.read_csv('../../dataset/GSM_Coord.csv')
    impact_coord = (latitude, longitude)
    GSMZone_dist = GSMZone_dist.apply(lambda x : get_distance_to_seism(x, impact_coord), axis=1)
    GSMZone_dist = GSMZone_dist.sort(['dist_from_seism'],ascending=1)
    GSMZone_dist_500 = GSMZone_dist[GSMZone_dist['dist_from_seism'] <= km_range]
    return GSMZone_dist_500