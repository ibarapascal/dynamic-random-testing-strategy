import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
import random

def generate_case(caseLength, generateParams):
    
    output = []
    method = generateParams['method']
    
    if method == 1:
        # Single random test
        output.append(np.arange(0, caseLength, 1).tolist()) # [)
    
    if method == 2:
        # Simple sort test
        setNum = generateParams['setNum']
        minLength = generateParams['minLength']
        r = []
        for unused in range(setNum - 1):
            while True:
                split = int(random.random() * caseLength) # [) but with int(), so []
                f = 0
                for j in range(len(r)):
                    if abs(split - r[j]) <= minLength or split == 0 or split == caseLength or split == caseLength - 1: #20180402
                        f = 1
                        continue
                if f:
                    continue #20180402
                r.append(split)
                break
        r.sort() #20180402
        s = np.arange(0, caseLength, 1).tolist() # [)
        for i in range(setNum):
            if i == 0:
                output.append(s[: r[i]])
            elif i == setNum - 1:
                output.append(s[r[i - 1] : ])
            else:
                output.append(s[r[i - 1] : r[i]])
     
    if method == 3:
        # DRT with certain set length
        setLength = generateParams['setLength']
        s = np.arange(0, caseLength, 1).tolist() # [)
        while True:
            r = []
            for unused in range(setLength):
                while True:
                    case = random.randint(0, caseLength - 1)
                    f = 0
                    for j in range(len(r)):
                        if r[j] == case:
                            f = 1
                            continue
                    if f:
                        continue
                    r.append(case)
                    try:
                        s.remove(case)
                    except:
                        pass
                    break
            f = 0
            for i in range(len(output)):
                if output[i] == r:
                    f = 1
                    continue
            if f:
                continue
            output.append(r)
            if not s:
                break
            
    if method == 4:
        # DRT with certain set number
        setNum = generateParams['setNum']
        output.append([])
        pass

    return output


def inject_defect(caseLength, defectLength, injectParams):
    
    output = []
    method = injectParams['method']
    
    if method == 1:
        # Average way of defect inject
        for unused in range(defectLength):
            while True:
                a = random.randint(0, caseLength - 1)
                f = 0
                for i in range(len(output)):
                    if output[i] == a:
                        f = 1
                        continue
                if f:
                    continue
                output.append(a) # []
                break
        output.sort()
    
    if method == 2:
        # Average way of defect inject with area district.
        for unused in range(defectLength):
            while True:
                a = random.randint(int(caseLength * 2 / 5), int(caseLength * 3 / 5) - 1)
                f = 0
                for i in range(len(output)):
                    if output[i] == a:
                        f = 1
                        continue
                if f:
                    continue
                output.append(a) # []
                break
        output.sort()
        
    if method == 3:
        # Normal distribution
        # The larger distribution rate, the longer defect distribution length.
        distributionRate = 0.25 # <=====
        # The center of distribution in range of (0, 1)
        distributePlace = 0.5 # <=====
        r = []
        total = 0
        if defectLength % 2 == 0:
            x = np.arange(0, defectLength / 2, 1)
            y = stats.norm.pdf(x, 0, 1 / distributionRate)
            for i in range(int(defectLength / 2)):
                if i == 0:
                    r.append(y[i] / 2)
                else:
                    r.append(y[i])
                total += r[i]            
        if defectLength % 2 == 1:
            x = np.arange(0, (defectLength - 1) / 2, 1) 
            y = stats.norm.pdf(x, 0, 1 / distributionRate)
            for i in range(int((defectLength - 1)/ 2)):
                r.append(y[i])
                total += r[i]            
#         plt.plot(x, y)
#         plt.show()
        rate = caseLength / 2 / total #20180402
        for i in range(len(r)):
            r[i] = int(r[i] * rate) 
        base = int(caseLength * distributePlace)
        for i in range(len(r)):
            output.append(base - r[len(r) - 1 - i])
        for i in range(len(r)):
            output.append(base + r[i])
        output.sort() #20180402
        if output[0] < 0 or output[-1] > (caseLength - 1):
            print('The distribution rate is too large. Please adjust the distribution rate.')
            input('Pause here.')
        xx = []
        for i in range(len(output)):
            xx.append(i)
#         plt.plot(xx, output)
#         plt.show()
        xx.pop()
        yy = []
        for i in range(len(output) - 1):
            yy.append(output[i] - output[i + 1])
#         plt.plot(xx, yy)
#         plt.show()
        
    if method == 3:
        output.append([])
    
    return output


