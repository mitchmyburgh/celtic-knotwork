import math


##The writeSTL functions all produce an STL file from an array of data, but each takes an array with data at a different depth
def writeSTL(name, fname, data):
    '''Writes STL file from data, where data[i] contains all the triangles in one shape'''
    file = open(fname, "w")

    
    file.write("solid "+name+"\n")


    for i in range(len(data)):
        file.write("\tfacet normal"+str(data[i][0][0])+" "+str(data[i][0][1])+" "+str(data[i][0][2])+"\n")
        file.write("\t\touter loop\n")
        
        for j in range(len(data[0])-1):
            j+= 1
            file.write("\t\t\tvertex "+str(data[i][j][0])+" "+str(data[i][j][1])+" "+str(data[i][j][2])+"\n")
            

        file.write("\t\tendloop\n")
        file.write("\tendfacet\n")
            



    
    file.write("endsolid "+name)
    
    file.close()
def writeSTL2(name, fname, data):
    '''Writes STL file from data, where data[k][i] contains all the triangles in one shape'''
    file = open(fname, "w")
    for k in range(len(data)):
    
        file.write("solid "+str(k)+"\n")


        for i in range(len(data[0])):
            file.write("\tfacet normal"+str(data[k][i][0][0])+" "+str(data[k][i][0][1])+" "+str(data[k][i][0][2])+"\n")
            file.write("\t\touter loop\n")
            
            for j in range(len(data[0][0])-1):
                j+= 1
                file.write("\t\t\tvertex "+str(data[k][i][j][0])+" "+str(data[k][i][j][1])+" "+str(data[k][i][j][2])+"\n")
                

            file.write("\t\tendloop\n")
            file.write("\tendfacet\n")
                



        
        file.write("endsolid "+name)
    
    file.close()
def writeSTL3(name, fname, data):
    '''Writes STL file from data, where data[k][c][i] contains all the triangles in one shape'''
    file = open(fname, "w")
    for k in range(len(data)):
        for c in range(len(data[k])):
    
                file.write("solid "+str(k)+"\n")


                for i in range(len(data[k][c])):
                    file.write("\tfacet normal"+str(data[k][c][i][0][0])+" "+str(data[k][c][i][0][1])+" "+str(data[k][c][i][0][2])+"\n")
                    file.write("\t\touter loop\n")
                    
                    for j in range(len(data[k][c][i])-1):
                        j+= 1
                        file.write("\t\t\tvertex "+str(data[k][c][i][j][0])+" "+str(data[k][c][i][j][1])+" "+str(data[k][c][i][j][2])+"\n")
                        

                    file.write("\t\tendloop\n")
                    file.write("\tendfacet\n")
                        



                
                file.write("endsolid "+name)
            
    file.close()

def genCirclePoints(n, rad):
    '''Generates the points around a circle'''
    points = []
    deg = 2*math.pi/n
    print(deg)
    for i in range (n):
        points.append([])
        x1 = rad*math.sin(deg*i)
        y1 = rad*math.cos(deg*i)
        x2 = rad*math.sin(deg*(i+1))
        y2 = rad*math.cos(deg*(i+1))
        points[i].append([0,0,0])
        
        points[i].append([float("{0:.2f}".format(x1)),float("{0:.2f}".format(y1)),0])
        points[i].append([0,0,0])
        points[i].append([float("{0:.2f}".format(x2)),float("{0:.2f}".format(y2)),0])
    print(points)
    return points
def genCylinderPoints(n, rad, length):
    '''Generates a cylinder with circular cross section'''
    points = genCirclePoints(n, rad)
    points2 = []
    for i in range(n):
        points2.append([])

        points2[i*2].append(points[i][0])
        points2[i*2].append(points[i][1])
        points2[i*2].append([points[i][1][0], points[i][1][1], length])
        points2[i*2].append(points[i][3])
        points2.append([])
        points2[i*2+1].append(points[i][0])
        points2[i*2+1].append([points[i][1][0], points[i][1][1], length])
        points2[i*2+1].append([points[i][3][0], points[i][3][1], length])
        points2[i*2+1].append(points[i][3])
    return points2
            
