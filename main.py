import math
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import rotation_gen as rg

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
        
        # to khang: i got these points by just drawing a schlegel and then manually tracing a valid path through them lmao
        # it's 2 vertices longer than an optimal path but that honestly doesn't matter for such a low number of points
        # https://imgur.com/FsOBkUS
        self.path = [self.t, self.p, self.f, self.o, self.n, self.t, self.s, self.l, self.m, self.n, self.o, self.e, self.d, self.m, self.d, self.c, self.k, self.l, self.k, self.j, self.i, self.b, self.c, self.b, self.i, self.h, self.g, self.a, self.b, self.a, self.e, self.a, self.g, self.f, self.p, self.q, self.h, self.q, self.r, self.j, self.r, self.s]
        self.path_positions = np.array([v.position() for v in self.path])


if __name__ == "__main__":

    frame = None
    dd = Dodecahedron()
    frame_rotations = rg.get_frame_rotations()
    frame_data = []

    # start movement at 03:03:471, 18103471
    # project dodecahedron to playfield
    for i in range(FRAME_COUNTER):
        t = i / FRAME_COUNTER
        th_x = (frame_rotations[i]["thX"] + 47) * math.pi/180
        th_y = (frame_rotations[i]["thY"] + 39) * math.pi/180
        th_z = (frame_rotations[i]["thZ"] + 120)* math.pi/180

        rotated = Point.rotX(th_x, Point.rotY(th_y, Point.rotZ(th_z, dd.path_positions)))
        rotated = rotated[:, :2] # remove z to project
    
        #scale the points to the playfield
        scaled_xy = rotated * np.array([frame_rotations[i]["size"] * 50, frame_rotations[i]["size"] * 50])
        rounded_xy = np.round(scaled_xy).astype(int)

        frame_data.append(rounded_xy)

    # the rest of the code fits the slider so that it lasts for 1/8th of a beat
    frame_distances = []
    for frame in frame_data:
        frame = np.array(frame)
        deltas = np.diff(frame, axis=0)
        distances = np.linalg.norm(deltas, axis=1)
        frame_distances.append(np.sum(distances))

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
        frame_offset = round(BASE_OFFSET + (idx-1) * MS_PER_BEAT/4)
        frame_x = frame[0][0]
        frame_y = frame[0][1]
        frame_string = []
        points_str = "|".join(f"{point[0]+X_OFFSET}:{point[1]+Y_OFFSET}|{point[0]+X_OFFSET}:{point[1]+Y_OFFSET}" for point in frame[1:])
        frame_string = f"{frame_x+X_OFFSET},{frame_y+Y_OFFSET},{frame_offset},2,0,L|{points_str},1,{round(frame_distances[idx-1])}"
        frame_strings.append(frame_string)

        with open("output_objects.txt", 'w') as f:
            f.write("\n".join(frame_strings))

    def find_BPM(distance):
        sv_factor = slider_multiplier * 1000
        total_time = MS_PER_BEAT/8.0
        ms_per_beat_divided = (sv_factor * total_time) / distance.item()
        return ms_per_beat_divided

    #and then I just dump it to a file and manually copy/paste into the level
    #i thought it'd be faster than generating a .osu every time, but in retrospect that was incorrect
    timing_strings = []
    STARTING_VOLUME = 30
    VOLUME_RANGE = 40
    for idx, frame in enumerate(frame_data, start=1):
        timing_offset = round(BASE_OFFSET + (idx-1) * MS_PER_BEAT/4) - 1
        BPM = find_BPM(frame_distances[idx-1])
        timing_string = f"{timing_offset},{BPM},4,2,0,{round(STARTING_VOLUME+VOLUME_RANGE*(idx/len(frame_data)))},1,0"
        timing_strings.append(timing_string)
        
        timing_string_2 = f"{timing_offset+1},{-10},4,2,0,{round(STARTING_VOLUME+VOLUME_RANGE*(idx/len(frame_data)))},0,0"
        timing_strings.append(timing_string_2)
        
        with open("output_timing.txt", 'w') as f:
            f.write("\n".join(timing_strings))
        #181471,-10,4,2,0,30,0,0
        #offset, multiplier (as percentage of -100), meter, sampleset iter (default, normal, soft, drum), sampleset index, volume, ?inhereted, effects (int) bitflags for additional effects such as kiai time
    

    print("Done")

    #notes to self
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

    
    