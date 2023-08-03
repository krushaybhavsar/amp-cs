import math


def get_radius():
    radius = input("Enter the radius of a circle (mm): ")
    return float(radius)


def calculate_circumference(radius):
    return 2 * radius * math.pi


def calculate_area(radius):
    return math.pi * radius**2


def calculate_distance(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


if __name__ == "__main__":
    radius = get_radius()

    circumference = calculate_circumference(radius)
    print(
        f"A circle with radius {radius}mm has a circumference of {round(circumference, 3)}mm"
    )

    area = calculate_area(radius)
    print(f"A circle with radius {radius}mm has an area of {round(area, 3)}mm\u00b2")

    x1, y1 = 3, 4
    x2, y2 = 0, 0
    distance = calculate_distance(x1, y1, x2, y2)
    print(f"The distance between ({x1}, {y1}) and ({x2}, {y2}) is {distance}")