def genRoundedRectanglePoints(x, y, width, height, radius, n):
    '''Generates a rounded rectangle (unrotated)'''
    circOrigin=[[x+ width/2-radius, y +height/2-radius, 0], [x- width/2+radius, y +height/2-radius, 0], [x- width/2+radius, y -height/2+radius, 0], [x+ width/2-radius, y -height/2+radius, 0]]
    points = []
    for i in range(6):
        points.append([])

    ##TODO go over these with right hand rule
    points[0].append([0,0,0])
    points[0].append([x- width/2+radius, y -height/2, 0])
    points[0].append([x+ width/2-radius, y -height/2, 0])
    points[0].append([x- width/2+radius, y +height/2, 0])

    points[1].append([0,0,0])
    points[1].append([x+width/2-radius, y +height/2, 0])
    points[1].append([x- width/2+radius, y +height/2, 0])
    points[1].append([x+ width/2-radius, y -height/2, 0])

    points[2].append([0,0,0])
    points[2].append([x-width/2, y +height/2-radius, 0])
    points[2].append([x- width/2, y -height/2+radius, 0])
    points[2].append([x- width/2+radius, y +height/2-radius, 0])

    points[3].append([0,0,0])
    points[3].append([x-width/2+radius, y +height/2-radius, 0])
    points[3].append([x- width/2, y -height/2+radius, 0])
    points[3].append([x- width/2+radius, y -height/2+radius, 0])

    points[4].append([0,0,0])
    points[4].append([x+width/2-radius, y +height/2-radius, 0])
    points[4].append([x+ width/2-radius, y -height/2+radius, 0])
    points[4].append([x+width/2, y -height/2+radius, 0])

    points[5].append([0,0,0])
    points[5].append([x+width/2, y +height/2-radius, 0])
    points[5].append([x+ width/2-radius, y +height/2-radius, 0])
    points[5].append([x+ width/2, y -height/2+radius, 0])

    deg = (math.pi/2)/n
    rad = radius
    for j in range(4):
        for i in range(n):
            points.append([])
            points[6+j*n+i].append([0,0,0])
            deg = (math.pi/2)/n
            if (j == 0):
                x1 = rad*math.sin(deg*i) + width/2 - rad
                y1 = rad*math.cos(deg*i) + height/2 - rad
                x2 = rad*math.sin(deg*(i+1)) + width/2 - rad
                y2 = rad*math.cos(deg*(i+1)) +height/2 - rad
            if (j == 1):
                x1 = rad*math.sin(deg*i -math.pi/2) - width/2 +rad
                y1 = rad*math.cos(deg*i -math.pi/2) + height/2 - rad
                x2 = rad*math.sin(deg*(i+1)-math.pi/2) - width/2 +rad
                y2 = rad*math.cos(deg*(i+1)-math.pi/2) +height/2 - rad
            if (j == 2):
                x1 = rad*math.sin(deg*i-math.pi*2/2) -width/2 + rad
                y1 = rad*math.cos(deg*i-math.pi*2/2) - height/2 + rad
                x2 = rad*math.sin(deg*(i+1)-math.pi*2/2) - width/2 + rad
                y2 = rad*math.cos(deg*(i+1)-math.pi*2/2) -height/2 + rad
            if (j == 3):
                x1 = rad*math.sin(deg*i - math.pi*3/2) + width/2 - rad
                y1 = rad*math.cos(deg*i- math.pi*3/2) - height/2 +rad
                x2 = rad*math.sin(deg*(i+1)- math.pi*3/2) + width/2 - rad
                y2 = rad*math.cos(deg*(i+1)- math.pi*3/2) -height/2 +rad
            
            points[6+j*n+i].append([float("{0:.2f}".format(x1)),float("{0:.2f}".format(y1)),0])
            points[6+j*n+i].append(circOrigin[j])
            points[6+j*n+i].append([float("{0:.2f}".format(x2)),float("{0:.2f}".format(y2)),0])
    print(points)
        
    return points

