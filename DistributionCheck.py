import csv

# Function to load the given csv file
def getCitiesDetailFromCsv():
    data = []
    
    with open('cities.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)
    
    return data[1:]

# Function that gets multiple include and exclude data from the user
def getMultipleIncludeAndExcludeData():
    multiIncludeExcludeDetails = []
    repeatFlag = True
    while repeatFlag:
        originalDistIncludeDetails = input("\tEnter include area\n").split("-")
        originalDistExcludeDetails = input("\tEnter exclude area\n").split("-")
        multiIncludeExcludeDetails.append([originalDistIncludeDetails, originalDistExcludeDetails])

        repeat = input("\tDo you want to add more data?(Y/N)?\n")
        if(repeat.upper() == 'Y'):
            repeatFlag = True
        else:
            repeatFlag = False

    return multiIncludeExcludeDetails

# Function that filters the whole data with the city/state/countrty provided and returns the filtered list
def getFilteredList(listData, filterKey):
    filteredData = []
    
    for item in listData:
        if item.count(filterKey) > 0:
            filteredData.append(item)
    
    return filteredData

# Function that filters the whole data with the value(City-State-Country) provided and returns the exact location's list
def filteredAreaDetails(fullAreaDetails, includeArea):
    result = fullAreaDetails

    for i in range(0,len(includeArea)):
        if includeArea[i] != '':
            result = getFilteredList(result, includeArea[i])
    
    return result

# Function that returns the locations available based on the input(include/exclude) provided
def grantedLocations(fullAreaDetails, includeArea, excludeArea):
    grantedLocationData = []
    
    includeAreaDetails = filteredAreaDetails(fullAreaDetails, includeArea)
    excludeAreaDetails = filteredAreaDetails(fullAreaDetails, excludeArea)

    for item in includeAreaDetails:
        if item not in excludeAreaDetails:
            grantedLocationData.append(item)
    
    return grantedLocationData 

# Function that returns the locations available based on the multiple input(include/exclude) provided
def multipleDataGrantedLocation(distGrantedLocationList, distributorDetails):
    grantedLocationsList = distGrantedLocationList
    for distDetails in distributorDetails:
            includeData = distDetails[0]
            excludeData = distDetails[1]
            grantedLocationsList = grantedLocations(grantedLocationsList,includeData, excludeData)
    
    return grantedLocationsList

# Function that validates the current distributor data based on his upper distributors data
# (current distributor is always subset of upper distributors)
def validatingOrigDistData(upperDistributorsCount, upperDistGrantedLocationList, originalDistGrantedLocationList):
    validationOfDistInput = True
    if upperDistributorsCount > 0:
        flag = True
        for origData in originalDistGrantedLocationList:
            if origData not in upperDistGrantedLocationList:
                flag = False
                print("flag", flag)
            if flag == False:
                validationOfDistInput = False
                break
    
    return validationOfDistInput  


upperDistributorsCount = int(input("Enter the number of upper distributors\n"))
upperDistributorsDetails = []
distributorsDetails = []

# loading the csv file
fullAreaDetails = getCitiesDetailFromCsv()
upperDistGrantedLocationList = fullAreaDetails

print("Please enter the include and exclude details in the format (City-State-Country)\n")
print("----------------------------------------Input Examples------------------------------------------\n")
print("\t\t\t(empty data<enter key>)-> Will take the previous available data\n")
print("\t\t\t\t--\n")
print("\t\t\t\tIndia\n")
print("\t\t\t\tTamil Nadu-India\n")
print("\t\t\t\tTamil Nadu\n")
print("\t\t\t\tChennai-Tamil Nadu-India\n")
print("\t\t\t\tChennai\n")
print("-----------------------------------------------------------------------------------------------\n")
print("-------------------------Provide the exact data as of csv file provided------------------------\n")
print("---------------------------------Beware of the typo mistake------------------------------------\n")
print("-----------------------------------------------------------------------------------------------\n")
if upperDistributorsCount > 0:
    for i in range(0,upperDistributorsCount):
        print("\nEnter details for upper distributor {}\n".format(i+1))
        multipleIncludeAndExcludeData = getMultipleIncludeAndExcludeData()
        upperDistributorsDetails.append(multipleIncludeAndExcludeData)
    for upperDistributors in upperDistributorsDetails:
        upperDistGrantedLocationList = multipleDataGrantedLocation(upperDistGrantedLocationList, upperDistributors)

print("\nEnter details for the current distributor")
multipleIncludeExcludeData = getMultipleIncludeAndExcludeData()
originalDistGrantedLocationList = multipleDataGrantedLocation(fullAreaDetails, multipleIncludeExcludeData)

while(True):
    distributionAreaInput = input('Please enter the area to check, if the distribution is possible?\n').split('-')

    distributionArea = filteredAreaDetails(originalDistGrantedLocationList, distributionAreaInput)
    print("Total Area Available is", len(distributionArea))

    if len(distributionArea)>0:
        print('\nYes!')
    else:
        print('\nNo!')
    print("\nPress Ctrl+C to exit\n")