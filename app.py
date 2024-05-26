import streamlit as st
import pandas as pd
import pickle
from googletrans import Translator

st.set_page_config(
    page_title="ঔষধ প্রস্তাবনা সিস্টেম",
    page_icon="💊"
)

# Define background image CSS


page_bg_img = """
<style>
[data-testid="stAppViewContainer"]{
background-image: url("https://i.ibb.co/xmMKV5w/output-onlinepngtools-1.png");
background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Load the similarity pickle file
with open('similarity.pkl', 'rb') as file:
    similarity = pickle.load(file)

# Load your dataset
new_df = pd.read_csv('medicine.csv', encoding='utf-8')  # Ensure this CSV has a 'Description' column

# Function to translate text to Bangla
def translate_to_bangla(text):
    translator = Translator()
    translated = translator.translate(text, dest='bn')
    return translated.text

# Define your recommendation function
def recommend(medicine):
    medicine_index = new_df[new_df['Drug_Name'] == medicine].index[0]
    distances = similarity[medicine_index]
    medicines_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_medicines = []
    for i in medicines_list:
        recommended_medicines.append(new_df.iloc[i[0]].Drug_Name)

    return recommended_medicines

# Streamlit UI
st.title('ঔষধ প্রস্তাবনা সিস্টেম')

# Sidebar for selecting medicine
selected_medicine = st.selectbox('একটি ঔষধ নির্বাচন করুন', new_df['Drug_Name'])

# Button to trigger recommendation
if st.button('প্রস্তাবনা করুন'):
    recommended_medicines = recommend(selected_medicine)

    # Create a DataFrame to hold medicine names and descriptions
    recommended_df = pd.DataFrame(columns=['ঔষধের নাম', 'বর্ণনা'])

    # Populate the DataFrame
    for med in recommended_medicines:
        bengali_name = translate_to_bangla(med)  # Translate to Bangla using the function

        # Get the description for the medicine
        description = new_df[new_df['Drug_Name'] == med]['Description'].values[0]
        bengali_description = translate_to_bangla(description)

        recommended_df = recommended_df.append({'ঔষধের নাম': bengali_name, 'বর্ণনা': bengali_description},
                                               ignore_index=True)

    # Display the DataFrame as a table
    st.write('**শীর্ষ 5 প্রস্তাবিত ঔষধ:**')
    st.table(recommended_df)
