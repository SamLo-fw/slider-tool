import cv2
from PIL import Image
import numpy as np

images = {
    "hytale":"hytale.webp",
    "miku":"miku.png",
    "miku2":"mikuv2.webp",
    "shape":"Dodecahedron.png",
    "mikupng":"mikuv2.png"
}

LOW_EDGE_THRESHOLD = 50
HIGH_EDGE_THRESHOLD = 150
MERGE_THRESHOLD = 10
MERGE_TOLERANCE = 10

class MergeSections:
    def __init__(self):
        self.nodes_merge_intersections = []
        self.edges_non_merge_sections = []
class State:
    def __init__(self):
        self.img = None
        self.filename = None
        self.edges = None
        self.hierarchy = None
        self.contours_raw = None
        self.merge_sections = MergeSections()

def contour_convert(state):
    if state is None or state.img is None:
        raise FileNotFoundError(f"image not created")
    gray = cv2.cvtColor(state.img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, threshold1=LOW_EDGE_THRESHOLD, threshold2=HIGH_EDGE_THRESHOLD)
    contours, hierarchy = cv2.findContours(edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return edges, contours, hierarchy

def load_image(state):
    if state is None or state.filename not in images:
        raise KeyError(f"image {state.filename} not found in images")
    img = cv2.imread(images[state.filename], cv2.IMREAD_UNCHANGED)
    if img is None:
        raise FileNotFoundError(f"image not created")
    return img

def find_merges(contour1, contour2):
    if state is None or state.contours_raw is None:
        raise KeyError(f"state.countours not found in state object")
    
    merge_sections = MergeSections()
    
    counter_down = 0
    arr = merge_sections.edges_non_merge_sections
    for point_1 in contour1:
        for point_2 in contour2:
            del_vect = point_2 - point_1
            if np.linalg.norm(del_vect) < MERGE_THRESHOLD:
                counter_down = MERGE_TOLERANCE
                arr = merge_sections.nodes_merge_intersections
            else:
                counter_down = counter_down - 1
                if counter_down<=0:
                    arr = merge_sections.edges_non_merge_sections
            
            arr.append((point_1, point_2)) #let's just do this naively for now
            
    return merge_sections

def perform_merge(contour1, contour2, to_merge):
    return None

def merge(state):
    if state is None or state.contours_raw is None:
        raise KeyError(f"state.countours not found in state object")
    
    contours = [{'contour':c, 'checked':False} for c in state.contours_raw]
    merge_sections = None

    a_contour_was_changed = True
    while a_contour_was_changed:
        a_contour_was_changed = False

        for i in range(len(contours)):
            contour_base = contours[i]["contour"]
            if contours[i]["checked"]: continue

            for j in range(i+1, len(contours)):
                contour_comparison = contours[j]["contour"]
                merge_sections = find_merges(contour_base, contour_comparison)

                if merge_sections:
                    merged_contour = {'contour': perform_merge(contours[i], contours[j], merge_sections),'checked':False}
                    contours[i] = merged_contour
                    contours.pop(j)
                    a_contour_was_changed = True
                    break

            if not a_contour_was_changed:
                contours[i]["checked"] = True
        
        if not a_contour_was_changed and all(c['checked'] for c in contours):
            break

    return None

if __name__ == "__main__":
    state = State()
    state.filename = "shape"

    state.img = load_image(state)
    state.edges, state.contours_raw, state.hierarchy = contour_convert(state)
    state.merged_contour = merge(state)

    # temp rendering code
    # nah this ain't worth it the eps is too small anyways

    contour_image = np.zeros_like(state.img)

    cv2.drawContours(contour_image, state.contours_raw, contourIdx=-1, color=(255, 255, 255), thickness=1)
    cv2.namedWindow('Grayscale', cv2.WINDOW_NORMAL)
    cv2.imshow('Grayscale', contour_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()




# grayscale, cleanup, gaussian
    # edge detection
    # get a list of contours
    # set flag to false
    # ingnore the trivial i=j case (index x,x)
    # for every countour, pairwise check to return a list of MergeSections: {sections: [pairs of indices where misdist is under a threshold], nonmergec1:[nested list of indices for non-merged sections], indicesc2:[same for c2]} ]
        # define a MergeSection as: dist between points is under some threshold. once I go above that threshold, start counting down. once I hit zero, that's the end of the threshold. If I go back below the threshold, then it's still the same segment and I reset the counter
        #can use a many to many mapping, that's fine -- when I merge them together it'll be the easiest
    # merge by averaging each pair of points, and making each index from list of segments a "merge section"
        # then pick the first merge section, and add that to the merged contour. trace a set of points until I exit the merge section, then pick a non-traversed non-merge segment.
        # traverse until I reach another intersection.
        # repeat until I return to home node and there are no more non-traversed edges
        # provably works because each node has an even number of connected edges, and if you leave then you enter the next time or vice versa, so on non-starter nodes enter->leave->enter->leave (done) and for starter nodes have leave->...enter (done) . Also, you are forced to remove 2 non-traversed edges each time you visit a node, so therefore you are forced to end on starter when there are no more non-traversed edges
        # append the merged contour to a list, and to a "merged" list to avoid duplicating like (2,3) and (3,2)
    # set the countour list to that list, and flag = true
    # repeat while flag = true


# figure out how to convert a gif into a set of images
# parse some .osu file so that I can grab timing data so that I know what offset to place the object + the slider velocity
# build the slider strings based on the slider path I generate in the code

# try to figure out an algo to always make the slider ssable
# stack a simple GUI layer on top so that the tool isn't restricted to command line