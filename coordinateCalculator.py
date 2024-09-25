import psycopg2
import numpy as np


def find_distance(height):
    print(f"Distance: {-16.10 * height + 2875}")
    return -16.10 * height + 2875


def find_angle(monitor_x_position):
    pixels_from_center = monitor_x_position - 1280  # Assuming 1280 is the screen center
    angle = pixels_from_center * 0.04376
    print(f"Angle: {angle}")
    return angle


def push_to_database(x_coordinate, y_coordinate):
    global connection, cursor
    try:
        connection = psycopg2.connect(
            # Users who have gotten this repo from GitHub can input their personal PostgreSQL database info here
            user="coordinate_user",
            password="",
            host="127.0.0.1",
            port="5432",
            database="coordinates_db"
        )

        # The cursor can traverse the rows including inserting
        cursor = connection.cursor()

        insert_query = """INSERT INTO predicted_coordinates (x_coordinate, y_coordinate) VALUES (%s, %s)"""
        cursor.execute(insert_query, (x_coordinate, y_coordinate))

        # Confirms changes
        connection.commit()

        print(f"Coordinates ({x_coordinate}, {y_coordinate}) inserted successfully.")

    except Exception as error:
        print(f"Error inserting coordinates: {error}")
    finally:
        if connection:
            cursor.close()
            connection.close()


def predict_coordinates(height, monitor_x_position, current_coordinates):
    distance = find_distance(height)
    angle = find_angle(monitor_x_position)

    if distance < 0:
        distance = 0

    # Parse the current_coordinates string into a list of floats
    current_coordinates_list = list(map(float, current_coordinates.split(',')))
    print(f"Parsed coordinates: {current_coordinates_list}")

    current_x = current_coordinates_list[0]
    current_y = current_coordinates_list[1]
    yaw = current_coordinates_list[3]

    # Make yaw a 0-360 degree value rather than 180 to -180
    if yaw < 0:
        yaw = 360 + yaw

    angle_of_distance = yaw + angle

    # Force the angle_of_distance to be within 360
    angle_of_distance = angle_of_distance % 360

    predicted_x = 0
    predicted_y = 0

    # Calculate the angle with respect to the X-axis based on the quadrant (the four quadrants on a graph in math)
    if angle_of_distance < 90:
        # First quadrant
        angle_to_x_axis_from_distance = 90 - angle_of_distance
        angle_to_x_axis_from_distance = np.radians(angle_to_x_axis_from_distance)
        predicted_y = np.cos(angle_to_x_axis_from_distance) * distance
        predicted_x = np.sin(angle_to_x_axis_from_distance) * distance
        print(f"Q1: Predicted x {predicted_x}, Predicted y {predicted_y}")
    elif angle_of_distance < 180:
        # Fourth quadrant
        angle_to_x_axis_from_distance = angle_of_distance - 90
        angle_to_x_axis_from_distance = np.radians(angle_to_x_axis_from_distance)
        predicted_y = np.cos(angle_to_x_axis_from_distance) * distance
        predicted_x = np.sin(angle_to_x_axis_from_distance) * distance
        print(f"Q4: Predicted x {predicted_x}, Predicted y {predicted_y}")
    elif angle_of_distance < 270:
        # Third quadrant
        angle_to_x_axis_from_distance = 270 - angle_of_distance
        angle_to_x_axis_from_distance = np.radians(angle_to_x_axis_from_distance)
        predicted_y = np.cos(angle_to_x_axis_from_distance) * distance
        predicted_x = np.sin(angle_to_x_axis_from_distance) * distance
        print(f"Q3: Predicted x {predicted_x}, Predicted y {predicted_y}")
    else:
        # Second quadrant
        angle_to_x_axis_from_distance = angle_of_distance - 270
        angle_to_x_axis_from_distance = np.radians(angle_to_x_axis_from_distance)
        predicted_y = np.cos(angle_to_x_axis_from_distance) * distance
        predicted_x = np.sin(angle_to_x_axis_from_distance) * distance
        print(f"Q2: Predicted x {predicted_x}, Predicted y {predicted_y}")

    push_to_database(predicted_x + current_x, predicted_y + current_y)

    return [predicted_x + current_x, predicted_y + current_y]
