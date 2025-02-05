#imports
import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import glob # may not need here, but in the notebook
import plotly.express as px # for hover in pie charts


st.write("""
# Google vs. Apple App Store Analysis
#### by Logan Warren
## Introduction
         
We use all kinds of mobile apps daily, whether they are from Google’s Play Store or Apple’s App Store. Despite each store offering millions of apps, I wanted to look into the differences between these two marketplaces and analyze differences in places such as, top categories, cost structures, and how users feel the quality is.
To explore this, I combined two large datasets from Kaggle (one for Google Play, one for Apple App Store) and created visualizations and interactive filters to answer questions such as:
- Are there more free or paid apps in one store?
- Which platform hosts more low-quality apps?
- How do categories differ, and which ones appear most frequently?

To approach answering these, I obtained the data, then combined, cleaned, and split these datasets into manageable parts and analyzed them through various ways displayed in visualizations below. 

""")

st.image("App Photo.jpg")

st.write("""
## Data Selection and Pitfalls

I chose two specific Kaggle datasets:
         
- Gauthamp10. (2020). https://www.kaggle.com/datasets/gauthamp10/apple-appstore-apps. Kaggle. (Apple)
- Lava18. (2018). https://www.kaggle.com/datasets/lava18/google-play-store-apps. Kaggle. (Google)

Each of these large datasets contained thousands of entries with overlapping columns like Category, Rating, Price etc.
- Why these datasets? These two sets contained enough similarity to allow for direct comparisons between the two stores. These were also some of the largest datasets I was able to find, providing plenty of data to analyze for both stores. 
- Pitfalls: The Apple dataset had some columns that Google’s did not, and vice versa. There were also plenty of rows that were not relevant to my data story such as App_Website. In addition to this, some rows had missing values, or a rating of “0” for apps that had no user reviews yet. For my analysis, I  decided to drop rows with a rating of 0 when focusing on app quality, as 0 would imply that the apps were unrated. 

""")

st.write("""
## How my Data Story Evolved
Initially, I simply wanted to see the stores top categories. As I cleaned the data, I noticed interesting questions about free vs. paid apps, and the possibility of one store hosting more lower end quality apps than the other. This shifted my focus to monetization and rating distributions:
- Does one store have a larger group of low rated (low quality) apps?
- Would free vs paid ratios differ significantly between Apple and Google?

With these questions, I built additional filters and interactive charts, like the comparing any Google category to any Apple category, to see how user ratings lineup when you focus on a specific domain such as Games, or Education.

## Data Transformations 
Because these datasets were very large with several thousands of rows, I chose to split them into smaller parts locally and then upload these parts to GitHub. Once In GitHub I was able to merge the split parts in my Jupyter Notebook using Python’s glob library, and successfully avoid memory constraints. I removed columns like developer websites and irrelevant text fields that didn't add value to the data store. I also filtered out zero ratings or NaN rating apps for certain quality analyses below. 

""")

# Loading in apple data from parts
@st.cache_data
def appleDataTogether():
    apple_parts = glob.glob("appleDataEdit_part*.csv")
    apple_frames = []
    for file in apple_parts:
        df = pd.read_csv(file)
        apple_frames.append(df)
    appleDataTogether = pd.concat(apple_frames, ignore_index=True)
    return appleDataTogether
# loading in google data from parts
@st.cache_data #caches the data so nothing has to reload all the datasets when interacted with. 
def googleDataTogether():
    google_parts = glob.glob("googleDataEdit_part*.csv")
    google_frames = []
    for file in google_parts:
        df = pd.read_csv(file)
        google_frames.append(df)
    googleDataTogether = pd.concat(google_frames, ignore_index=True)
    return googleDataTogether

###########################################################################################################################
# checking to make sure all parts combined when loaded
appleData = appleDataTogether()
googleData = googleDataTogether()

#st.write("Apple data shape:", appleData.shape)
#st.write("Google data shape:", googleData.shape)

#st.write("### Sample rows from Apple data:")
#st.dataframe(appleData.head())

#st.write("### Sample rows from Google data:")
#st.dataframe(googleData.head())
# Dont need these anymore - hopefully... 
###########################################################################################################################
# Top categories in Apple and Google app stores

