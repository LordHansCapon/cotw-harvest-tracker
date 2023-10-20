from constants import *


def getDifficultyName(score):
    scoreIndex = -1

    for threshold in DIFFICULTY_SCORE_THRESHOLDS:
        if score >= threshold:
            scoreIndex = scoreIndex + 1
        else:
            break

    return DIFFICULTIES[scoreIndex]

