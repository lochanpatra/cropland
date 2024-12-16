import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """
This app is maintained by lochan patra.It uses for basemap,terrain map search and export.
"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://cdn.pixabay.com/photo/2013/07/12/18/35/world-153534_640.png"
st.sidebar.image(logo)

# Customize page title
st.title(" Geospatial Applications")

st.markdown(
    """
   
    """
)

st.header("Instructions")

markdown = """


"""

st.markdown(markdown)

m = leafmap.Map(minimap_control=True)
m.add_basemap("OpenTopoMap")
m.to_streamlit(height=500)
