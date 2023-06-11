from st_pages import Page, show_pages, add_page_title
from PIL import Image
import streamlit.components.v1 as components
import streamlit as st
from bokeh.plotting import figure, show

add_page_title()

# Specify what pages should be show n in the sidebar, and what their titles and icons
# should be
show_pages(
    [
        Page("./streamlit_app.py", "Planet Playground", "🪐"),
        Page("./pages/impact_prediction.py", "Impact Prediction", "🌕"),
        Page("./pages/inverse_prediction.py", "Inverse Prediction", "🌑"),
    ]
)

# image = Image.open("./figures/jwst_test_img.jpg")
image = Image.open("./figures/ImpactImage.jpeg")

st.image(image)

st.title("Hello :blue[Planet]")

st.header("SPH giant impact simulation")
st.write("Check in 3D how differnet giant impact looks like.")

tab1, tab2, tab3 = st.tabs(["Head-on", "Low speed oblique", "Erosive hit-and-run"])

with tab1:
    st.write(
        "Below is a SPH simulation of a head-on giant impact between two 1.0 $M_{\oplus}$ planets. This is an interactive 3D plot, you can zoom in/out, rotate and pan the plot. The lime particles in the center if you zoom in, are the bound particles from the largest remnant"
    )
    HtmlFile = open("./k3d_files/K3D-withBound.html", "r", encoding="utf-8")
    source_code = HtmlFile.read()

    components.html(source_code, height=600, width=600)


with tab2:
    st.write(
        "In the middle of low speed oblique giant impact between two 1.0 $M_{\oplus}$ planets at b=0.4 and 14.5 km/s. When Speed is low, the two colliding planets will finally merge into one."
    )
    HtmlFile = open("./k3d_files/K3D-lowspeed-b0d4.html", "r", encoding="utf-8")
    source_code = HtmlFile.read()
    components.html(source_code, height=600, width=600)

with tab3:
    st.write(
        "High speed oblique giant impact between two 1.0 $M_{\oplus}$ planets at b=0.4 and 44.5 km/s. When the speed is high enough, the imapct transits to erosive hit-and-run whereas the largest and second largest remnant have similar mass and iron fraction."
    )
    HtmlFile = open("./k3d_files/K3D-m1d0-highspeed-b0d4.html", "r", encoding="utf-8")
    source_code = HtmlFile.read()
    components.html(source_code, height=600, width=600)


# HtmlFile = open("./K3D_m1d0_HighSpeed.html", "r", encoding="utf-8")\
