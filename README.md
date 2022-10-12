# CMU Interactive Data Science Assigment 3

* **Team members**: schikara@andrew.cmu.edu 
* **Online URL**: https://share.streamlit.io/CMU-IDS-Fall-2022/YYYY/master/streamlit_app.py (Update YYYY with your repo name)

## Instructions

### Run Locally

Check out the Streamlit [getting started](https://docs.streamlit.io/en/stable/getting_started.html) guide and setup your Python environment.

To run the application locally, install the dependencies with `pip install -r requirements.txt` (or another preferred method to install the dependencies listed in `requirements.txt`). Then run `streamlit run streamlit_app.py`.

### Deploy to Streamlit Sharing

Before you can view your application online, you need to have it set up with Streamlit Cloud. 
Sign up for a [free Starter Streamlit Cloud account](https://streamlit.io/cloud). 

Then, go to [share.streamlit.io](https://share.streamlit.io) to deploy your Streamlit app by creating a new app and pointing it to your github repo.

Once the repo is set up, please update the URL as the top of this readme and add the URL as the website for this GitHub repository.

### Deliverables

- [ ] An interactive data science or machine learning application using Streamlit.
- [ ] The URL at the top of this readme needs to point to your Streamlit application online. The application should also list the names of the team members. 
- [ ] A write-up that describes the goals of your application, justifies design decisions, and gives an overview of your development process. Use the `writeup.md` file in this repository. You may add more sections to the document than the template has right now.

### Goals & Description:

I used the Nobel Prize winners dataset (1901-2020) to see the age distribution across prize categories and gender to see how the distribution looks like. Are there some patterns? How has the trend evolved over years given the advancements in technology and other sectors? 
Do some categories have relatively younger winners than others? Gender composition in the entire dataset? Is there gender parity? Is the trend improving or do we need to do more on the same front?
The size of the dataset was comparatively small and made the app relatively more responsive.

### The rationale for design decisions?

Giving the user enough room to play around with the subset of the dataset was the main goal behind designing the sidebar. The end user can pick and choose a year range between 1901-2020 to interact with the data. Scatterplots are great at depicting quite a handful of information. I used them extensively to portray every single prize winner.
Scatterplots are also great at conveying a lot of information with the help of a tooltip. I made interactive scatterplots so that if the user needs to see all the relevant information with respect to a particular winner they can just hover over the point on the scatterplots.
Another idea was to do some regression analysis on the mean age to see how the trend looks over the year. As a matter of fact, it came out to be a bit surprising that the winners are getting older over the years when they receive prizes. The usage of interactive bar charts also added to the interactivity of the application.

The piazza post around grouping up for the project did not materialize. Hence, I finished the project on my own. I spent around 25+ hours on this app. The majority of the time was spent on the learning and researching altair and streamlit. I started early given I had super demanding obligations such as Cloud Computing. Starting early helped me be confident and gave me enough room to play around with things like bar chart-based slider.