def adjust_rate(rateSet, rateBase, caseSetChooseIndex, detectedFlag, adjustParams):
    
    output = []
    method = adjustParams['method']
    
    if method == 1:
        output = rateSet
        
    if method == 2:
        adjustRateL = rateBase * adjustParams['rateL']
        adjustRateS = rateBase * adjustParams['rateS']
        rateSetLength = len(rateSet)
        if detectedFlag: # Detected.
            for i in range(rateSetLength):
                if i == caseSetChooseIndex:
                    rateSet[i] *= 1 + adjustRateL
                else:
                    rateSet[i] *= (1 - adjustRateL / (rateSetLength - 1))
        else: # Not detected.
            for i in range(rateSetLength):
                if i == caseSetChooseIndex:
                    rateSet[i] *= 1 - adjustRateS
                else:
                    rateSet[i] *= (1 + adjustRateS / (rateSetLength - 1))
        output = rateSet
    
    return output


def main(params):
    
    # STRAT simulation!
    simulationLength = params['simulationLength']
    totalDCNum = 0
    totalDDList = []
    
    for unused in range(simulationLength):
        
        # Initialize case set.
        caseLength = params['caseLength']
        caseList = []
        for unused in range(caseLength):
            caseList.append(random.randint(1, 10)) # [], the value here is prepared for future usage. Notice that it's Int.
        
        # Initialize defect set index.   
        defectLength = params['defectLength']
        defectIndex = inject_defect(caseLength, defectLength, params['injectParams'])
        
        # Inject defect.
        for i in range(len(defectIndex)):
            caseList[defectIndex[i]] += 0.01 # Inject the defect by transform Int to Float.
        
        # Initialize case set index.
        caseSetIndex = generate_case(caseLength, params['generateParams'])
        caseSetLength = len(caseSetIndex)
           
        # Initialize rate set.
        rateBase = 1 / caseSetLength
        rateSet = [rateBase] * caseSetLength
        
        # Start this time simulation.
        defectDetectNum, defectCheckNum, defectTryNum = 0, 0, 0
        defectDetectList = []
        detectedFlag = False
        startUpFlag = True
        
        while True:
            # Make case set.
            # Notice that if no repeat with caseList, we need to make case set every time the simulation run.
            caseSet = []    
            for i in range(caseSetLength):
                case = []
                for j in range(len(caseSetIndex[i])):
                    case.append([caseSetIndex[i][j], caseList[caseSetIndex[i][j]]]) # Basic case structure. [caseIndex, caseValue], where case value prepared for future usage.
                caseSet.append(case)            
                 
            # Choose case set.
            # Adjust the rateSet to 0 if all of the item becomes to None.
            for i in range(caseSetLength):
                allNone = True
                for j in range(len(caseSetIndex[i])):
                    if not caseSet[i][j][1] == None: # 20180516
                        allNone = False
                        break
                if allNone:
                    rateSet[i] = 0
            # Quit if all of the rateSet becomes to Zero.
            rateChoose = []
            allZero = True
            for i in range(len(rateSet)):
                if rateSet[i]:
                    allZero = False
                rateChoose.append(rateSet[i] * random.random())
            if allZero:
                break # Quit this time simulation.  
            # Continue to choose.
            caseSetChooseIndex = 0          
            for i in range(len(rateChoose)):
                if rateChoose[i] == max(rateChoose):
                    caseSetChooseIndex = i
            caseSetChoose = caseSet[caseSetChooseIndex]
            # Choose case.
            caseChooseIndex = 0
            while True:
                caseChooseIndex = random.randint(0, len(caseSetChoose) - 1) # []
                if caseSetChoose[caseChooseIndex][1] == None:
#                     print('piripara')
                    continue
                else:
                    break
            caseChoose = caseSetChoose[caseChooseIndex]
            
            # Judge, adjust rate in rate set. Notice that after this, we need to rebuild case set.
            defectTryNum += 1
            if isinstance(caseChoose[1], float): # According to basic case structure defined in make case set.
#                 caseList[caseChoose[0]] = int(caseList[caseChoose[0]]) # Remark the defect to normal one (Float to Int).
                caseList[caseChoose[0]] = None
                defectCheckNum += 1
                defectDetectNum += 1
                defectDetectList.append(defectCheckNum)
                detectedFlag = True
            elif isinstance(caseChoose[1], int): # Not detected.
                caseList[caseChoose[0]] = None
                defectCheckNum += 1
                detectedFlag = False
            else: # Have been checked.
                print('opsssss')
                break
            
            # Adjust rate of case set choose.
            rateSet = adjust_rate(rateSet, rateBase, caseSetChooseIndex, detectedFlag, params['adjustParams'])