st.title("Top 10 Categories for Each App Store")

st.write("Bar Charts for Google vs. Apple show the top 10 categories. Games takes the lead for Google, While Education is ontop for Apple's store")
st.write("This helps to see if users or developers are focused more on certain functional areas or entertainment")
google, apple = st.columns(2)

with google:
    st.write("## Google")
    googleTop = googleData["Category"].value_counts().head(10)
    fig1, ax1 = plt.subplots(figsize=(4,4))  #
    sns.barplot(x=googleTop.index, y=googleTop.values, ax=ax1)
    ax1.set_title("Google Play Store (Top 10)")
    ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)
    st.pyplot(fig1)

with apple:
    st.write("## Apple")
    appleTop = appleData["Primary_Genre"].value_counts().head(10)
    fig2, ax2 = plt.subplots(figsize=(4,4))
    sns.barplot(x=appleTop.index, y=appleTop.values, ax=ax2)
    ax2.set_title("Apple Store (Top 10)")
    ax2.set_xticklabels(ax2.get_xticklabels(), rotation=45)
    st.pyplot(fig2)
###########################################################################################################################
# Single Apple apps filtered by ratings 
#st.write("## Filter Apple Apps by Ratings ")
#st.write("Use the slider to pick a rating range and see how many apps fall within it.")

#minRating, maxRating = st.slider(
#    "Pick a range", 
#    min_value=0.0, 
#    max_value=5.0, 
#    step=0.5, 
#    value=(0.0,5.0)
#)

#filteredApple = appleData[
#    (appleData["Average_User_Rating"] >= minRating) & 
#    (appleData["Average_User_Rating"] <= maxRating)
#]

#fig3, ax3 = plt.subplots(figsize=(6,4))
#sns.histplot(filteredApple["Average_User_Rating"].dropna(), bins=20, color="orange", ax=ax3)
#ax3.set_title(f"Apple Ratings from {minRating} to {maxRating}")
#ax3.set_xlabel("Rating")
#st.pyplot(fig3)

#st.write(f"Number of apps in this rating range: {len(filteredApple)}")

###########################################################################################################################
# Replacing the single apple filter for the option of looking at Google / Apple or both. 

st.write("## Apps by Ratings for Apple, Google or Both")
st.write("Here, a slider lets you pick a rating range from 0-5, for either Apple, Google, or both overlapped. This shows how many apps fall into a specific range on each platform")
st.write("I found that Google had fewer apps scoring a perfect 5, while Apple had more 5-star apps proportionally. Meanwhile, in the 3-4.5 range, Google had a higher concentration showing that there are more quality apps in Googles Store")



choice = st.radio("Which platform do you want to filter?",("Apple","Google","Both"))

st.write("Use the slider to pick a range for the rating in the graph")
minRating, maxRating = st.slider("Pick a rating range", min_value=0.0, max_value=5.0, step=0.5, value=(0.0, 5.0))

# APPLE FILTER
if choice == "Apple": 
    filteredApple = appleData[(appleData["Average_User_Rating"] >= minRating) &(appleData["Average_User_Rating"] <= maxRating)]

    fig, ax = plt.subplots(figsize=(6,4))
    sns.histplot(filteredApple["Average_User_Rating"].dropna(), bins=20, color="orange", ax=ax)
    ax.set_title(f"Apple Ratings from {minRating} to {maxRating}")
    ax.set_xlabel("Rating")
    st.pyplot(fig)

    st.write(f"Number of apps in this range: {len(filteredApple)}")

#GOOGLE Filter
if choice == "Google":
    filteredGoogle = googleData[(googleData["Rating"] >= minRating) & (googleData["Rating"] <= maxRating)]
    fig, ax = plt.subplots(figsize=(6,4))
    sns.histplot(filteredGoogle["Rating"].dropna(), bins=20, color="blue", ax=ax)
    ax.set_title(f"Google Ratings from {minRating} to {maxRating}")
    ax.set_xlabel("Rating")
    st.pyplot(fig)

    st.write(f"Number of apps in this range: {len(filteredGoogle)}")

