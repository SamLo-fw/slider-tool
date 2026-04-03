import json, math

def s_curve(p, inflection=0.5, steepness=6):

    # p ranges from [0,1]
    # paramaterized logistic curve, endpoints clamp to [0,1]
    k = steepness
    x0 = inflection
    raw = 1 / (1 + math.exp(-k * (p - x0)))
    lo = 1 / (1 + math.exp(-k * (0 - x0)))
    hi = 1 / (1 + math.exp(-k * (1 - x0)))
    return (raw - lo) / (hi - lo)

def split_ease(p, exp_in=3.0, exp_out=3.0, split=0.5):
    A = (exp_out * split) / (exp_in * (1.0 - split) + exp_out * split)
    # piecewise ease-in-out, A is a scaling constant to ensure the curve is differentiable

    if p < split:
        t = p / split
        return A * (t ** exp_in)
    else:
        q = (p - split) / (1.0 - split)
        return A + (1.0 - A) * (1.0 - (1.0 - q) ** exp_out)

def get_frame_rotations():
    frames = [
    181471,181563,181654,181745,181836,181927,182017,182108,182199,182290,182381,
    182472,182563,182654,182745,182836,182927,183017,183108,183199,183290,
    183381,183472,183563,183654,183745,183836,183927,184017,184108,184199,
    184290,184381,184472,184563,184654,184745,184836,184927,185017,185108,
    185199,185290,185381,185472,185563,185654,185745,185836,185927,186017,
    186108,186199,186290,186381,186472,186563
    ]

    SEG1_START = 181471
    SEG1_END   = 183472
    SEG2_END   = 186563
    SEG1_5_END = 184745 #seg 1.5 lol that's the scuff

        
    result = []
    for t in frames:
        if t <= SEG1_END:
            duration = SEG1_END - SEG1_START
            p = (t - SEG1_START) / duration  # 0..1
            ease = 3*p**2 - 2*p**3
            thX = round(33.0 * ease, 4)
            thY = round(50.0 * ease, 4)
            thZ = 0.0
            size = round(1.0 + 0.5 * ease, 4)
        else:
            # this was supposed to be 2 sections but I got lazy so now the code is rlly scuffed
            duration = SEG2_END - SEG1_END
            duration_scuff = SEG1_5_END - SEG1_END
            p = (t - SEG1_END) / duration  # 0..1
            p_scuff = (t - SEG1_END) / duration_scuff #lol
            split_frame  = frames[-(16)]
            split_p      = (split_frame - SEG1_END) / (SEG2_END - SEG1_END)

            easeOutX = split_ease(p, exp_in=3.0, exp_out=4.0, split=split_p)
            easeOutY = split_ease(p, exp_in=3.0, exp_out=4.0, split=split_p)
            easeScuffY = p_scuff ** 2.0

            thX = round(33.0 - 24  * easeOutX, 4)
            thY = round(50.0 - 60 * easeOutY - easeScuffY * 10, 4)
            easeZ = 1 - (1 - p) ** 1.25
            thZ = round(0.0 - 0.85 * easeZ, 4)
            easeSize = split_ease(p, exp_in=4.0, exp_out=3.0, split=split_p)
            size = round(1.5 - 0.55 * easeSize, 4)

        result.append({
            "t": t,
            "thX": thX,
            "thY": thY,
            "thZ": thZ,
            "size": size
        })
    return result