import pandas as pd
from sklearn.preprocessing import MinMaxScaler
from imblearn.over_sampling import SMOTE
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score, classification_report

# Function to normalize the dataset using MinMaxScaler - this is optional 
def NormaliseData(df):
    numericalFeatures = ['popularity', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness']
    scaler = MinMaxScaler()
    df[numericalFeatures] = scaler.fit_transform(df[numericalFeatures])
    df.to_csv('songs_normalized.csv', index=False)
    return df.head()

# Function to filter Recommended Library so it does not include any of the songs in User Favs
def FilterRecommendedLibrary():
    userFavsIds = set()
    with open('userfavs.csv', 'r', encoding='utf-8') as userFavs:
        header = next(userFavs)  # Skip the header row
        for line in userFavs:
            trackId = line.split(',')[0].rstrip()
            userFavsIds.add(trackId)
    
    filteredLibrary = []
    isFirstLine = True  # Flag to check if we're on the first line
    with open('recommendations_library.csv', 'r', encoding='utf-8') as recommendedLibrary:
        for line in recommendedLibrary:
            if isFirstLine:
                filteredLibrary.append(line)  # Add the header to the filtered list
                isFirstLine = False
                continue
            trackId = line.split(',')[0].rstrip()
            if trackId not in userFavsIds:
                filteredLibrary.append(line)
    
    with open('recommendations_library.csv', 'w', encoding='utf-8') as recommendedLibrary:
        for line in filteredLibrary:
            recommendedLibrary.write(line)


def AddFavoriteField():
    # Add favorite field to user favorites CSV
    with open('userfavs.csv', 'r', encoding='utf-8') as infile, open('userfavs_updated.csv', 'w', encoding='utf-8') as outfile:
        header = next(infile)  # Read the first line as header
        outfile.write(header.strip() + ',favorite\n')  # Add 'favorite' to header
        for line in infile:
            outfile.write(line.strip() + ',1\n')  # Append ',1' for favorite
    
    # Add favorite field to recommendations library CSV
    with open('recommendations_library.csv', 'r', encoding='utf-8') as infile, open('library_updated.csv', 'w', encoding='utf-8') as outfile:
        header = next(infile)  # Read the first line as header
        outfile.write(header.strip() + ',favorite\n')  # Add 'favorite' to header
        for line in infile:
            outfile.write(line.strip() + ',0\n')  # Append ',0' for not favorite


# Function to prepare datasets for training
def PrepareDatasets(userfavsPath, libraryPath, combinedCsvPath='combined_data.csv'):
    userfavsDf = pd.read_csv(userfavsPath)
    libraryDf = pd.read_csv(libraryPath)
    combinedDf = pd.concat([userfavsDf, libraryDf], ignore_index=True)
    combinedDf.to_csv(combinedCsvPath, index=False)
    
    numericFields = ['length', 'popularity', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'timeSignature', 'favorite']
    combinedNumericDf = combinedDf[numericFields]
    trainDf, testDf = train_test_split(combinedNumericDf, test_size=0.2, random_state=42)
    
    X_train = trainDf.drop('favorite', axis=1)
    y_train = trainDf['favorite']
    smote = SMOTE(random_state=42)
    X_trainResampled, y_trainResampled = smote.fit_resample(X_train, y_train)
    
    resampledTrainDf = pd.DataFrame(X_trainResampled, columns=X_train.columns)
    resampledTrainDf['favorite'] = y_trainResampled
    testDf.to_csv('test_data.csv', index=False)
    resampledTrainDf.to_csv('training_data.csv')
    DeleteFirstFieldAndSave('training_data.csv')
    RemoveFav('test_data.csv')

    return resampledTrainDf

# Function to delete the first field from CSV and save
def DeleteFirstFieldAndSave(csvPath, newCsvPath=None):
    df = pd.read_csv(csvPath)
    df.drop(columns=df.columns[0], inplace=True)
    df.to_csv(newCsvPath if newCsvPath else csvPath, index=False)

#Function to remove favorite column
def RemoveFav(csvPath):
    df = pd.read_csv(csvPath)

    # Check if 'favorite' column exists and remove it
    if 'favorite' in df.columns:
        df.drop(columns=['favorite'], inplace=True)

    df.to_csv(csvPath,index=False)

# Function to train a decision tree classifier
def TrainDecisionTreeClassifier(csvPath):
    df = pd.read_csv(csvPath)
    X = df.drop(columns=['favorite'])
    y = df['favorite']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    clf = DecisionTreeClassifier(random_state=42)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print("\nClassification Report:\n", classification_report(y_test, y_pred))
    
    return clf

# Function to combine CSVs
def CombineCsvs(csvPath1, csvPath2, outputCsvPath):
    df1 = pd.read_csv(csvPath1)
    df2 = pd.read_csv(csvPath2)
    combinedDf = pd.concat([df1, df2], ignore_index=True)
    combinedDf.to_csv(outputCsvPath, index=False)

# Function to recommend based on the trained model
def Recommend(testDataDf, clfModel):
    probabilities = clfModel.predict_proba(testDataDf)[:, 1]
    testDataDf['predictedFavoriteProbability'] = probabilities
    sortedTestDataDf = testDataDf.sort_values(by='predictedFavoriteProbability', ascending=False)
    top10Recommendations = sortedTestDataDf.head(10)
    sortedTestDataDf.head(10).to_csv('recs.csv')
    DeleteFirstFieldAndSave('recs.csv', 'recs.csv')
    return top10Recommendations

# Function to find a match in the recommendations
def FindMatch(recsCsvPath, combinedRawCsvPath):
    recsDf = pd.read_csv(recsCsvPath)
    combinedRawDf = pd.read_csv(combinedRawCsvPath)
    featuresToCompare = ['length', 'popularity', 'danceability']
    matchingTrackIds = []
    
    for index, recRow in recsDf.iterrows():
        mask = (combinedRawDf[featuresToCompare] == recRow[featuresToCompare]).all(axis=1)
        matchingRows = combinedRawDf[mask]
        if not matchingRows.empty:
            matchingTrackIds.extend(matchingRows['trackId'].tolist())
    
    return matchingTrackIds