def rotatePoints(x, y, z, anglex,angley, anglez, homex, homey, homez):
    '''Rotates point at (x, y, z) around (homex, homey, homez) by angle (anglex, angley, anglez)'''
    rotx =  [x, (y-homey)*math.cos(anglex)-(z-homez)*math.sin(anglex)+homey, (x-homey)*math.sin(anglex)+(z-homez)*math.cos(anglex)+homez]
    roty = [(rotx[0]-homex)*math.cos(angley)+(rotx[2]-homez)*math.sin(angley)+homex, rotx[1], (rotx[2]-homez)*math.cos(angley)-(rotx[0]-homex)*math.sin(angley) + homez]
    rotz = [(roty[0]-homex)*math.cos(anglez)-(roty[1]-homey)*math.sin(anglez)+homex,(roty[0]-homex)*math.sin(anglez)+(roty[1]-homey)*math.cos(anglez)+homey, roty[2]]
    return rotz



def genRoundedRectanglePointsRotate(x, y, z, width, height, radius, n, angle1, angle2, angle3):
    '''Generates a rounded rectangle at (x,y,z) with width, height and radius of corners (divided into n segments), rotated by angle (angle1, angle2, angle3)'''

    ##Rotate the origin of each circle for the corners
    circOrigin = [rotatePoints(x+ width/2-radius, y +height/2-radius, 0,  angle1, angle2, angle3,  x, y, z),rotatePoints(x- width/2+radius, y +height/2-radius, 0,  angle1, angle2, angle3,  x, y, z),rotatePoints(x- width/2+radius, y -height/2+radius, 0,  angle1, angle2, angle3,  x, y, z), rotatePoints(x+ width/2-radius, y -height/2+radius, 0,  angle1, angle2, angle3,  x, y, z)]


    points = []
    for i in range(6):
        points.append([])

    points[0].append([0,0,0])

    ##add the ractangles on the inside of the shape
    a = rotatePoints(x- width/2+radius, y -height/2, 0,  angle1, angle2, angle3,  x, y, z)
    points[0].append(a)
    a = rotatePoints(x+ width/2-radius, y -height/2,0,  angle1,angle2,  angle3,x, y, z)
    points[0].append(a)
    a= rotatePoints(x- width/2+radius,  y +height/2,0,  angle1,angle2,  angle3,x, y, z)
    points[0].append(a)

    points[1].append([0,0,0])
    a = rotatePoints(x+width/2-radius, y +height/2, 0,  angle1, angle2,  angle3, x, y, z)
    points[1].append(a)
    a = rotatePoints(x- width/2+radius, y +height/2,0,  angle1,angle2,  angle3,x, y, z)
    points[1].append(a)
    a= rotatePoints(x+ width/2-radius,  y -height/2,0,  angle1,angle2, angle3, x, y, z)
    points[1].append(a)


    points[2].append([0,0,0])
    a = rotatePoints(x-width/2, y +height/2-radius, 0,  angle1, angle2,  angle3, x, y, z)
    points[2].append(a)
    a = rotatePoints(x- width/2, y -height/2+radius,0,  angle1,angle2, angle3, x, y, z)
    points[2].append(a)
    a= rotatePoints(x- width/2+radius, y +height/2-radius,0,  angle1,angle2, angle3, x, y, z)
    points[2].append(a)


    points[3].append([0,0,0])
    a = rotatePoints(x-width/2+radius, y +height/2-radius, 0,  angle1, angle2, angle3,  x, y, z)
    points[3].append(a)
    a = rotatePoints(x- width/2, y -height/2+radius,0,  angle1,angle2, angle3, x, y, z)
    points[3].append(a)
    a= rotatePoints(x- width/2+radius, y -height/2+radius,0,  angle1,angle2, angle3, x, y, z)
    points[3].append(a)

    points[4].append([0,0,0])
    a = rotatePoints(x+width/2-radius, y +height/2-radius, 0,  angle1, angle2, angle3,  x, y, z)
    points[4].append(a)
    a = rotatePoints(x+ width/2-radius, y -height/2+radius,0,  angle1,angle2, angle3, x, y, z)
    points[4].append(a)
    a= rotatePoints(x+width/2, y -height/2+radius,0,  angle1,angle2, angle3, x, y, z)
    points[4].append(a)


    points[5].append([0,0,0])
    a = rotatePoints(x+width/2, y +height/2-radius, 0,  angle1, angle2, angle3,  x, y, z)
    points[5].append(a)
    a = rotatePoints(x+ width/2-radius, y +height/2-radius,0,  angle1,angle2, angle3, x, y, z)
    points[5].append(a)
    a= rotatePoints(x+ width/2, y -height/2+radius,0,  angle1,angle2, angle3, x, y, z)
    points[5].append(a)


    deg = (math.pi/2)/n
    rad = radius

    ## add the rounded corners    
    for j in range(4):
        for i in range(n):
            points.append([])
            points[6+j*n+i].append([0,0,0])
            deg = (math.pi/2)/n
            
            if (j == 0):
                x1 = rad*math.sin(deg*i) + x +width/2 - rad
                y1 = rad*math.cos(deg*i) + y +height/2 - rad
                x2 = rad*math.sin(deg*(i+1)) +x+ width/2 - rad
                y2 = rad*math.cos(deg*(i+1)) + y+height/2 - rad
            if (j == 1):
                x1 = rad*math.sin(deg*i -math.pi/2) +x- width/2 +rad
                y1 = rad*math.cos(deg*i -math.pi/2)+y + height/2 - rad
                x2 = rad*math.sin(deg*(i+1)-math.pi/2)+x - width/2 +rad
                y2 = rad*math.cos(deg*(i+1)-math.pi/2)+y +height/2 - rad

            if (j == 2):
                x1 = rad*math.sin(deg*i-math.pi*2/2) +x-width/2 + rad
                y1 = rad*math.cos(deg*i-math.pi*2/2) +y- height/2 + rad
                x2 = rad*math.sin(deg*(i+1)-math.pi*2/2)+x - width/2 + rad
                y2 = rad*math.cos(deg*(i+1)-math.pi*2/2) +y-height/2 + rad
            if (j == 3):
                x1 = rad*math.sin(deg*i - math.pi*3/2)+x + width/2 - rad
                y1 = rad*math.cos(deg*i- math.pi*3/2) +y- height/2 +rad
                x2 = rad*math.sin(deg*(i+1)- math.pi*3/2)+x + width/2 - rad
                y2 = rad*math.cos(deg*(i+1)- math.pi*3/2) +y-height/2 +rad

            ##Rotate and add teh points to the array
            a = rotatePoints(x1, y1,0,  angle1,angle2, angle3, x, y, z)            
            points[6+j*n+i].append([float("{0:.2f}".format(a[0])),float("{0:.2f}".format(a[1])),a[2]])
            points[6+j*n+i].append(circOrigin[j])
            points[6+j*n+i].append([float("{0:.2f}".format(rotatePoints(x2, y2,0,  angle1,angle2, angle3, x, y, z)[0])),float("{0:.2f}".format(rotatePoints(x2, y2,0,  angle1,angle2, angle3, x, y, z)[1])),rotatePoints(x2, y2,0,  angle1,angle2, angle3, x, y, z)[2]])

    return points


