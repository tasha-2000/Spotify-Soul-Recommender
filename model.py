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

# Function to filter Reccomended Library so it does not include any of the song in User Favs
def FilterRecommendedLibrary():
    userFavsIds = set()
    with open('userfavs.csv', 'r', encoding='utf-8') as userFavs:
        for line in userFavs:
            trackId = line.split(',')[0].rstrip()
            userFavsIds.add(trackId)
    
    filteredLibrary = []
    with open('recommendations_library.csv', 'r', encoding='utf-8') as recommendedLibrary:
        for line in recommendedLibrary:
            trackId = line.split(',')[0].rstrip()
            if trackId not in userFavsIds:
                filteredLibrary.append(line)
    
    with open('recommended_library.csv', 'w', encoding='utf-8') as recommendedLibrary:
        for line in filteredLibrary:
            recommendedLibrary.write(line)

# Function to add headers to CSV files
def AddHeadersToCsv(filePaths):
    header = "track_id,name,album,artist,release_date,length,popularity,danceability,acousticness,energy,instrumentalness,liveness,loudness,speechiness,tempo,time_signature,favorite\n"
    
    for filePath in filePaths:
        with open(filePath, 'r', encoding='utf-8') as file:
            content = file.read()
        with open(filePath, 'w', encoding='utf-8') as file:
            file.write(header + content)

# Function to add favorite field to CSV
def AddFavoriteField():
    with open('userfavs.csv', 'r', encoding='utf-8') as infile, open('userfavs_updated.csv', 'w', encoding='utf-8') as outfile:
        for line in infile:
            outfile.write(line.rstrip() + ',1\n')
    
    with open('final_lib.csv', 'r', encoding='utf-8') as infile, open('library_updated.csv', 'w', encoding='utf-8') as outfile:
        for line in infile:
            outfile.write(line.rstrip() + ',0\n')

# Function to prepare datasets for training
def PrepareDatasets(userfavsPath, libraryPath, combinedCsvPath='combined_data.csv'):
    userfavsDf = pd.read_csv(userfavsPath)
    libraryDf = pd.read_csv(libraryPath)
    combinedDf = pd.concat([userfavsDf, libraryDf], ignore_index=True)
    combinedDf.to_csv(combinedCsvPath, index=False)
    
    numericFields = ['length', 'popularity', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature', 'favorite']
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
    
    return resampledTrainDf

# Function to delete the first field from CSV and save
def DeleteFirstFieldAndSave(csvPath, newCsvPath=None):
    df = pd.read_csv(csvPath)
    df.drop(columns=df.columns[0], inplace=True)
    df.to_csv(newCsvPath if newCsvPath else csvPath, index=False)


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
    featuresToCompare = ['length', 'popularity', 'danceability', 'acousticness', 'energy', 'instrumentalness', 'liveness', 'loudness', 'speechiness', 'tempo', 'time_signature']
    matchingTrackIds = []
    
    for index, recRow in recsDf.iterrows():
        mask = (combinedRawDf[featuresToCompare] == recRow[featuresToCompare]).all(axis=1)
        matchingRows = combinedRawDf[mask]
        if not matchingRows.empty:
            matchingTrackIds.extend(matchingRows['track_id'].tolist())
    
    return matchingTrackIds

def Main():
    # Step 1: remove songs in the reccomended library that are also in the user favs dataset
    FilterRecommendedLibrary()

    #Step2: Add favorite field to both files
    AddFavoriteField()

    # Step 3: prepare the datasets by balancing the two datasets using SMOTE and dropping nonnumerical fields
    PrepareDatasets('userfavs_updated.csv', 'library_updated.csv')

    #Step 4: train DT Model
    clfModel = TrainDecisionTreeClassifier('training_data.csv')

    #Step 5: use DT model to get recommendations
    testDataDf = pd.read_csv('test_data.csv')
    X_test = testDataDf.drop(columns=['favorite'])
    recommendations = Recommend(X_test, clfModel)
    print(recommendations)

    #Step 6: Find the Track IDs associated with the reccomendedations
    trackIDs = FindMatch('recs.csv', 'combined_data.csv')
    print(trackIDs)

if __name__ == "__main__":
    Main()