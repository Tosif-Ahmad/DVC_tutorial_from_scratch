import pandas as pd
import os

# Create a sample DataFrame with column names
data = {'Compound': ['Benzene', 'Toulene', 'Naphtalene'],
    'Molecular weight': [78.11, 92.14, 128.17],
    'TPSA': [0.0, 0.0, 0.0]
    }

df = pd.DataFrame(data)

# # # Adding new row to df for V2
new_row_loc = {'Compound': 'Acetone', 'Molecular weight': 58.08, 'TPSA': 20.23}
df.loc[len(df.index)] = new_row_loc

# # # Adding new row to df for V3
# new_row_loc2 = {'Compound': 'GF2', 'Molecular weight': 30.0, 'TPSA': 15.4}
# df.loc[len(df.index)] = new_row_loc2

# Ensure the "data" directory exists at the root level
data_dir = 'data'
os.makedirs(data_dir, exist_ok=True)

# Define the file path
file_path = os.path.join(data_dir, 'sample_data.csv')

# Save the DataFrame to a CSV file, including column names
df.to_csv(file_path, index=False)

print(f"CSV file saved to {file_path}")