def genRoundedRectanglePointsRotateSkel(x, y, z, width, height, radius, n, angle1, angle2, angle3):
    '''Generates the points around the edge of a rounded rectangle at (x,y,z) with width, height and radius of corners (divided into n straight lines) rotated by (angle1, angle2, angle3)'''
    circOrigin = [rotatePoints(x+ width/2-radius, y +height/2-radius, 0,  angle1, angle2, angle3,  x, y, z),rotatePoints(x- width/2+radius, y +height/2-radius, 0,  angle1, angle2, angle3,  x, y, z),rotatePoints(x- width/2+radius, y -height/2+radius, 0,  angle1, angle2, angle3,  x, y, z), rotatePoints(x+ width/2-radius, y -height/2+radius, 0,  angle1, angle2, angle3,  x, y, z)]

    points = []

    deg = (math.pi/2)/n
    rad = radius

    ##Generate the points
    for j in range(4):
        for i in range(n):
            deg = (math.pi/2)/n
            
            if (j == 0):
                x1 = rad*math.sin(deg*i) + x +width/2 - rad
                y1 = rad*math.cos(deg*i) + y +height/2 - rad
                x2 = rad*math.sin(deg*(i+1)) +x+ width/2 - rad
                y2 = rad*math.cos(deg*(i+1)) + y+height/2 - rad
            if (j == 3):
                x1 = rad*math.sin(deg*i + math.pi*3/2) +x- width/2 +rad
                y1 = rad*math.cos(deg*i + math.pi*3/2 )+y + height/2 - rad
                x2 = rad*math.sin(deg*(i+1) + math.pi*3/2)+x - width/2 +rad
                y2 = rad*math.cos( deg*(i+1) + math.pi*3/2)+y +height/2 - rad

            if (j == 2):
                x1 = rad*math.sin(deg*i+math.pi*2/2) +x-width/2 + rad
                y1 = rad*math.cos(deg*i+math.pi*2/2) +y- height/2 + rad
                x2 = rad*math.sin(deg*(i+1)+math.pi*2/2)+x - width/2 + rad
                y2 = rad*math.cos(deg*(i+1)+math.pi*2/2) +y-height/2 + rad
            if (j == 1):
                x1 = rad*math.sin(deg*i + math.pi/2)+x + width/2 - rad
                y1 = rad*math.cos(deg*i+ math.pi/2) +y- height/2 +rad
                x2 = rad*math.sin(deg*(i+1)+ math.pi/2)+x + width/2 - rad
                y2 = rad*math.cos(deg*(i+1)+ math.pi/2) +y-height/2 +rad

                

            a = rotatePoints(x1, y1,0,  angle1,angle2, angle3, x, y, z)
            
            points.append([float("{0:.2f}".format(a[0])),float("{0:.2f}".format(a[1])),a[2]])
            if (i == n-1): ##close the loop
                points.append([float("{0:.2f}".format(rotatePoints(x2, y2,0,  angle1,angle2, angle3, x, y, z)[0])),float("{0:.2f}".format(rotatePoints(x2, y2,0,  angle1,angle2, angle3, x, y, z)[1])),rotatePoints(x2, y2,0,  angle1,angle2, angle3, x, y, z)[2]])

    return points



