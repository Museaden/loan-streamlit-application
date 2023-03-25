import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import streamlit as st  # pip install streamlit

# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Loan Dashboard", page_icon=":bar_chart:", layout="wide")

# ---- READ EXCEL ----
@st.cache_data
def get_data_from_csv():
    df = pd.read_csv("train.csv")
    df = df.dropna()
    return df

df = get_data_from_csv()

# ---- SIDEBAR ----
st.sidebar.header("Please Filter Here:")
gender = st.sidebar.multiselect(
"Select the Gender:",
options=df["Gender"].unique(),
default=df["Gender"].unique()
)

married = st.sidebar.multiselect(
"Select the Married:",
options=df["Married"].unique(),
default=df["Married"].unique(),
)

education = st.sidebar.multiselect(
"Select the Education:",
options=df["Education"].unique(),
default=df["Education"].unique()
)

loan_status = st.sidebar.multiselect(
"Select the Loan Status:",
options=df["Loan_Status"].unique(),
default=df["Loan_Status"].unique()
)

df_selection = df.query(
"Gender == @gender & Married ==@married & Education == @education & Loan_Status == @loan_status"
)
st.dataframe(df_selection)
# ---- MAINPAGE ----
st.title(":bar_chart: Loan Dashboard")
st.markdown("##")

# TOP KPI's
total_ApplicantIncome = int(df_selection["ApplicantIncome"].sum())
average_LoanAmount = round(df_selection["LoanAmount"].mean(), 1)
#star_rating = ":star:" * int(round(average_rating, 0))
average_CoapplicantIncome = round(df_selection["CoapplicantIncome"].mean(), 2)

left_column, middle_column, right_column = st.columns(3)
with left_column:
    st.subheader("Applicant Income:")
    st.subheader(f"US $ {total_ApplicantIncome:,}")
with middle_column:
    st.subheader("Average Loan Amount:")
    st.subheader(f"{average_LoanAmount }")
with right_column:
    st.subheader("Average Co applicant Income:")
    st.subheader(f"US $ {average_CoapplicantIncome}")

st.markdown("""---""")

# Applicant Income BY Education [PIE CHART]

fig_product_sales = px.pie(
    df_selection,
    values='ApplicantIncome',
    names='Education',
    #orientation="h",
    title="<b>Applicant Income by Education</b>",
    #color_discrete_sequence=["#0083B8"],
    #template="plotly_white",
)
# Applicant Income BY Property Area [BAR CHART]
fig_hourly_sales =  px.bar(
df_selection ,
x="Property_Area",
y="ApplicantIncome",
color = "Loan_Status",
title="<b>Applicant Income by Property Area</b>",
# color_discrete_sequence=["#ffff00"],
template="plotly_white",
)
fig_hourly_sales.update_layout(
xaxis=dict(tickmode="linear"),
plot_bgcolor="rgba(0,0,0,0)",
yaxis=(dict(showgrid=False)),
)


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_hourly_sales, use_container_width=True)
right_column.plotly_chart(fig_product_sales, use_container_width=True)


# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)