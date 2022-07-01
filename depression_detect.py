import numpy as np
import csv
from pomegranate import *
import cv2
import ctypes  # An included library with Python install.   

def createModel():
    depression = DiscreteDistribution({'true': 0.2, 'false': 0.8})
    angry = ConditionalProbabilityTable(
        [
            ['true', 'true', 0.8],
            ['true', 'false', 0.2],
            ['false', 'true', 0.2],
            ['false', 'false', 0.8]
        ], [depression])
    disgust = ConditionalProbabilityTable(
        [
            ['true', 'true', 0.8],
            ['true', 'false', 0.2],
            ['false', 'true', 0.2],
            ['false', 'false', 0.8]
        ], [depression])
    scared = ConditionalProbabilityTable(
        [
            ['true', 'true', 0.7],
            ['true', 'false', 0.3],
            ['false', 'true', 0.2],
            ['false', 'false', 0.8]
        ], [depression])
    happy = ConditionalProbabilityTable(
        [
            ['true', 'true', 0.9],
            ['true', 'false', 0.1],
            ['false', 'true', 0.8],
            ['false', 'false', 0.2]
        ], [depression])
    sad = ConditionalProbabilityTable(
        [
            ['true', 'true', 0.8],
            ['true', 'false', 0.2],
            ['false', 'true', 0.2],
            ['false', 'false', 0.8]
        ], [depression])
    surprised = ConditionalProbabilityTable(
        [
            ['true', 'true', 0.3],
            ['true', 'false', 0.7],
            ['false', 'true', 0.8],
            ['false', 'false', 0.2]
        ], [depression])
    neutral = ConditionalProbabilityTable(
        [
            ['true', 'true', 0.1],
            ['true', 'false', 0.9],
            ['false', 'true', 0.7],
            ['false', 'false', 0.3]
        ], [depression])

    depressionNode = Node(depression, name="depression")
    angryNode = Node(angry, name="angry")
    disgustNode = Node(disgust, name="disgust")
    scaredNode = Node(scared, name="scared")
    happyNode = Node(happy, name="happy")
    sadNode = Node(sad, name="sad")
    surprisedNode = Node(sad, name="surprised")
    neutralNode = Node(sad, name="neutral")

    model = BayesianNetwork("Depression Model")
    model.add_states(depressionNode, angryNode, disgustNode,
                     scaredNode, happyNode, sadNode, surprisedNode, neutralNode)
    model.add_edge(depressionNode, angryNode)
    model.add_edge(depressionNode, disgustNode)
    model.add_edge(depressionNode, scaredNode)
    model.add_edge(depressionNode, happyNode)
    model.add_edge(depressionNode, sadNode)
    model.add_edge(depressionNode, surprisedNode)
    model.add_edge(depressionNode, neutralNode)
    model.bake()

    return model

def createAnxietyModel():
    anxiety = DiscreteDistribution({'true': 0.2, 'false': 0.8})
    angry = ConditionalProbabilityTable(
        [
            ['true', 'true', 0.6],
            ['true', 'false', 0.4],
            ['false', 'true', 0.2],
            ['false', 'false', 0.8]
        ], [anxiety])
    disgust = ConditionalProbabilityTable(
        [
            ['true', 'true', 0.8],
            ['true', 'false', 0.2],
            ['false', 'true', 0.2],
            ['false', 'false', 0.8]
        ], [anxiety])
    scared = ConditionalProbabilityTable(
        [
            ['true', 'true', 0.7],
            ['true', 'false', 0.3],
            ['false', 'true', 0.2],
            ['false', 'false', 0.8]
        ], [anxiety])
    happy = ConditionalProbabilityTable(
        [
            ['true', 'true', 0.3],
            ['true', 'false', 0.7],
            ['false', 'true', 0.2],
            ['false', 'false', 0.7]
        ], [anxiety])
    sad = ConditionalProbabilityTable(
        [
            ['true', 'true', 0.4],
            ['true', 'false', 0.6],
            ['false', 'true', 0.2],
            ['false', 'false', 0.8]
        ], [anxiety])
    surprised = ConditionalProbabilityTable(
        [
            ['true', 'true', 0.7],
            ['true', 'false', 0.3],
            ['false', 'true', 0.4],
            ['false', 'false', 0.6]
        ], [anxiety])
    neutral = ConditionalProbabilityTable(
        [
            ['true', 'true', 0.1],
            ['true', 'false', 0.9],
            ['false', 'true', 0.7],
            ['false', 'false', 0.3]
        ], [anxiety])

    anxietyNode = Node(anxiety, name="anxiety")
    angryNode = Node(angry, name="angry")
    disgustNode = Node(disgust, name="disgust")
    scaredNode = Node(scared, name="scared")
    happyNode = Node(happy, name="happy")
    sadNode = Node(sad, name="sad")
    surprisedNode = Node(sad, name="surprised")
    neutralNode = Node(sad, name="neutral")

    model = BayesianNetwork("Depression Model")
    model.add_states(anxietyNode, angryNode, disgustNode,
                     scaredNode, happyNode, sadNode, surprisedNode, neutralNode)
    model.add_edge(anxietyNode, angryNode)
    model.add_edge(anxietyNode, disgustNode)
    model.add_edge(anxietyNode, scaredNode)
    model.add_edge(anxietyNode, happyNode)
    model.add_edge(anxietyNode, sadNode)
    model.add_edge(anxietyNode, surprisedNode)
    model.add_edge(anxietyNode, neutralNode)
    model.bake()

    return model

