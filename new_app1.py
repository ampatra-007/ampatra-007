import streamlit as st #web app 
import pandas as pd # data manipulation
#import numpy as np # random gen
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.metrics import confusion_matrix
from matplotlib.pyplot import figure


st.set_page_config(page_title="Simulating Loan Thresholds", layout="wide")
#st.title("Simulating Loan Thresholds")

st.subheader("using Python")

values_male, values_female = st.columns(2)

vm=values_male.slider(
     'Select a range of values for class: male',
     min_value =20.0, max_value = 100.0, step=1.0, value=56.0)
#st.write('Cut off Values:', values)

vf=values_female.slider(
     'Select a range of values for class: female',
     min_value =20.0, max_value = 100.0, step=1.0, value=64.0)

st.markdown("### Key Metrics")

kpi1, kpi2 = st.columns(2)


# Read Excel file (Financial_Data.xlsx) into a pandas DataFrame.
df = pd.read_excel(
    io= 'D:/amit/customer loan details.xlsx',
    engine= "openpyxl",
    sheet_name= "Overlapping categories", #Orders
    #skiprows= 2,
    usecols= "A:G", #B:T
    nrows= 21 #3312,
)

df_male=df[df.Gender=='M']
df_female=df[df.Gender=='F']

#gndr=df.Gender.unique().to_list()
#st.write('Select Gender:', gndr)

#final_val = df.shape[0]

kpi1.metric(label = "Cut off for Male",
            value = vm)

kpi2.metric(label = "Cut off for Female",
            value = vf)

# gndr = st.radio(
#      "Class",
#      ('Male', 'Female', 'Overall'))

# if(gndr == 'Male'):
#     st.write('M')
# elif(gndr== 'Female'):
#     st.write('F')
# else:
#     st.write("Overall")
# kpi3.metric(label = "Select Class",value = gndr)

st.markdown("### Confusion Matrix 📈")

chart1, chart2 = st.columns(2)


def f1(row):
    if row['Loan_Eligibility_Probability'] <= vm:
        val = 'Yes'
    else:
        val = 'No'
    return val

def f2(row):
    if row['Loan_Eligibility_Probability'] <= vf:
        val = 'Yes'
    else:
        val = 'No'
    return val

df_male.predicted_default_male = df_male.apply(f1, axis=1)
df_female.predicted_default_male = df_female.apply(f2, axis=1)
# df.predicted_default1.value_counts()

chart_data_male=pd.DataFrame(confusion_matrix(df_male.Loan_Eligibility_Actual, df_male.predicted_default_male))
chart_data_female=pd.DataFrame(confusion_matrix(df_female.Loan_Eligibility_Actual, df_female.predicted_default_male))

fig, ax = plt.subplots()
sns.heatmap(chart_data_male, annot=True, fmt="d", annot_kws={"size": 18}, ax=ax,cmap="Blues")
ax.set_title('For Male', fontsize = 20)
plt.xlabel('Loan_Eligibility_Predicted', fontsize = 15) 
plt.ylabel('Loan_Eligibility_Actual', fontsize = 15)
ax.invert_yaxis()
figure(figsize=(8, 6), dpi=80)
chart1.pyplot(fig)

fig1, ax1 = plt.subplots()
sns.heatmap(chart_data_female,annot=True, fmt="d", annot_kws={"size": 18}, ax=ax1,cmap="Blues")
ax1.set_title('For Female', fontsize = 20)
plt.xlabel('Loan_Eligibility_Predicted', fontsize = 15) 
plt.ylabel('Loan_Eligibility_Actual', fontsize = 15)
ax1.invert_yaxis()
plt.figure(figsize=(1, 1))
chart2.pyplot(fig1)

#st.dataframe(df_male)
#st.dataframe(df_female)

#open anaconda Navigator and run streamlit run new_app1.py