##The following functions produce slightly different results to genCyl3. The first takes an array of points that is not divided by band, and the second only generates cross sections and does not join them together.
##def genCyl(points_, width, height, radius, n):
##    '''Generate the 3D model with cross sections from points_ with width height and radius of corners (divided into n triangles) and save it to file'''
##    cyls = []
##    cyl = []
##    print("PRINTING N")
##    print(n)
##    for i in range(len(points_)):
##        print(points_[i])
##        x = points_[i][0]
##        y = points_[i][1]
##        z = points_[i][2]
##        print(y)
##        cyl =  genRoundedRectanglePointsRotate(x,y,z, width, height, radius, n, points_[i][3],points_[i][4],points_[i][5])
##        
##        for j in range(len(cyl)):
##            cyls.append(cyl[j])
##    writeSTL("bob3", "test4.stl", cyls)
##
##
##def genCyl2(points_, width, height, radius, n):
##    '''Generate the 3D model with cross sections from points_ with width height and radius of corners (divided into n triangles) and save it to file'''
##    cyls = []
##    cyl = []
##
##    for i in range(len(points_)):
##
##        for j in range(len(points_[i])):
##
##            x = points_[i][j][0]
##            y = points_[i][j][1]
##            z = points_[i][j][2]
##
##            cyl =  genRoundedRectanglePointsRotate(x,y,z, width, height, radius, n, points_[i][j][3],points_[i][j][4],points_[i][j][5])
##            cyls.append(cyl)
##
##    writeSTL2("bob3", "test4.stl", cyls)

