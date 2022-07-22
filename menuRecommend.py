# TODO
# categoryNumberCurrent 이용은 아직 -> OK
# 불러온 식품 중 셔플해서 랜덤 추가 -> OK
# 범위 안에 들어오는 지 확인해주는 f
# reload했을 때 아무것도 없으면?! / categoryNumberRemain 다 0일때?!
# 범위안에 들어오지 않으면 반복작업 -> OK


import loadFoods
import random
from copy import deepcopy


def is_emptyAll(foodList):
    is_emptyAll = False
    emptyNum = 0
    for category in foodList:
        if not category:
            emptyNum += 1
    if len(foodList) == emptyNum:
        is_emptyAll = True
        print("-----식품 카테고리 모두 비어있음-----")
    return is_emptyAll


def is_satisfiedAll(remain):
    # 범위 안에 안들어와서 임시로 높임
    # if (
    #     (0 <= remain.get("priceRemain"))
    #     and (-50 <= remain.get("calRemain") <= 50)
    #     and (-20 <= remain.get("carbRemain") <= 20)
    #     and (-10 <= remain.get("protRemain") <= 10)
    #     and (-10 <= remain.get("fatRemain") <= 10)
    # ):
    # 원하는 범위
    if (
        (0 <= remain.get("priceRemain"))
        and (-50 <= remain.get("calRemain") <= 50)
        and (-10 <= remain.get("carbRemain") <= 10)
        and (-5 <= remain.get("protRemain") <= 5)
        and (-3 <= remain.get("fatRemain") <= 3)
    ):
        return True
    else:
        return False


def infoUpdate(currentInfo, remain, food):
    """currentInfo, remain 업데이트"""
    # 1: 카테고리 / 2: 식품명 / 3: 가격 / 4: 칼 / 5: 탄 / 6: 단 / 7: 지
    currentInfo["priceCurrent"] += food[3]
    currentInfo["calCurrent"] += food[4]
    currentInfo["carbCurrent"] += food[5]
    currentInfo["protCurrent"] += food[6]
    currentInfo["fatCurrent"] += food[7]
    currentInfo["recommendedNumber"] += 1

    remain["priceRemain"] -= food[3]
    remain["calRemain"] -= food[4]
    remain["carbRemain"] -= food[5]
    remain["protRemain"] -= food[6]
    remain["fatRemain"] -= food[7]

    # 카테고리idx: CG002 -> 1로
    print("추가된 식품 카테고리idx:", int(food[0][-3:]) - 1)
    categoryidx = int(food[0][-3:]) - 1
    remain["categoryNumberRemain"][categoryidx] -= 1
    print("남은 카테고리 추천 수(infoUpdate): ", remain["categoryNumberRemain"])

    return currentInfo, remain


def foodAppend(currentInfo, foodList, preferCategory, remain):
    """
    return : currentInfo, remain \n
    (식품 추가하고 현재까지 추가된+남은 영양, 가격 등 업데이트)
    """
    foodListShuffle = foodList
    preferCategoryForShuffle = preferCategory
    random.shuffle(preferCategoryForShuffle)
    # 카테고리순서는 그대로고 하위에 row들만 순서가 바뀌어야함
    for i in range(len(foodListShuffle)):
        random.shuffle(foodListShuffle[i])
    # print(foodListShuffle)

    isAppended = False
    for category in preferCategory:
        for food in foodListShuffle[category]:
            currentInfo["recommendedList"].append(food)
            isAppended = True
            break
        if isAppended:
            currentInfo, remain = infoUpdate(currentInfo, remain, food)
            print("식품추가!!!")
            break

    return currentInfo, remain


