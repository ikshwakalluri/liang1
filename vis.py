import laspy

# Open the LASer file
las = laspy.read("D:\Projects\Liang1/unt2.las")

# Access header information
header = las.header

# Access point data
points = las.points
print(len(points))
# Iterate over each point
data = {"sdf": 1, "key": "sd"}
