import streamlit as st
import openrouteservice
from openrouteservice import convert
import pandas as pd
import numpy as np

# Function to get directions
def get_directions(client, coordinates):
    routes = client.directions(coordinates=coordinates, profile='driving-car', format='geojson')
    return routes

# Function to calculate time-distance matrix
def get_matrix(client, locations):
    matrix = client.distance_matrix(locations, profile='driving-car', metrics=['distance', 'duration'])
    return matrix

# Function to perform optimization
def optimize_route(client, jobs, vehicles):
    result = client.optimization(jobs=jobs, vehicles=vehicles)
    return result

st.title("Open Route Service App")

api_key = st.text_input("Enter your OpenRouteService API key:")

if api_key:
    client = openrouteservice.Client(key=api_key)

    st.header("Get Directions")
    start_lat = st.number_input("Start Latitude", value=0.0)
    start_lon = st.number_input("Start Longitude", value=0.0)
    end_lat = st.number_input("End Latitude", value=0.0)
    end_lon = st.number_input("End Longitude", value=0.0)
    
    if st.button("Get Directions"):
        coordinates = [[start_lon, start_lat], [end_lon, end_lat]]
        routes = get_directions(client, coordinates)
        st.json(routes)

    st.header("Calculate Time-Distance Matrix")
    locations_input = st.text_area("Enter locations as lat,lon (one per line):")
    locations = []
    if locations_input:
        locations = [list(map(float, loc.split(','))) for loc in locations_input.split('\n')]
    
    if st.button("Calculate Matrix"):
        if len(locations) > 1:
            matrix = get_matrix(client, locations)
            st.json(matrix)
        else:
            st.warning("Enter at least two locations.")

    st.header("Route Optimization")
    jobs_input = st.text_area("Enter jobs as id, lat, lon (one per line):")
    vehicles_input = st.text_area("Enter vehicles as id, start_lat, start_lon, end_lat, end_lon, capacity:")
    
    jobs = []
    vehicles = []
    
    if jobs_input:
        jobs = [{'id': int(job.split(',')[0]), 'location': [float(job.split(',')[2]), float(job.split(',')[1])]} for job in jobs_input.split('\n')]
    
    if vehicles_input:
        vehicles = [{'id': int(veh.split(',')[0]), 'start': [float(veh.split(',')[2]), float(veh.split(',')[1])], 
                    'end': [float(veh.split(',')[4]), float(veh.split(',')[3])], 'capacity': [int(veh.split(',')[5])]} for veh in vehicles_input.split('\n')]

    if st.button("Optimize Route"):
        if jobs and vehicles:
            result = optimize_route(client, jobs, vehicles)
            st.json(result)
        else:
            st.warning("Enter at least one job and one vehicle.")
