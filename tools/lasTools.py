import laspy
import math
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from tools.voxelization import voxelize
from tools.voxelization import visualize_voxel_grid

def iterate_over_las(las_file : str, bound : int, voxel_size : float):

    """
    This function iterates through a .las file and returns a tuple consisting of a list of voxel grids, as well as a
    parallel list containing each voxel grid's x, y maximums and minimums
    """

    #Load LiDAR data
    las = laspy.read(las_file)
    print(las)

    #Recording the data in a numpy array
    point_data = np.stack([las.x, las.y, las.z, las.classification], axis = 0).transpose((1,0))
    print(point_data)

    XMIN = las.header.mins[0]
    XMAX = las.header.maxs[0]
    YMIN = las.header.mins[1]
    YMAX = las.header.maxs[1]
        
    print('looping...')

    #222 and 262 are arbitrary numbers that should be changed based on the las file

    #initialize a 222x262 2D array for the points
    boxes = []
    for i in range(222):
        boxes.append([])
        for j in range(262):
            boxes[i].append([])

    #initialize a 222x262 2D array for the colors
    colors = []
    for i in range(222):
        colors.append([])
        for j in range(262):
            colors[i].append([])

    for i in point_data:
        xIndex = math.floor((i[0] - XMIN)/bound)
        yIndex = math.floor((i[1] - YMIN)/bound)

        #Add the points and colors to boxes
        match i[3]:
            case 1:
                boxes[xIndex][yIndex].append([i[0], i[1], i[2], 0.416, 0.424, 0.471])
            case 2:
                boxes[xIndex][yIndex].append([i[0], i[1], i[2], 0.541, 0.357, 0.173])
            case 3:
                boxes[xIndex][yIndex].append([i[0], i[1], i[2], 0.329, 0.62, 0.8])
            case 4: 
                boxes[xIndex][yIndex].append([i[0], i[1], i[2], 0.137, 0.922, 0.216])
            case 5:
                boxes[xIndex][yIndex].append([i[0], i[1], i[2], 0.29, 0.69, 0.333])
            case 6:
                boxes[xIndex][yIndex].append([i[0], i[1], i[2], 0.922, 0.149, 0.149])
            case 7:
                boxes[xIndex][yIndex].append([i[0], i[1], i[2], 0.541, 0.145, 0.145])
            case 8: 
                boxes[xIndex][yIndex].append([i[0], i[1], i[2], 0.165, 0.843, 0.878])
            case 9:
                boxes[xIndex][yIndex].append([i[0], i[1], i[2], 0.898, 0.941, 0.192])
            case 10:
                boxes[xIndex][yIndex].append([i[0], i[1], i[2], 0.337, 0.251, 0.749])
            case 11:
                boxes[xIndex][yIndex].append([i[0], i[1], i[2], 0.282, 0.286, 0.322])
            case 12: 
                boxes[xIndex][yIndex].append([i[0], i[1], i[2], 0.949, 0.314, 0.651])

    #Initialize x,y,z, and colors lists
    x_data = []
    y_data = []
    z_data = []
    colors = []
    voxel_grid_list = []
    xy = []
    count = 0
    for i in boxes:
        count += 1
        if count == 20:
            break
        for j in i:
            #Clear the lists when moving to a new box
            x_data.clear()
            y_data.clear()
            z_data.clear()
            colors.clear()
            for k in j:
                #fill the lists with all the values in the current box
                x_data.append(k[0])
                y_data.append(k[1])
                z_data.append(k[2])
                colors.append([k[3],k[4], k[5]])
                if k[3] == 0.137 or k[3] == 0.29:
                    green = True
            
            #If there is no x or y data, or if the boxe's x or y length is short it means we are on an edge piece and we should skip
            if(len(x_data) == 0 or len(y_data) == 0 or max(x_data) - min(x_data) <  (bound - 2) or max(y_data) - min(y_data) < (bound - 2)):
                continue
            
            # Print the data of the current box
            # print('point count: ', len(x_data))
            # print('xmin: ', min(x_data), 'xmax: ', max(x_data), 'diff: ', max(x_data) - min(x_data))
            # print('ymin: ', min(y_data), 'ymax: ', max(y_data), 'diff: ', max(y_data) - min(y_data))
            # print('zmin: ', min(z_data), 'zmax: ', max(z_data), 'diff: ', max(z_data) - min(z_data))

            
            # #draw the points using matplotlib
            # fig = plt.figure(figsize=(5, 5))
            # ax = fig.add_subplot(111, projection="3d")
            # ax.scatter(x_data, y_data, z_data)
            # ax.set_axis_off()
            # plt.show()

            #voxelize
            points = []
            xmin = min(x_data)
            ymin = min(y_data)
            zmin = min(z_data)
            for i in range(len(x_data)):
                points.append([x_data[i] - xmin, y_data[i] - ymin, z_data[i] - zmin])

            xy.append([min(x_data), min(y_data), max(x_data), max(y_data)])
            voxel_grid_list.append(voxelize(points, colors, voxel_size, bound))

    
    return (voxel_grid_list, xy)

def get_voxelization(xmin : float, ymin: float, bound : int, voxel_size : float, las_file : str):
    """
    Given a x and y coordinate, a voxel grid is constructed of size bound x bound x bound whose origin is xmin and ymin.
    The voxel grid is returned
    """
    xmax = xmin + bound
    ymax = ymin + bound
    las = laspy.read(las_file)
    #Recording the data in a numpy array
    point_data = np.stack([las.x, las.y, las.z, las.classification], axis = 0).transpose((1,0))

    x_data = []
    y_data = []
    z_data = []
    colors = []
    l = []
    for i in point_data:
        if i[0] > xmin and i[0] <  xmax and i[1] > ymin and i[1] < ymax:
            if i[3] == 5:
                l.append(i[2])
            x_data.append(i[0])
            y_data.append(i[1])
            z_data.append(i[2])
            match i[3]:
                case 1:
                    colors.append([0.416, 0.424, 0.471])
                case 2:
                    colors.append([0.541, 0.357, 0.173])
                case 3:
                    colors.append([0.329, 0.62, 0.8])
                case 4: 
                    colors.append([0.137, 0.922, 0.216])
                case 5:
                    colors.append([0.29, 0.69, 0.333])
                case 6:
                    colors.append([0.922, 0.149, 0.149])
                case 7:
                    colors.append([0.541, 0.145, 0.145])
                case 8: 
                    colors.append([0.165, 0.843, 0.878])
                case 9:
                    colors.append([0.898, 0.941, 0.192])
                case 10:
                    colors.append([0.337, 0.251, 0.749])
                case 11:
                    colors.append([0.282, 0.286, 0.322])
                case 12: 
                    colors.append([0.949, 0.314, 0.651])
                case _:
                    colors.append([0, 0, 0])

    points = []
    zmin = min(z_data)
    for i in range(len(x_data)):
        points.append([x_data[i] - xmin, y_data[i] - ymin, z_data[i] - zmin])
    voxel = voxelize(points, colors, voxel_size, bound)

    return voxel