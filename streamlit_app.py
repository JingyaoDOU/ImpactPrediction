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

image = Image.open("./figures/jwst_test_img.jpg")

st.image(image)

st.title("Hello :blue[Planet]")

st.header("SPH giant impact simulation")


# # create a new plot with a title and axis labels
# p = figure(title="Simple line example", x_axis_label="x", y_axis_label="y")
# # add a line renderer with legend and line thickness to the plot
# p.line(x, y, legend_label="Temp.", line_width=2)
# # show the results
# # show(p)
# st.bokeh_chart(p, use_container_width=True)
HtmlFile = open("./K3D_m1d0_HighSpeed.html", "r", encoding="utf-8")
source_code = HtmlFile.read()
# print(source_code)
components.html(source_code, height=600, width=600)