def recommendInitialize(baseInfo):
    """return: currentInfo, remain"""

    # 이상하게 deepCopy 안하면 recommendedList가 base["recommendedList"] 에 영향을줌....
    recommendedListBase = deepcopy(baseInfo["recommendedListBase"])

    currentInfo = {
        "priceCurrent": baseInfo.get("priceBase"),
        "calCurrent": baseInfo.get("calBase"),
        "carbCurrent": baseInfo.get("carbBase"),
        "protCurrent": baseInfo.get("protBase"),
        "fatCurrent": baseInfo.get("fatBase"),
        "recommendedNumber": 0,
        "recommendedList": recommendedListBase,
        "is_satisfiedAll": False,
        "notSatisfied": [0, 0, 0, 0, 0],
    }
    remain = {
        "priceRemain": baseInfo.get("priceTarget") - currentInfo.get("priceCurrent"),
        "calRemain": baseInfo.get("calTarget") - currentInfo.get("calCurrent"),
        "carbRemain": baseInfo.get("carbTarget") - currentInfo.get("carbCurrent"),
        "protRemain": baseInfo.get("protTarget") - currentInfo.get("protCurrent"),
        "fatRemain": baseInfo.get("fatTarget") - currentInfo.get("fatCurrent"),
        "categoryNumberRemain": [1, 2, 1, 2, 2, 1],
    }
    for i, num in enumerate(baseInfo.get("categoryNumberBase")):
        if i not in baseInfo.get("preferCategory"):
            remain["categoryNumberRemain"][i] = 0
        remain["categoryNumberRemain"][i] -= baseInfo.get("categoryNumberBase")[i]
    print("남은 카테고리 추천 수(recommendInitialize): ", remain.get("categoryNumberRemain"))

    return currentInfo, remain


# 처음 가져오는 고객 정보 #######################
baseInfo = {
    "priceBase": 0,
    "calBase": 0,
    "carbBase": 0,
    "protBase": 0,
    "fatBase": 0,
    "priceTarget": 8000,
    "calTarget": 832,
    "carbTarget": 92,
    "protTarget": 42,
    "fatTarget": 21,
    "preferCategory": [0, 1, 5],
    "categoryNumberBase": [0, 0, 0, 0, 0, 0],
    "recommendedListBase": [],
    "initializeReason": [0,0,0,0,0],            # 가격 / 칼 / 탄 / 단 / 지
}

# 식품 추가되면서 업데이트 되는 정보
print("----------------")
currentInfo, remain = recommendInitialize(baseInfo)

# 식품가져오기
foodList = loadFoods.loadFoods(remain, currentInfo)
foodListInitialized = foodList
print("----------------")

preferCategory = baseInfo.get("preferCategory")


# ##########################test########################
# print("식품추가전 baseInfo:", baseInfo)
# print("식품추가전 currentInfo:", currentInfo)
# currentInfo, remain = foodAppend(currentInfo, foodList, preferCategory, remain)
# print("식품추가후 baseInfo:", baseInfo)
# print("식품추가후 currentInfo:", currentInfo)
# #######################################################


############ 식품추가 ############
while not currentInfo.get("is_satisfiedAll"):
    foodList = loadFoods.reloadFoods(foodList, remain, currentInfo)

    # categoryNumRemain 없으면 reloadFoods때 걸러짐 -> 비어있는지만 확인하면 됨
    if is_emptyAll(foodList):        
        for i, j in enumerate(currentInfo.get("notSatisfied")):
            baseInfo["initializeReason"][i] += j
        currentInfo, remain = recommendInitialize(baseInfo)
        print("initializeReason:", baseInfo.get("initializeReason"))
        foodList = foodListInitialized

    currentInfo, remain = foodAppend(currentInfo, foodList, preferCategory, remain)
    # Nutr 만족하는지 확인하고 is_satisfied 변경
    if is_satisfiedAll(remain):
        currentInfo["is_satisfiedAll"] = True
        print("is_satisfiedAll: ", currentInfo["is_satisfiedAll"])
        break

    print(currentInfo["recommendedList"])
    print("notSatisfied:", currentInfo.get("notSatisfied"))    

print("--------------식단구성완료---------------")
print("식단:")

for idx, food in enumerate(currentInfo["recommendedList"]):
    print(idx, food)
print("-----------------------------------------")
print("currentInfo: ", currentInfo)
print("-----------------------------------------")
# for key, value in currentInfo.items():
#     print(f"{key} : {value}")
