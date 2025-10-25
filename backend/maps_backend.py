from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
from functools import wraps

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend requests

# Store API key securely - use environment variable in production
GOOGLE_MAPS_API_KEY = os.getenv('GOOGLE_MAPS_API_KEY', 'a84c4a92cc9e4e1f9374d8ab09897b78')

def handle_errors(f):
    """Decorator to handle errors consistently"""
    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    return wrapper

@app.route('/api/maps/geocode', methods=['GET'])
@handle_errors
def geocode():
    """Convert address to coordinates"""
    address = request.args.get('address')
    if not address:
        return jsonify({'error': 'Address parameter is required'}), 400
    
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'address': address,
        'key': GOOGLE_MAPS_API_KEY
    }
    
    response = requests.get(url, params=params)
    return jsonify(response.json())

@app.route('/api/maps/reverse-geocode', methods=['GET'])
@handle_errors
def reverse_geocode():
    """Convert coordinates to address"""
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    
    if not lat or not lng:
        return jsonify({'error': 'lat and lng parameters are required'}), 400
    
    url = 'https://maps.googleapis.com/maps/api/geocode/json'
    params = {
        'latlng': f'{lat},{lng}',
        'key': GOOGLE_MAPS_API_KEY
    }
    
    response = requests.get(url, params=params)
    return jsonify(response.json())

@app.route('/api/maps/directions', methods=['GET'])
@handle_errors
def directions():
    """Get directions between two points"""
    origin = request.args.get('origin')
    destination = request.args.get('destination')
    mode = request.args.get('mode', 'driving')  # driving, walking, bicycling, transit
    
    if not origin or not destination:
        return jsonify({'error': 'origin and destination parameters are required'}), 400
    
    url = 'https://maps.googleapis.com/maps/api/directions/json'
    params = {
        'origin': origin,
        'destination': destination,
        'mode': mode,
        'key': GOOGLE_MAPS_API_KEY
    }
    
    response = requests.get(url, params=params)
    return jsonify(response.json())

@app.route('/api/maps/places/nearby', methods=['GET'])
@handle_errors
def nearby_search():
    """Search for nearby places"""
    lat = request.args.get('lat')
    lng = request.args.get('lng')
    radius = request.args.get('radius', 1500)  # meters
    place_type = request.args.get('type', 'restaurant')
    
    if not lat or not lng:
        return jsonify({'error': 'lat and lng parameters are required'}), 400
    
    url = 'https://maps.googleapis.com/maps/api/place/nearbysearch/json'
    params = {
        'location': f'{lat},{lng}',
        'radius': radius,
        'type': place_type,
        'key': GOOGLE_MAPS_API_KEY
    }
    
    response = requests.get(url, params=params)
    return jsonify(response.json())

@app.route('/api/maps/places/details', methods=['GET'])
@handle_errors
def place_details():
    """Get details about a specific place"""
    place_id = request.args.get('place_id')
    
    if not place_id:
        return jsonify({'error': 'place_id parameter is required'}), 400
    
    url = 'https://maps.googleapis.com/maps/api/place/details/json'
    params = {
        'place_id': place_id,
        'key': GOOGLE_MAPS_API_KEY
    }
    
    response = requests.get(url, params=params)
    return jsonify(response.json())

@app.route('/api/maps/distance-matrix', methods=['GET'])
@handle_errors
def distance_matrix():
    """Calculate distance and time between multiple origins and destinations"""
    origins = request.args.get('origins')
    destinations = request.args.get('destinations')
    mode = request.args.get('mode', 'driving')
    
    if not origins or not destinations:
        return jsonify({'error': 'origins and destinations parameters are required'}), 400
    
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    params = {
        'origins': origins,
        'destinations': destinations,
        'mode': mode,
        'key': GOOGLE_MAPS_API_KEY
    }
    
    response = requests.get(url, params=params)
    return jsonify(response.json())

@app.route('/api/maps/api-key', methods=['GET'])
def get_api_key():
    """Provide API key for frontend (use with caution - consider restrictions)"""
    return jsonify({'api_key': GOOGLE_MAPS_API_KEY})

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)