import streamlit as st
import pandas as pd
import plost

st.set_page_config(layout='wide', initial_sidebar_state='expanded')

# Load the data
liver_cancer_across_countries = pd.read_csv('regional liver cancer death rate per 100,000.csv')
liver_cancer_death_rate = pd.read_csv('liver cancer death rate per 100,000.csv')

#############################################################################################################################
# Sidebar

st.sidebar.header('Liver cancer and AUD in Cyprus Dashboard `Parameters`')

# Select box to show/hide visualizations
selected_option = st.sidebar.selectbox("Select Visualizations", ["Liver Cancer Death Rate", "Alcohol Use Disorder"])

# Bar chart parameter
selected_year = st.sidebar.slider('Select a Year', 
                                  min_value=int(liver_cancer_across_countries['Year'].min()), 
                                  max_value=int(liver_cancer_across_countries['Year'].max()), 
                                  value=2019, step=1)


###########################################################################################################################

# Custom header
if selected_option == "Liver Cancer Death Rate":

    # Sidebar for selecting gender using a dropdown
    selected_gender = st.sidebar.selectbox("Select Gender", liver_cancer_death_rate['Sex'].unique())

    # Sidebar for selecting age using a dropdown
    selected_age = st.sidebar.selectbox("Select Age Group", liver_cancer_death_rate['Age'].unique())

    st.markdown("<h2 style='text-align: left;'>Liver Cancer Death Rate in the East Mediterranean Region</h2>", unsafe_allow_html=True)

    # Main content
    c1, c2 = st.columns((1, 1))

    with c1:
        st.write("Deaths per 100,000")
        data_for_year = liver_cancer_across_countries[liver_cancer_across_countries['Year'] == selected_year]
        data_for_year_sorted = data_for_year.sort_values(by='Value', ascending=False)

        plost.bar_chart(
            data=data_for_year_sorted,
            bar='Location',
            value='Value',
            use_container_width=True,  # Ensure the plot uses the full width of the container
            height=300,  # Set a fixed height for the plot
            color='Location',
            legend=None
        )

    with c2:
        st.write("Deaths per 100,000")
        # Create the line plot
        plost.line_chart(
            data=liver_cancer_across_countries,
            x='Year',
            y='Value',
            color='Location',
            height=300,  # Set the same fixed height for the plot
            use_container_width=True,
            legend=None
        )

##############################################################################################################################

    st.markdown("<h2 style='text-align: left;'>Trends in Liver Cancer Death Rates Across Demographics</h2>", unsafe_allow_html=True)

    # Define a function to create the gender graph
    def create_gender_graph(selected_age, selected_gender):
        # Filter the data for Cyprus and the selected age group
        data_cyprus_selected_age = liver_cancer_death_rate[(liver_cancer_death_rate['Location'] == 'Cyprus') & 
                                                            (liver_cancer_death_rate['Age'] == selected_age)]

        # Filter the data for the selected gender
        selected_data = data_cyprus_selected_age[data_cyprus_selected_age['Sex'] == selected_gender]

        # Create line plots for each sex
        fig = plost.line_chart(
            data=selected_data,
            x='Year',
            y='Value',
            color='Location',
            height=300,  # Set the same fixed height for the plot
            use_container_width=True,
            legend=None
        )

        return fig

    # Render the gender graph in c3
    c3, c4 = st.columns((1, 1))
    with c3:
        st.write("Deaths per 100,000")
        create_gender_graph(selected_age, selected_gender)  # Pass both selected_age and selected_gender

    with c4:
        # Filter data for the selected year
        data_for_selected_year = liver_cancer_death_rate[liver_cancer_death_rate['Year'] == selected_year]

        # Filter the data for males and females
        male_data = data_for_selected_year[data_for_selected_year['Sex'] == 'Male']
        female_data = data_for_selected_year[data_for_selected_year['Sex'] == 'Female']

        # Calculate the total count for the selected year
        total_count = male_data['Value'].sum() + female_data['Value'].sum()

        # Calculate the percentage of males and females
        male_percentage = (male_data['Value'].sum() / total_count) * 100
        female_percentage = (female_data['Value'].sum() / total_count) * 100

        # Create a DataFrame for the percentages
        gender_percentage_data = pd.DataFrame({
            'Gender': ['Male', 'Female'],
            'Percentage': [male_percentage, female_percentage]
        })

        # Create a pie chart for the percentages
        plost.pie_chart(
            data=gender_percentage_data,
            theta='Percentage',  # Column containing the percentages for each category
            use_container_width=True,  # Ensure the plot uses the full width of the container
            height=300,
            color='Gender'  
        )

