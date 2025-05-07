#!/usr/bin/env python3
import csv
import json
import argparse
import os
import re


def parse_coordinates(coord_str):
    """Parse coordinate string formatted as '[lon, lat]' to [lon, lat] list."""
    # Check if the coordinate might be split across columns
    if coord_str.startswith('[') and not coord_str.endswith(']'):
        # This is a partial coordinate, return None to be handled later
        return None
        
    # Extract numbers from string using regex
    matches = re.findall(r'-?\d+\.\d+', coord_str)
    print(coord_str)
    if len(matches) == 2:
        return [float(matches[0]), float(matches[1])]
    else:
        raise ValueError(f"Invalid coordinate format: {coord_str}")


def csv_to_geojson(input_file, output_file, include_properties=True, create_linestring=True):
    """
    Convert CSV with GPS data to GeoJSON.
    
    Args:
        input_file (str): Path to input CSV file
        output_file (str): Path to output GeoJSON file
        include_properties (bool): Whether to include all properties in output
        create_linestring (bool): Whether to create a LineString in addition to Points
    """
    features = []
    linestring_coords = []
    
    with open(input_file, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        headers = next(csv_reader)  # Read the header row
        
        for row in csv_reader:
            try:
                # Handle case where coordinates are split across columns
                if 1==1:
                    # Combine first two columns to form the full coordinate string
                    lon_part = row[0].strip()
                    lat_part = row[1].strip()
                    
                    

                    # Extract the numbers
                    lon_match = re.search(r'-?\d+\.\d+', lon_part)
                    lat_match = re.search(r'-?\d+\.\d+', lat_part)


                    
                    if lon_match and lat_match:
                        lon = float(lon_match.group())
                        lat = float(lat_match.group())
                        coordinates = [lon, lat]
                        
                        # Shift all other columns
                        altitude = float(row[2].strip()) if len(row) > 2 and row[2] else None
                        speed = float(row[3].strip()) if len(row) > 3 and row[3] else None
                        
                        # Handle timestamp - ensure it's an integer if present
                        timestamp = None
                        if len(row) > 4 and row[4]:
                            try:
                                timestamp = int(float(row[4].strip()))
                            except ValueError:
                                timestamp = row[4].strip()
                        
                        # Handle "nan" values for course and variation
                        course = None
                        if len(row) > 5 and row[5]:
                            if row[5].strip().lower() == "nan":
                                course = None
                            else:
                                try:
                                    course = float(row[5].strip())
                                except ValueError:
                                    course = row[5].strip()
                        
                        variation = None
                        if len(row) > 6 and row[6]:
                            if row[6].strip().lower() == "nan":
                                variation = None
                            else:
                                try:
                                    variation = float(row[6].strip())
                                except ValueError:
                                    variation = row[6].strip()
                        
                        # Handle satellites
                        satellites = None
                        if len(row) > 7 and row[7]:
                            try:
                                satellites = int(row[7].strip())
                            except ValueError:
                                satellites = row[7].strip()
                    else:
                        raise ValueError(f"Could not extract coordinates from {lon_part} and {lat_part}")
                
                # Create point feature
                properties = {}
                if include_properties:
                    properties = {
                        "altitude": altitude,
                        "speed": speed,
                        "timestamp": timestamp,
                        "course": course,
                        "variation": variation,
                        "satellites": satellites
                    }
                point_feature = {
                    "type": "Feature",
                    "geometry": {
                        "type": "Point",
                        "coordinates": coordinates
                    },
                    "properties": properties
                }
                features.append(point_feature)
                
                # Add coordinates to linestring collection
                if create_linestring:
                    linestring_coords.append(coordinates)
                    
            except Exception as e:
                print(f"Error processing row: {row}")
                print(f"Error details: {e}")
    
    # Add LineString feature if requested
    if create_linestring and linestring_coords:
        linestring_feature = {
            "type": "Feature",
            "geometry": {
                "type": "LineString",
                "coordinates": linestring_coords
            },
            "properties": {
                "name": "Track",
                "points": len(linestring_coords)
            }
        }
        features.append(linestring_feature)
    
    # Create the final GeoJSON structure
    geojson = {
        "type": "FeatureCollection",
        "features": features
    }
    
    # Write to output file
    with open(output_file, 'w') as output:
        json.dump(geojson, output, indent=2)
    
    return len(features)


def main():
    parser = argparse.ArgumentParser(description='Convert GPS CSV data to GeoJSON')
    parser.add_argument('input', help='Input CSV file path')
    parser.add_argument('-o', '--output', help='Output GeoJSON file path')
    parser.add_argument('--no-properties', action='store_true', help='Exclude additional properties from output')
    parser.add_argument('--points-only', action='store_true', help='Create only Point features, no LineString')
    
    args = parser.parse_args()
    
    # If no output file specified, use the input filename with .geojson extension
    if not args.output:
        base_name = os.path.splitext(args.input)[0]
        args.output = f"{base_name}.geojson"
    
    feature_count = csv_to_geojson(
        args.input, 
        args.output, 
        include_properties=not args.no_properties,
        create_linestring=not args.points_only
    )
    
    print(f"Conversion complete! {feature_count} features written to {args.output}")


if __name__ == "__main__":
    main()