def genTubes(points):
    '''Generates the connections between the cross sections described in points'''

    tubes = []
    for i in range(len(points)):
        tubes.append([])
        for j in range(len(points[i])):
            tubes[i].append([])
            for k in range(len(points[i][j])):

                if (j+1 <len(points[i])):
                    if (k+1 <len(points[i][j])):
                        a = [[0,0,0], points[i][j][k], points[i][j][k+1], points[i][j+1][k]]
                        a2 = [[0,0,0], points[i][j+1][k], points[i][j][k+1], points[i][j+1][k+1]]
                        tubes[i][j].append(a)
                        tubes[i][j].append(a2)
                    elif (k+1 == len(points[i][j])):
                        a = [[0,0,0], points[i][j][k], points[i][j][0], points[i][j+1][k]]
                        a2 = [[0,0,0], points[i][j+1][k], points[i][j][0], points[i][j+1][0]]
                        tubes[i][j].append(a)
                        tubes[i][j].append(a2)
                elif (j+1 == len(points[i])):
                    if (k+1 <len(points[i][j])):
                        a = [[0,0,0], points[i][j][k], points[i][j][k+1], points[i][0][k]]
                        a2 = [[0,0,0], points[i][0][k], points[i][j][k+1], points[i][0][k+1]]
                        tubes[i][j].append(a)
                        tubes[i][j].append(a2)
                    elif (k+1 == len(points[i][j])):
                        a = [[0,0,0], points[i][j][k], points[i][j][0], points[i][0][k]]
                        a2 = [[0,0,0], points[i][0][k], points[i][j][0], points[i][0][0]]
                        tubes[i][j].append(a)
                        tubes[i][j].append(a2)
                    

    return tubes

                
    

def genCyl3(points_, width, height, radius, n, file):
    '''Generate the 3D model with cross sections from points_ with width height and radius of corners (divided into n triangles) and save it to file'''
    cyls = []
    cylsCaps = []
    for i in range(len(points_)):
        cyls.append([])
        cylsCaps.append([])
        for j in range(len(points_[i])):

            x = points_[i][j][0]
            y = points_[i][j][1]
            z = points_[i][j][2]

            cyl = genRoundedRectanglePointsRotateSkel(x,y,z, width, height, radius, n, points_[i][j][3],points_[i][j][4],points_[i][j][5])

            cyls[i].append(cyl)
            ##Generate the caps to the cylinders (if you want each cylinder as a seperate file)
            cylsCaps[i].append([])
            cylsCaps[i][j].append(genRoundedRectanglePointsRotate(x, y, z, width, height, radius, n, points_[i][j][3],points_[i][j][4],points_[i][j][5]))
            if (j != len(points_[i])-1):
                cylsCaps[i][j].append(genRoundedRectanglePointsRotate(points_[i][j+1][0], points_[i][j+1][1], points_[i][j+1][2], width, height, radius, n, points_[i][j+1][3],points_[i][j+1][4],points_[i][j+1][5]))
            else:
                cylsCaps[i][j].append(genRoundedRectanglePointsRotate(points_[i][0][0], points_[i][0][1], points_[i][0][2], width, height, radius, n, points_[i][0][3],points_[i][0][4],points_[i][0][5]))
                

    test = genTubes(cyls)

##    for i in range(len(test[0])):
##        writeSTL("bob3", file+str(i)+".stl", test[0][i])

    ##Uncomment to generate seperate stl files for each cylinder
##    for j in range(len(test)):
##        for i in range(len(test[j])):
##            print(file)
##            writeSTL("bob3", file+str(i)+".stl", test[j][i]+cylsCaps[j][i][0]+cylsCaps[j][i][1])
##            
            
    writeSTL3("bob3", file+".stl", test)
    
        

if __name__ == "__main__":

    test = genRoundedRectanglePointsRotate(5, 5, 0, 10, 10, 3, 10, math.pi/4, 0, math.pi/2)

    writeSTL("test1", "test1.stl", test)

    genCirclePoints(3, 1)