def runModel(fileName):

    ANGRY_THRESHOLDS = 0.10
    DISGUST_THRESHOLDS = 0.05
    SCARED_THRESHOLDS = 0.10
    HAPPY_THRESHOLDS = 0.40
    SAD_THRESHOLDS = 0.10
    SURPRISED_THRESHOLDS = 0.05
    NEUTRAL_THRESHOLDS = 0.60

    isAngry = None
    isDisgust = None
    isScared = None
    isHappy = None
    isSad = None
    isSurprised = None
    isNeutral = None
    readdata = csv.reader(open(fileName, 'r'))
    data = []

    for row in readdata:
        data.append(row)

    # incase you have a header/title in the first row of your csv file, do the next line else skip it
    data.pop(0)

    angry = []
    disgust = []
    scared = []
    happy = []
    sad = []
    surprised = []
    neutral = []

    for i in range(len(data)):
        angry.append(float(data[i][0]))
        disgust.append(float(data[i][1]))
        scared.append(float(data[i][2]))
        happy.append(float(data[i][3]))
        sad.append(float(data[i][4]))
        surprised.append(float(data[i][5]))
        neutral.append(float(data[i][6]))

    if np.mean(angry) > ANGRY_THRESHOLDS:
        isAngry = 'true'

    if np.mean(disgust) > DISGUST_THRESHOLDS:
        isDisgust = 'true'

    if np.mean(scared) > SCARED_THRESHOLDS:
        isScared = 'true'

    if np.mean(happy) > HAPPY_THRESHOLDS:
        isHappy = 'true'

    if np.mean(sad) > SAD_THRESHOLDS:
        isSad = 'true'

    if np.mean(surprised) > SURPRISED_THRESHOLDS:
        isSurprised = 'true'

    if np.mean(neutral) > NEUTRAL_THRESHOLDS:
        isNeutral = 'true'

    print('Mean of angry :            ', (np.mean(angry) * 100))
    print('Mean of disgust :            ', (np.mean(disgust) * 100))
    print('Mean of scared :            ', (np.mean(scared) * 100))
    print('Mean of happy :            ', (np.mean(happy) * 100))
    print('Mean of sad :            ', (np.mean(sad) * 100))
    print('Mean of surprised :            ', (np.mean(surprised) * 100))
    print('Mean of neutral :            ', (np.mean(neutral) * 100))

    anxietyModel = createAnxietyModel()
    depressionModel = createModel()
    observations = {'angry': isAngry, 'disgust': isDisgust, 'scared': isScared,
                    'happy': isHappy, 'sad': isSad, 'surprised': isSurprised, 'neutral': isNeutral}
    resultsDepression = depressionModel.predict_proba(observations)
    resultsAnxiety = anxietyModel.predict_proba(observations)

    print("Person isAngry:", isAngry)
    print("Person isDisgust:", isDisgust)
    print("Person isScared:", isScared)
    print("Person isHappy:", isHappy)
    print("Person isSad:", isSad)
    print("Person isSurprised:", isSurprised)
    print("Person isNeutral:", isNeutral)

    depression_level = round(resultsDepression[0].parameters[0]['true'] * 100)
    anxiety_level = round(resultsAnxiety[0].parameters[0]['true'] * 100)
    print("Depression Level:: {} %".format(depression_level))
    print("Anxiety Level:: {} %".format(anxiety_level))
    resultText = "Depression Level:: {} % Anxiety Level:: {} %\n ".format(depression_level,anxiety_level)

    ctypes.windll.user32.MessageBoxW(0, resultText, "Depression/Anxiety", 1)