#Filter for BOTH
if choice == "Both":
    filteredApple = appleData[(appleData["Average_User_Rating"] >= minRating) & (appleData["Average_User_Rating"] <= maxRating)]
    filteredGoogle = googleData[(googleData["Rating"] >= minRating) & (googleData["Rating"] <= maxRating)]
    fig, ax = plt.subplots(figsize=(8,5))
    sns.histplot(filteredGoogle["Rating"].dropna(), bins=20, color="red", alpha=0.5, label="Google", ax=ax)
    sns.histplot(filteredApple["Average_User_Rating"].dropna(), bins=20, color="blue", alpha=0.5, label="Apple", ax=ax)
    ax.set_title(f"Ratings from {minRating} to {maxRating} (Both)")
    ax.set_xlabel("Rating")
    ax.set_ylabel("Count")
    ax.legend()
    st.pyplot(fig)


###########################################################################################################################
# Poor Quality Apps chart below
st.write("## Which Store Has More Poor Quality Apps?")
st.write("""Poor quality apps are defined as having a rating < 2
         The apps with ratings of 0, or NaN are filtered out so only rated apps are included in the percentage.""")


#google setup
googleRated = googleData[googleData['Rating'] > 0]
googlePoor = googleRated[googleRated['Rating'] < 2]
googlePoorLen = len(googlePoor)
googleRatedLen = len(googleRated)
#apple setup
appleRated = appleData[appleData['Average_User_Rating'] > 0]
applePoor = appleRated[appleRated['Average_User_Rating'] < 2]
applePoorLen = len(applePoor)
appleRatedLen = len(appleRated)

#Percent math for both
googlePoorMath = (googlePoorLen / googleRatedLen) * 100 if googleRatedLen else 0
applePoorMath = (applePoorLen / appleRatedLen) * 100 if appleRatedLen else 0
# Writing out the percent of poor quality apps in each of the stores.
st.write(f"Google poor quality apps: {googlePoorLen} / {googleRatedLen} "
         f"(~{googlePoorMath:.2f}%)")
st.write(f"Apple poor quality apps:  {applePoorLen} / {appleRatedLen} "
         f"(~{applePoorMath:.2f}%)")

#Graph for the poor quality apps.
platforms = ["Google", "Apple"]
poorPercent = [googlePoorMath, applePoorMath]

fig4, ax4 = plt.subplots(figsize=(6,4))
ax4.bar(platforms, poorPercent, color=['orange','blue'])
ax4.set_title("Percentage of Poor Quality Apps")
ax4.set_ylabel("Percentage")
st.pyplot(fig4)
###########################################################################################################################
# starting the compare between Google and Apple categories - 


st.write("## Compare Ratings for Any Google and Apple top 10 Category")
st.write("This comparison will allow for interaction from a user to pick a top Google category, and match it against an Apple category to see an overlapping histograms of rating distributions.")
st.write("It seems amongst the top categories of each store, Apple has more 5-star apps, while Google continues to sit in the 3-4.5 range for its ratings. ")




googleTop2= googleData["Category"].value_counts().head(10).index
appleTopGenres = appleData["Primary_Genre"].value_counts().head(10).index

colGoogle, colApple = st.columns(2)

with colGoogle:
    chosenGoogleCat = st.selectbox("Google Category:", googleTop2)

with colApple:
    chosenAppleGenre = st.selectbox("Apple Genre:", appleTopGenres)

st.write(f"Comparing: Google '{chosenGoogleCat}' vs. Apple '{chosenAppleGenre}'")


# filtering using the users interaction - 
googleSelection = googleData[googleData["Category"] == chosenGoogleCat]
appleSelection = appleData[appleData["Primary_Genre"] == chosenAppleGenre]

# Removing the na / 0 ratings again. 
googleSelectionRatings = googleSelection["Rating"].dropna()
googleSelectionRatings = googleSelectionRatings[googleSelectionRatings > 0]
appleSelectionRatings = appleSelection["Average_User_Rating"].dropna()
appleSelectionRatings = appleSelectionRatings[appleSelectionRatings > 0]

##Plotting the graphs -
fig, ax = plt.subplots(figsize=(8,5))
sns.histplot(googleSelectionRatings, label=f"Google {chosenGoogleCat}", color='red', bins=20, alpha=0.5, ax=ax)
sns.histplot(appleSelectionRatings, label=f"Apple {chosenAppleGenre}", color='blue', bins=20, alpha=0.5, ax=ax)

