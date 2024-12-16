import streamlit as st
import leafmap.foliumap as leafmap

st.set_page_config(layout="wide")

markdown = """

"""

st.sidebar.title("About")
st.sidebar.info(markdown)
logo = "https://cdn.pixabay.com/photo/2017/07/27/09/56/sphere-stone-2544690_640.png"
st.sidebar.image(logo)

st.title("Split-panel Map")

with st.expander("See source code"):
    with st.echo():
        m = leafmap.Map()
        m.split_map(
            left_layer="ESA WorldCover 2020 S2 FCC", right_layer="ESA WorldCover 2020"
        )
        m.add_legend(title="ESA Land Cover", builtin_legend="ESA_WorldCover")

m.to_streamlit(height=700)