#############################################################################################################
######################################################################################################3######################
################################################################################################################


else:
    age_group_labels = {
    'Current number of cases of alcohol use disorders per 100 people, in both sexes aged under 5': '>5 years',
    'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 5-14 years': '5-14 years',
    'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 15-49 years': '15-49 years',
    'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 50-69 years': '50-69 years',
    'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 70+ years': '70+ years'
    }

    # Create a sidebar dropdown to select the age group
    selected_age_group_label = st.sidebar.selectbox('Select Age Group', list(age_group_labels.values()))

    regional_alcohol_data = pd.read_csv('world-share-with-alcohol-use-disorders.csv')
    regional_alcohol_data["Current number of cases of alcohol use disorders per 100 people, in both sexes aged age-standardized"]=regional_alcohol_data["Current number of cases of alcohol use disorders per 100 people, in both sexes aged age-standardized"]*1000
    regional_alcohol_data["Value"]=regional_alcohol_data["Current number of cases of alcohol use disorders per 100 people, in both sexes aged age-standardized"]

    # Filter data for specific entities
    entities_of_interest = ['Cyprus', 'Turkey', 'Lebanon', 'Palestine', 'Jordan']
    filtered_data = regional_alcohol_data[regional_alcohol_data['Entity'].isin(entities_of_interest)]
    
    st.markdown("<h2 style='text-align: left;'>Alcohol Use Disorder Rates in the East Mediterranean Region</h2>", unsafe_allow_html=True)

    # Main content
    c3, c4 = st.columns((1, 1))

    with c3:
        st.write("Per 100,000")
        data_for_year = filtered_data[filtered_data['Year'] == selected_year]

        # Sort data in descending order based on the death rate
        data_for_year_sorted_1 = data_for_year.sort_values(by='Value', ascending=False)

        plost.bar_chart(
            data=data_for_year_sorted_1,
            bar='Entity',
            value='Value',
            use_container_width=True,  # Ensure the plot uses the full width of the container
            height=300,  # Set a fixed height for the plot
            color='Entity',
            legend=None
        )
        
    with c4:
        st.write("Per 100,000")
        plost.line_chart (
            data=filtered_data,
            x='Year',
            y='Value',
            color='Entity',
            height=300,
            use_container_width=True,
            legend=None
        )
        
