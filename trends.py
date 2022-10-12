#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Oct  1 12:27:29 2022

@author: shashankchikara
"""
# import relevant packages
import streamlit as st
import pandas as pd
import altair as alt
from PIL import Image

#Create two column layout to display title and image
cols = st.columns(2,gap="large")
with cols[1]:
    st.image(
            "https://upload.wikimedia.org/wikipedia/en/e/ed/Nobel_Prize.png",
            width=200
        )
with cols[0]:
    st.title("Nobel Prize trends")
with st.spinner(text="Loading data..."):
    df_cc=pd.read_csv("nobel_final.csv",encoding='utf8', encoding_errors='ignore') 
df_cc.columns = df_cc.columns.str.replace(' ','_')

#A little cleanup on the dataset
df_cc["name_of_university"] = df_cc.name_of_university.fillna("Not Reported")
df_cc["city_of_university"] = df_cc.city_of_university.fillna("Not Reported")
df_cc["country_of_university"] = df_cc.country_of_university.fillna("Not Reported")


# Create a sidebar the helps the user slice the data set based on year ranges
with st.sidebar:
    st.write("Pick one of the following Year ranges for the dataset.")
    #Add radio button
    add_radio = st.radio(
        "Choose a range",
        ('1901-2020', '1950-2020','1990-2020','2000-2020')
    )
    #Create form with a submit button
    with st.form(key='my_form'):
        st.write ("OR enter your own range")
        st.write ("FROM")
        uifrm = st.text_input("Enter an Year >=1901 & <=2020", 1901)
        st.write ("To")
        uito = st.text_input("Enter an Year >=1901 & <=2020", 2020)
        submit_button = st.form_submit_button(label='Submit') 
    st.write("Disclaimer: This is an educational project")

# Based on radio selection, take relevant action
varto = 2021
if add_radio == '1901-2020' :
    varfrom = 1900
    df_new = df_cc[(varfrom < df_cc['year']) & (df_cc['year'] < varto)]
if add_radio == '1950-2020' :
    varfrom = 1949
    df_new = df_cc[(varfrom < df_cc['year']) & (df_cc['year'] < varto)]
if add_radio == '1990-2020' :
    varfrom = 1989
    df_new = df_cc[(varfrom < df_cc['year']) & (df_cc['year'] < varto)]
if add_radio == '2000-2020' :
    varfrom = 1999
    df_new = df_cc[(varfrom < df_cc['year']) & (df_cc['year'] < varto)]
# Action to be performed when user clicks on submit button
if submit_button:
    varfrom = int(uifrm)
    varto = int(uito)
    if varfrom > 1900 and varfrom < 2021:
        if varto >= varfrom and varto <2021:
            df_new = df_cc[(varfrom < df_cc['year']) & (df_cc['year'] < varto)]
        else:
            st.error("Please enter a valid range") 
    

st.text("Economists tend to be older? Are women represented equally across all categories?")
st.text("Use interactive bar chart to slice or slide and get insights")

#Create a scatterplot that has barchart as slider
select_year = alt.selection_interval(encodings=['x'])
#Bar chart that works as slider
bar_slider = alt.Chart(df_new).mark_bar().encode(
    x='year',
    y='count()').properties(height=50,width=500).add_selection(select_year)
#Scatter plot that can handle interactions
scatter_plot = alt.Chart(df_new).mark_circle().encode(
    x='age_get_prize',
    y='category',
    color='gender',
    tooltip=['firstname','surname','born_country_code','country_of_university','name_of_university','age_get_prize'],
    opacity=alt.condition(
        select_year,
        alt.value(0.7), alt.value(0.0))).properties(
    width=500,
    height=400
)
#Display Scatter plot and bar slider
st.altair_chart(scatter_plot & bar_slider)

df_ctrygrp = df_new[['country_of_university', 'year']].groupby(['country_of_university', 'year']).sum() \
  .groupby(level=0).cumsum().reset_index()

#Create a regression plot
#https://altair-viz.github.io/user_guide/transform/regression.html

degree_list = [1, 3, 5]
base = alt.Chart(df_new).mark_circle(color="gray").encode(
        alt.X("year" ,scale=alt.Scale(domain=[varfrom,varto])), alt.Y("age_get_prize")
).properties(width=350,height=300)
polynomial_fit = [
    base.transform_regression(
        "year", "age_get_prize", method="poly", order=order, as_=["year", str(order)]
    )
    .mark_line()
    .transform_fold([str(order)], as_=["degree", "age_get_prize"])
    .encode(alt.Color("degree:N"))
    for order in degree_list
]

#Display Regression plot
chr=alt.layer(base, *polynomial_fit)


#Layered scatter with histogram to represent mean age for genders
# https://altair-viz.github.io/gallery/scatter_with_layered_histogram.html

selector = alt.selection_single(empty='all', fields=['gender'])

color_scale = alt.Scale(domain=['male', 'female'],
                        range=['#1f50c3', '#ee24f5'])

base = alt.Chart(df_new).properties(
    width=250,
    height=250
).add_selection(selector)

points = base.mark_point(filled=True, size=200).encode(
    x=alt.X('mean(age_get_prize):Q',
            scale=alt.Scale(domain=[0,120])),
    y=alt.Y('mean(age):Q',
            scale=alt.Scale(domain=[0,120])),
    color=alt.condition(selector,
                        'gender:N',
                        alt.value('lightgray'),
                        scale=color_scale),
)

hists = base.mark_bar(opacity=0.5, thickness=100).encode(
    x=alt.X('age_get_prize',
            bin=alt.Bin(step=5), # step keeps bin size the same
            scale=alt.Scale(domain=[0,120])),
    y=alt.Y('count()',
            stack=None,
            scale=alt.Scale(domain=[0,200])),
    color=alt.Color('gender:N',
                    scale=color_scale)
).transform_filter(
    selector
)

st.write("Are Nobel prize winners getting older over years? What's the mean for both genders?")
#Display regression plot and mean scatter plot with histogram
cols = st.columns(2)
with cols[0]:
    st.altair_chart(chr)
with cols[1]:
    st.altair_chart(points | hists)


# Interactive scatterplots which use three features
#Re-used from Assignment 2
features = [ "age_get_prize", "year","age"]
corelchart = alt.Chart(df_new).mark_point().encode(
    alt.X(alt.repeat("column"), scale = alt.Scale(zero=False), type="quantitative"),
    alt.Y(alt.repeat("row"), scale = alt.Scale(zero=False), type="quantitative"),
    alt.Color("gender"),
    tooltip=['firstname','surname','born_country_code','country_of_university','name_of_university','age_get_prize']
).properties(
    width=250,
    height=175
).repeat(
    row=features,
    column=features
)

st.altair_chart(corelchart)
#group univerity and category to get relevant counts
university_and_category = df_new.groupby('name_of_university')['category'].value_counts().to_frame()
st.write("How does the university affiliation of winners look across categories (counts)?")
st.dataframe(university_and_category, use_container_width=1)

# Reused from Lab
st.write("Where did the nobel prize winners go to school?")
ctry_br = alt.selection_multi(fields=['country_of_university'])
cat_br = alt.selection_multi(fields=['category'])
cols = st.columns(2)
with cols[0]:
    ctry_chart = alt.Chart(df_new).mark_bar().encode(
    x=alt.X('country_of_university', sort='x'),
    y='count()',
    color=alt.condition(ctry_br, alt.value('orangered'), alt.value('lightgray'))
).transform_filter(cat_br).add_selection(ctry_br).interactive().properties(
    width=400,
    height=400
)
with cols[1]:
    cat_chart = alt.Chart(df_new).mark_bar().encode(
    x=alt.X('count()'),
    y=alt.Y('category', sort='-x'),
    color=alt.condition(cat_br, alt.value('deepskyblue'), alt.value('lightgray'))
).transform_filter(ctry_br).add_selection(cat_br).interactive().properties(
    width=400,
    height=400
)

cat_chart.configure_axisY(maxExtent = 20)
st.altair_chart(ctry_chart | cat_chart)
cols = st.columns(3)
with cols[2]:
    st.header("More coming soon!")
