import pandas as pd
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
import missingno as msno
import matplotlib.pyplot as plt

# Load data
directory_path = '/home/wiz-tech-kid/Downloads/financial-inclusion-in-africa-for-botswana20231019-32227-2ppact/'
train_data = pd.read_csv(directory_path + 'Train.csv')
test_data = pd.read_csv(directory_path + 'Test.csv')
variable_definitions = pd.read_csv(directory_path + 'VariableDefinitions.csv')
submission_format = pd.read_csv(directory_path + 'SampleSubmission.csv')

# Explore missing data
msno.matrix(train_data)
plt.show()

# Preprocess data
le = LabelEncoder()
scaler = MinMaxScaler()

train_data['bank_account'] = le.fit_transform(train_data['bank_account'])
X = train_data.drop(['bank_account'], axis=1)
y = train_data['bank_account']

categorical_columns = ['relationship_with_head', 'marital_status', 'education_level', 'job_type', 'country']
X = pd.get_dummies(X, columns=categorical_columns, prefix_sep='_')

X['location_type'] = le.fit_transform(X['location_type'])
X['cellphone_access'] = le.fit_transform(X['cellphone_access'])
X['gender_of_respondent'] = le.fit_transform(X['gender_of_respondent'])

X = X.drop('uniqueid', axis=1)

X = scaler.fit_transform(X)

X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42)

# Train the model
xg_model = XGBClassifier()
xg_model.fit(X_train, y_train)

y_pred = xg_model.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)
print("Model accuracy:", accuracy)

# Process test data and make predictions
processed_test = test_data.copy()
test_predictions = xg_model.predict(processed_test)

# Create submission file
submission = pd.DataFrame({
    "uniqueid": test_data["uniqueid"] + " x " + test_data["country"],
    "bank_account": test_predictions
})

submission.to_csv('financial_inclusion_submission.csv', index=False)
print("Submission file saved.")
