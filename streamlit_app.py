import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title('Science Mill Summer Camp Dashboard')

# Raw GitHub link for your pre and post training data
url_pre = 'https://raw.githubusercontent.com/henryco94/scienceMillDash/main/june12_pre.csv'
url_post = 'https://raw.githubusercontent.com/henryco94/scienceMillDash/main/june12_post.csv'

# Load the pre and post survey data
df_pre = pd.read_csv(url_pre)
df_post = pd.read_csv(url_post)

# Drop the specified columns
columns_to_drop = ['#', 'Responder','Person', 'Teacher Number', 'Type', 'Approval Status', 'Date']
df_pre = df_pre.drop(columns=columns_to_drop, errors='ignore')
df_post = df_post.drop(columns=columns_to_drop, errors='ignore')

# Get list of all districts
districts = list(df_pre['District'].unique())
districts.insert(0, 'All')

# Mapping between pre and post survey questions
question_mapping = {
    'Before the training, I felt most comfortable teaching concepts within my subject/content area': 'After the training, I have experienced growth in my comfort level and now feel more confident teaching these previously challenging topics or concepts within my subject/content area',
    'Please rate your confidence in your ability to teach STEM concepts in your lesson plans and activities': 'Please rate your confidence in your ability to teach STEM concepts in your lesson plans and activities',
    'Please rate your confidence in your ability to incorporate career connections in your lesson plans and activities': 'Please rate your confidence in your ability to incorporate career connections in your lesson plans and activities',
    'I believe that I have the ability to shape the development of my students’ STEM identities': 'I believe that I have the ability to shape the development of my students’ STEM identities.',
    'I believe that I have the ability to shape my students’ self efficacies in STEM': 'I believe that I have the ability to shape my students’ self efficacies in STEM.',
}

# Dropdown to select a district
selected_district = st.selectbox('Select a district:', districts)

# Filter the data for the selected district
if selected_district != 'All':
    df_pre = df_pre[df_pre['District'] == selected_district]
    df_post = df_post[df_post['District'] == selected_district]

# Dropdown to select the survey type
survey_type = st.selectbox('Select a survey type:', ['Pre only', 'Post only', 'Mapped'])

# List of all questions in the pre and post survey data
mapped_questions = list(question_mapping.keys()) + list(question_mapping.values())
unmapped_questions_pre = [q for q in list(df_pre.columns) if q not in mapped_questions]
unmapped_questions_post = [q for q in list(df_post.columns) if q not in mapped_questions]

# Determine the list of questions to display based on the selected survey type
if survey_type == 'Pre only':
    questions = unmapped_questions_pre
elif survey_type == 'Post only':
    questions = unmapped_questions_post
elif survey_type == 'Mapped':
    questions = mapped_questions

# Dropdown to select a question
selected_question = st.selectbox('Select a question:', questions)

# Function to add percentage on the bars
def add_percentage(ax):
    for p in ax.patches:
        height = p.get_height()
        ax.text(p.get_x()+p.get_width()/2.,
                height + 0.01,
                '{:1.1f}%'.format(height*100),
                ha="center")

# If the selected question is a mapped question
if selected_question in question_mapping.keys() or selected_question in question_mapping.values():
    fig, ax = plt.subplots()
    # Identify the pre and post question pair
    pre_question = [k for k, v in question_mapping.items() if v == selected_question][0] if selected_question in question_mapping.values() else selected_question
    post_question = question_mapping[pre_question]

    # Count the responses for the pre and post survey questions
    pre_counts = df_pre[pre_question].value_counts(normalize=True)
    post_counts = df_post[post_question].value_counts(normalize=True)

    # Create a DataFrame with the response counts for both surveys
    counts = pd.DataFrame({'Pre': pre_counts, 'Post': post_counts})

    # Plot a grouped bar chart with percentages
    counts.plot(kind='bar', color=['blue', 'green'], figsize=(10, 6), ax=ax)
    plt.title(f'Pre vs Post: {pre_question}')
    plt.ylabel('Proportion of Responses')
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1))
    add_percentage(ax)
    plt.tight_layout()
    st.pyplot(fig)

# If the selected question is in the pre survey data, plot a bar chart with percentages
elif selected_question in df_pre.columns:
    fig, ax = plt.subplots()
    df_pre[selected_question].value_counts(normalize=True).plot(kind='bar', color='blue', figsize=(10, 6), ax=ax)
    plt.title(f'Pre: {selected_question}')
    plt.ylabel('Proportion of Responses')
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1))
    add_percentage(ax)
    plt.tight_layout()
    st.pyplot(fig)

# If the selected question is in the post survey data, plot a bar chart with percentages
elif selected_question in df_post.columns:
    fig, ax = plt.subplots()
    df_post[selected_question].value_counts(normalize=True).plot(kind='bar', color='green', figsize=(10, 6), ax=ax)
    plt.title(f'Post: {selected_question}')
    plt.ylabel('Proportion of Responses')
    plt.xticks(rotation=45)
    plt.gca().yaxis.set_major_formatter(plt.matplotlib.ticker.PercentFormatter(1))
    add_percentage(ax)
    plt.tight_layout()
    st.pyplot(fig)
