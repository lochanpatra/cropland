import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

# Customize the sidebar
markdown = """

"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://emojipedia.org/laptop"
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