###################################################################################################################################

    number_alcohol_use_disorder = pd.read_csv('number-with-alcohol-use-disorders.csv')
    number_alcohol_use_disorder_copy = number_alcohol_use_disorder.copy()
    number_alcohol_use_disorder_copy["Males"] = number_alcohol_use_disorder_copy["Current number of cases of alcohol use disorders, in males aged all ages"]
    number_alcohol_use_disorder_copy["Females"] = number_alcohol_use_disorder_copy["Current number of cases of alcohol use disorders, in females aged all ages"]
    number_alcohol_use_disorder_copy = number_alcohol_use_disorder_copy[number_alcohol_use_disorder_copy['Entity'] == 'Cyprus']
    number_alcohol_use_disorder_copy['Total'] = number_alcohol_use_disorder_copy['Males'] + number_alcohol_use_disorder_copy['Females']
    number_alcohol_use_disorder_copy.reset_index(drop=True, inplace=True)
    number_alcohol_use_disorder_copy['Percentage Males'] = (number_alcohol_use_disorder_copy['Males'] / number_alcohol_use_disorder_copy['Total']) * 100
    number_alcohol_use_disorder_copy['Percentage Females'] = (number_alcohol_use_disorder_copy['Females'] / number_alcohol_use_disorder_copy['Total']) * 100

    population = pd.read_csv('population-by-age-group.csv')
    population_copy = population.copy()
    population_copy['Total Population'] = population_copy.iloc[:, 3:].sum(axis=1)
    cyprus_pop = population_copy[population_copy['Entity'] == 'Cyprus']
    cyprus_pop = cyprus_pop[(cyprus_pop['Year'] >= 1990) & (cyprus_pop['Year'] <= 2019)]
    cyprus_pop.reset_index(drop=True, inplace=True)

    columns_to_remove = [
        'Population by broad age group - Sex: all - Age: 65+ - Variant: estimates',
        'Population by broad age group - Sex: all - Age: 25-64 - Variant: estimates',
        'Population by broad age group - Sex: all - Age: 15-24 - Variant: estimates',
        'Population by broad age group - Sex: all - Age: 5-14 - Variant: estimates',
        'Population by broad age group - Sex: all - Age: 0-4 - Variant: estimates'
    ]

    cyprus_pop = cyprus_pop.drop(columns=[col for col in columns_to_remove if col in cyprus_pop.columns])
    cyprus_pop["total alcohol use disorders"] = number_alcohol_use_disorder_copy['Total']
    cyprus_pop['Rate per 100,000'] = (cyprus_pop['total alcohol use disorders'] / cyprus_pop['Total Population']) * 100000

    aud_by_age = pd.read_csv('prevalence-of-alcohol-use-disorders-by-age.csv')
    columns_to_convert = [
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged all ages',
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 70+ years',
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 15-49 years',
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 5-14 years',
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 50-69 years',
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged age-standardized',
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged under 5'
    ]

    # Convert each column to per 100,000
    for column in columns_to_convert:
        aud_by_age[column] *= 1000

#################################################################################################################

    # Assuming `aud_by_age` is your DataFrame
    plot = aud_by_age[aud_by_age['Entity'] == 'Cyprus']

    # Extract the relevant columns including 'Year' for melting
    alcohol_use_columns = [
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged under 5',
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 5-14 years',
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 15-49 years',
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 50-69 years',
        'Current number of cases of alcohol use disorders per 100 people, in both sexes aged 70+ years'
    ]

    # Find the corresponding column name from the selected label
    selected_age_group_column = [key for key, value in age_group_labels.items() if value == selected_age_group_label][0]

    # Filter the DataFrame to only include the selected age group
    filtered_plot = plot[['Year', selected_age_group_column]].rename(columns={selected_age_group_column: 'Alcohol Use Disorders'})

    # Display the header
    st.markdown("<h2 style='text-align: left;'>Alcohol Use Disorder Rates Across Demographics</h2>", unsafe_allow_html=True)

    # Display the column layout
    c7, c8 = st.columns((1, 1))
    with c7:
        st.write("Per 100,000")
        # Create the line chart
        st.line_chart(data=filtered_plot.set_index('Year'))

    with c8:
        import plotly.express as px
        
        data_for_year_grouped = number_alcohol_use_disorder_copy[number_alcohol_use_disorder_copy['Year'] == selected_year]

        gender_percentage_data1 = pd.DataFrame({
            'Gender': ['Male', 'Female'],
            'Percentage': [data_for_year_grouped['Percentage Males'].iloc[0], data_for_year_grouped['Percentage Females'].iloc[0]]
        })
        
        plost.pie_chart(
            data=gender_percentage_data1,
            theta='Percentage',  # Column containing the percentages for each category
            use_container_width=True,  # Ensure the plot uses the full width of the container
            height=300,
            color='Gender'  
        )
        


st.sidebar.markdown('''
---
Created by [Aya El Saoudi](https://www.linkedin.com/in/aya-el-saoudi/).
''')