ax.set_title("Google vs Apple By Chosen Category")
ax.set_xlabel("Rating")
ax.set_ylabel("Count")
ax.legend()

st.pyplot(fig)

###########################################################################################################################
# 2 pie charts showing the percent of free vs paid apps in the 2 stores 
st.write("## Free vs. Paid Apps")
st.write("I chose to use pie charts here to see how many apps are free or paid in each store. About 98.1% of Google apps are free, and less than 2% are paid. Apple on the other hand is slightly more balanced, but still heavily free with 91.6% free and 8.37% paid for. However these do not take into consideration the payments present inside any type of app for either platform. ")
googlePie, applePie = st.columns(2)
with googlePie:
    st.write("## Google")
    googleFreePaid = googleData["Free"].value_counts()
    labels = ["Free","Paid"] if len(googleFreePaid)==2 else googleFreePaid.index
    figPlotly = px.pie(
        names=labels,
        values=googleFreePaid,
        title="Google Free vs. Paid",
        color_discrete_sequence=["blue","orange"]
    )
    st.plotly_chart(figPlotly)

with applePie:
    st.write("## Apple")
    appleFreePaid = appleData["Free"].value_counts()
    labels = ["Free","Paid"] if len(appleFreePaid)==2 else appleFreePaid.index

    figPlotly = px.pie(
        names=labels,
        values=appleFreePaid,
        title="Apple Free vs. Paid",
        color_discrete_sequence=["blue","orange"]
    )
    st.plotly_chart(figPlotly)


st.write("""
# Conclusion
## Answered Questions:
#### Are there more free or paid apps in one store?
- The interactive Pie charts revealed that Google overwhelmingly favors free apps with less then 2% of apps paid, whereas Apple has a higher proportion of paid apps at 8% (100K apps). This can show that if developers wamt to launch a paid app, Apple might be the best choice, since Google users expect their apps to be mostly free.
#### Which platform hosts more low quality apps?
- After filtering out zero/missing ratings, Google had only 1% of its rated apps under 2 stars, versus Apple at nearly 9%. While there are certainly outside factors, it still appears Apple has the higher amount of low rated apps.
#### How do categories differ across Apple and Google?
- Bar charts comparing the top 10 categories showed that Apple’s top 10 lean more towards entertainment like Games. Google’s store on the other hand focused more on practical apps like education and music/audio. In addition to this, with the compare ratings for Apple, Google or Both apps, it showed that Apple frequently has more 5-star ratings in a given category where Google apps often cluster around the 3-4.5 range. 


## Benefits to Visualizing This Data
Visualizing through interactive bar charts, histograms, and pie charts allowed me to quickly compare categories or rating distributions side by side. I was able to provide immediate insight on how poor quality or free vs. paid proportions shift across stores or categories. And they were able to have interactive elements so a user can ask their own questions, without writing code.

## Potential Harm or Misinterpretation of Data
An app's rating can be influenced by marketing, brand or possibly review bombing. I chose to go with < 2 as poor to keep the analysis simplistic, but there is definitely much more that should go into considering an app to be poor. The datasets I chose are not frequently updated, and possibly not complete with all app store data, this could leave some categories to go underrepresented. Concluding that Apple has worse apps because it has a higher share of below 2 ratings may be misleading if many apple users tend to leave extreme negative or positive reviews more readily. 

## Overall Reflection
The interactive additions to the visuals, like the slider and radio buttons can let other users toggle what data they’d like to see from my work. I feel this approach was more engaging than static data. Regarding failed attempts, I initially tried to load entire datasets all in one go, causing memory and GitHub file size issues. Splitting into parts, then putting them back together in Python solved this issue. I also used static Matplotlib pie charts at first, with hard to read numbers, and instead chose to go with Plotly since it had a way to hover over the charts. For areas to revise, I could incorporate app size or update frequency for a more in depth analysis, since these columns were present in the data. What I liked best was creating the interactive visuals. I like using Streamlit and seeing how the changes made with radio buttons or sliders could happen in real time. 



""")