#             print(str(defectCheckNum) + ' / ' + str(defectLength) + ' / ' + str(defectDetectNum))  
            # Break when all defect have been detected.
            if defectDetectNum == defectLength:
                break
            if defectTryNum >= caseLength * 2:
                break
#             print(str(defectTryNum))
#             print(defectDetectList)
#             print(str(defectDetectNum))
            
        # Record the single step simulation result.    
        totalDCNum += defectCheckNum
        totalDDList.append(defectDetectList)
        print('RE: '+ str(defectDetectList))
        
    # Output the total record result.
    averageDCNum = totalDCNum / simulationLength
    averageDDList = []
    averageDDListSTD = []
    maxList =[]
    for i in range(simulationLength):
        maxList.append(len(totalDDList[i]))
    for i in range(max(maxList)):
        totalItemValue, k = 0, 0
        tempList = []
        for j in range(simulationLength):
            try:
                totalItemValue += totalDDList[j][i]
                tempList.append(totalDDList[j][i])
                k += 1
            except:
                pass
        totalItemValue /= k 
        averageDDList.append(totalItemValue)
        averageDDListSTD.append(np.std(tempList, ddof = 1))
    print('\nRE: ' +str(averageDDList))
    print('\nRE: ' +str(averageDDListSTD))
    
    # Plot the average result.
    axisX = np.arange(0, max(maxList), 1)
    axisY1 = averageDDList
    axisY2, axisY3, axisY4 = [], [], []
    for i in range(len(axisY1)):
        axisY2.append(axisY1[i] - averageDDListSTD[i])
        axisY3.append(axisY1[i] + averageDDListSTD[i])
        axisY4.append(averageDDListSTD[i])
#     plt.plot(axisX, axisY1)
#     plt.plot(axisX, axisY2)
#     plt.plot(axisX, axisY3)
    plt.plot(axisX, axisY4)
#     plt.yscale('log')
#     plt.show()
    
    # Write the output to excel file.
    import time
    import time as myTime
    import xlrd
    import xlwt
    from xlutils.copy import copy
    ts = int(myTime.time())
    file_path = 'C:\\Users\\Pascal JING\\Desktop\\DRT_Simulation_' + str(ts) +'.xls'
#     file_path = 'C:\\Users\\Administrator\\Desktop\\DRT_Simulation_' + str(ts) +'.xls'
    file = xlwt.Workbook()
    sheetname = 'result'
    sheet = file.add_sheet(sheetname, cell_overwrite_ok = True)
#     sheet.write(0, 0, 'start')
    for i in range(len(totalDDList)):
        for j in range(len(totalDDList[i])):
            sheet.write(i, j, totalDDList[i][j])
    for j in range(len(averageDDList)):
        sheet.write(i + 2, j, averageDDList[j])
#     file.save(file_path)
    return

params = {
    'simulationLength': 100, # The number of simulation times using the same params below.
    'caseLength': 1000, # The number of case.
    'defectLength': 100, # The number of defect in case.
    'injectParams': {
        'method': 2,
        },
#     'generateParams': {
#         'method': 3,
#         'setLength': 200,
#         },
    'generateParams': {
        'method': 2,
        'setNum': 10,
        'minLength': 10,
        },
    'adjustParams': {
        'method': 2,
        'rateL': 0.2,
        'rateS': 0.2,
        }, 
#     'adjustParams': {
#         'method': 1,
#         }, 
    }
    
'''
main
'''
# main(params)
'''
main
'''
# x = [0, 0.1, 0.2, 0.4, 0.8]
# for i in range(len(x)):
#     if x[i] == 0:
#         params['adjustParams']['method'] = 1
#     else:
#         params['adjustParams']['method'] = 2
#         params['adjustParams']['rateL'] = x[i]
#         params['adjustParams']['rateS'] = x[i]
#     main(params)

x = [1, 2, 4, 8, 16, 32, 64]
for i in range(len(x)):
    if x[i] == 1:
        params['generateParams']['method'] = 1
    else:
        params['generateParams']['method'] = 2
        params['generateParams']['setNum'] = x[i]
        params['generateParams']['minLength'] = 1
    main(params)
    
# plt.xlim((0,20))
# plt.ylim((0,1000))
plt.xticks(np.linspace(0,99,10))
# plt.yticks([0, 1000],['起始', '结束'])
plt.xlabel('Defect Number')
plt.ylabel('Detect Length')
plt.legend(labels = x)
plt.show()
