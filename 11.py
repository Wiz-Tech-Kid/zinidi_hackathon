
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import LabelEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn.metrics import confusion_matrix, accuracy_score

# Define the directory path
directory_path = '/home/wiz-tech-kid/Downloads/financial-inclusion-in-africa-for-botswana20231019-32227-2ppact/'

# Load the data
train_data = pd.read_csv(directory_path + 'Train.csv')
test_data = pd.read_csv(directory_path + 'Test.csv')

# Preprocess the data
le = LabelEncoder()
scaler = MinMaxScaler()

train_data['bank_account'] = le.fit_transform(train_data['bank_account'])

X = train_data.drop(['bank_account'], axis=1)
y = train_data['bank_account']

categorical_columns = ['relationship_with_head', 'marital_status', 'education_level', 'job_type', 'country']
for col in categorical_columns:
    X[col] = le.fit_transform(X[col])

X = pd.get_dummies(X, columns=categorical_columns, prefix_sep='_')

X = X.drop(['uniqueid'], axis=1)

X = X.astype(float)  # Convert to float for scaling

X = scaler.fit_transform(X)

# Split the data into training and validation sets
X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.1, random_state=42)

# Train an XGBoost model
xg_model = XGBClassifier()
xg_model.fit(X_train, y_train)

# Evaluate the model on the validation set
y_pred = xg_model.predict(X_val)
accuracy = accuracy_score(y_val, y_pred)

# Display the accuracy in tabular format
print("Model accuracy:")
print(accuracy)

# Make predictions on the test data
processed_test = test_data.copy()

for col in categorical_columns:
    processed_test[col] = le.fit_transform(processed_test[col])

processed_test = pd.get_dummies(processed_test, columns=categorical_columns, prefix_sep='_')

processed_test = processed_test.drop(['uniqueid'], axis=1)

processed_test = processed_test.astype(float)  # Convert to float for scaling

processed_test = scaler.transform(processed_test)

test_predictions = xg_model.predict(processed_test)

# Create a submission file
submission = pd.DataFrame({
    "uniqueid": test_data["uniqueid"] + " x " + test_data["country"],
    "bank_account": test_predictions
})

# Save the submission file
submission.to_csv('financial_inclusion_submission.csv', index=False)

# Display the predicted target variable for the test data in graphical format
plt.figure()
plt.hist(test_predictions)
plt.xlabel("Predicted target variable")
plt.ylabel("Frequency")
plt.title("Distribution of predicted target variable for test data")
plt.show()
