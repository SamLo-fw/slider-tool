import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

PHI = 1.61803398874989484820458683
PHIS = PHI + 1
FRAME_COUNTER = 56
SCALE_X = 50.0
SCALE_Y = 50.0
FILENAME = "map.osu"
BASE_OFFSET = 3*60000 + 1472
REAL_BPM = 165.0
MS_PER_BEAT = 60000.0 / REAL_BPM
X_OFFSET = 256
Y_OFFSET = 192

class Point:
    def __init__(self, x,y,z):
        self.x = x
        self.y = y
        self.z = z

    def position(self) -> tuple:
        return np.array([self.x,self.y,self.z])

    @staticmethod
    def distance(p1, p2) -> float:
        x = p2.x - p1.x
        y = p2.y - p1.y
        z = p2.z - p1.z
        return (math.sqrt(x**2 + y**2 + z**2))

    @staticmethod
    def rotX(angle, matrix):
        rotation_matrix = np.array([
            [1,     0,                  0               ],
            [0,     math.cos(angle),    -math.sin(angle)],
            [0,     math.sin(angle),    math.cos(angle) ]
        ])
        return matrix @ rotation_matrix.T

    @staticmethod
    def rotY(angle, matrix):
        rotation_matrix = np.array([
            [math.cos(angle),   0,      math.sin(angle) ],
            [0,                 1,      0               ],
            [-math.sin(angle),  0,      math.cos(angle) ]
        ])
        return matrix @ rotation_matrix.T

    @staticmethod
    def rotZ(angle, matrix):
        rotation_matrix = np.array([
            [math.cos(angle),   -math.sin(angle),   0],
            [math.sin(angle),   math.cos(angle),    0],
            [0,                 0,                  1]
        ])
        return matrix @ rotation_matrix.T


class Dodecahedron:
    
    a = Point(0, PHIS, 1)
    b = Point(PHI, PHI, PHI)
    c = Point(1, 0, PHIS)
    d = Point(-1, 0, PHIS)
    e = Point(-PHI, PHI, PHI)
    f = Point(-PHI, PHI, -PHI)
    g = Point(0, PHIS, -1)
    h = Point(PHI, PHI, -PHI)
    i = Point(PHIS, 1, 0)
    j = Point(PHIS, -1, 0)
    k = Point(PHI, -PHI, PHI)
    l = Point(0, -PHIS, 1)
    m = Point(-PHI, -PHI, PHI)
    n = Point(-PHIS, -1, 0)
    o = Point(-PHIS, 1, 0)
    p = Point(-1, 0, -PHIS)
    q = Point(1, 0, -PHIS)
    r = Point(PHI, -PHI, -PHI)
    s = Point(0, -PHIS, -1)
    t = Point(-PHI, -PHI, -PHI)

    def __init__(self):
        self.path = [self.t, self.p, self.f, self.o, self.n, self.t, self.s, self.l, self.m, self.n, self.o, self.e, self.d, self.m, self.d, self.c, self.k, self.l, self.k, self.j, self.i, self.b, self.i, self.h, self.g, self.a, self.b, self.a, self.e, self.a, self.g, self.f, self.p, self.q, self.h, self.q, self.r, self.j, self.r, self.s]
        self.path_positions = np.array([v.position() for v in self.path])


if __name__ == "__main__":

    frame = None
    #.. okay now what lmao
    # i guess we take those points and define a rotate operation as a matrix
    # then for each frame we project that set of points onto a 2d plane 
    # & scale to fit the screen pixel dimensions for the osu playfield

    # then convert each frame into a slider, which I will figure out... later

    dd = Dodecahedron()

    frame_data = []

    for i in range(FRAME_COUNTER):
        i_as_rad = i * math.pi / 180
        th_x = math.pi * math.sin(i)
        th_y = math.pi * math.cos(i)
        th_z = max(0, -math.pi * math.cos(i))

        rotated = Point.rotX(th_x, Point.rotY(th_y, Point.rotZ(th_z, dd.path_positions)))

        xy = rotated[:, 0:2]

        z = 1/(rotated[:, 2]/4 + 1)

        flattened_xy = xy * z[:, np.newaxis]
    
        #scale the points to the playfield
        scaled_xy = flattened_xy * np.array([SCALE_X, SCALE_Y])
        rounded_xy = np.round(scaled_xy).astype(int)

        frame_data.append(rounded_xy)

    frame_distances = []
    for i in range(len(frame_data)):
        prev_frame = np.array(frame_data[i-1])
        curr_frame = np.array(frame_data[i])

        delta = curr_frame - prev_frame
        distances = np.linalg.norm(delta, axis=1)
        total_disance = np.sum(distances)
        frame_distances.append(total_disance)

    with open(FILENAME, 'r', encoding="utf-8") as f:
        content = f.readlines()

    sections = {}
    current_section = None

    for line in content:
        line = line.strip()

        if line.startswith('[') and line.endswith(']'):
            current_section = line[1:-1]
            sections[current_section] = []
        elif current_section and line and not line.startswith('//'):
            sections[current_section].append(line)
    
    slider_multiplier = float(sections["Difficulty"][4].split(":")[1])
    
    frame_strings = []
    for idx, frame in enumerate(frame_data, start=1):
        frame_offset = round(BASE_OFFSET + idx * MS_PER_BEAT/4)
        frame_x = frame[0][0]
        frame_y = frame[0][1]
        frame_string = []
        points_str = "|".join(f"{point[0]+X_OFFSET}:{point[1]+Y_OFFSET}" for point in frame[1:])
        frame_string = f"{frame_x+X_OFFSET},{frame_y+Y_OFFSET},{frame_offset},2,0,L|{points_str},1,{round(frame_distances[idx-1]/slider_multiplier)}"
        frame_strings.append(frame_string)

    timing_strings = []
    
    import matplotlib.pyplot as plt

    frame = dd.path_positions
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')

    ax.plot(frame[:, 0], frame[:, 1], frame[:, 2])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_box_aspect([1,1,1])  # Equal aspect ratio
    plt.show()
    #convert the points into a slider

    #for sv: sv caps at x10 at -10, [2000,-10,4,1,0,100,0,0] -> [timestamp (2s), sv (x10), X, X, X, type - 0 = sv, 1 = timing, X]
    #for timing point: [0,250,4,1,0,100,1,0] -> timestamp, ms/beat ... type = 1
    #SliderMultiplier: base slider vel in hectopixels/beat 

    #x,y,time,type,hitSound,objectParams,hitSample
    #slider: [120,122,2000,2,0,L|434:284,1,350] -> x,y,time,type,hitSound as bitflags,curveType|curvePoints,slides,length,edgeSounds,edgeSets,hitSample
    # L|434:284,1,350 -> type linear, end 434:284, repeat 1 time, length 350 px
    #  (B = bézier, C = centripetal catmull-rom, L = linear, P = perfect circle)

    # okay so: find total length of the slider given all the points I hit
    # then scale the bpm and sv to match that
    # then create an object string at OFFSET + object_counter*1/4beat_offset at set x,y, 
    # and then generate the 
    # slider points, which should look vaguely like 
    # B|246:224|246:224|319:193|319:193|418:52|418:52|618:346, where each item in
    # the pipe seperated list is x:y of a point in the dodecahedron
    # https://osu.ppy.sh/wiki/en/Client/File_formats/osu_%28file_format%29

    
    