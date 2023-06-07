import streamlit as st
import numpy as np
import pandas as pd

import plotly.subplots as sp
from st_pages import Page, show_pages, add_page_title

# import colorcet as cc

# import seaborn as sns
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import streamlit.components.v1 as components
import prediction

# from st_metric import style_metric_cards


all_inone = pd.read_csv("./all_in_one.csv", dtype={"round_m_tar": str, "b_cat": str})


# page_name = ["Impact Prediction", "Inverse Prediction", "Visualization"]
# page = st.radio(label="Navigation", options=page_name)

# add_page_title()

# # Specify what pages should be shown in the sidebar, and what their titles and icons
# # should be
# show_pages(
#     [
#         Page("streamlit_app.py", "Home", "🏠"),
#         Page("other_pages/page2.py", "Page 2", ":books:"),
#     ]
# )


st.info(
    "Predict the result of a collision given: Mass of target planet ($M_{\oplus}$), impact velocity (km/s) and impact parameter  ($sin(\\theta)$)."
)
st.warning(
    "Current model only predict same-sized collision: $M_{tar}$ = $M_{imp}$ or $\gamma$ = 1"
)
target_mass = st.number_input(
    "Enter target planet mass in $M_{\oplus}$",
    min_value=0.05,
    max_value=20.0,
    value=1.0,
    step=0.5,
)
impact_velocity = st.number_input("Enter impact velocity in km/s", value=20.0, step=1.0)
b_data_widget = st.radio(
    label="Impact parameter", options=[0.0, 0.2, 0.3, 0.4, 0.5], horizontal=True
)
if b_data_widget == 0.0:
    Q_norm, mlr, ratio_mlr, Zfe = prediction.head_on_predict(
        target_mass, impact_velocity
    )
else:
    Q_norm, mlr, ratio_mlr, Zfe = prediction.ob_predict(
        target_mass, impact_velocity, b_data_widget
    )
    Q_norm = float(Q_norm)
    mlr = float(mlr)
    ratio_mlr = float(ratio_mlr)
    Zfe = float(Zfe)

col1, col2, col3 = st.columns(3)

if ratio_mlr >= 0.1:  # .all():
    col1.metric("Largest remnant mass ($M_{\oplus}$)", "%.2f" % mlr)
    col2.metric("Core fraction", "%.1f %%" % (100 * Zfe))
    col3.metric("$M_{lr}$/$M_{total}$", "%.1f %%" % (100 * ratio_mlr))

else:
    st.error("Terminating...", icon="🚨")
    st.error(
        "Please try a smaller velocity as current velocity tends to enter the super-catastrophic regime."
    )
    st.error(
        "Remants will tend to split into several small pieces and the final fate of these small shreds is currently unpredictable."
    )

    col1.metric("Largest remnant mass ($M_{\oplus}$)", "Unknown")
    col2.metric("Core fraction", "Unknown")
    col3.metric("$M_{lr}$/$M_{total}$", "Unknown")

# style_metric_cards()
# fig_mlr = px.scatter(
#     data_frame=all_inone.loc[all_inone["b"] == 0],
#     x="Q_norm",
#     y="ratio_lr",
#     color="round_m_tar",
# )
# fig_zfe = px.scatter(
#     data_frame=all_inone.loc[all_inone["b"] == 0],
#     x="Q_norm",
#     y="Z_Fe_lr",
#     color="round_m_tar",
# )
# fig = make_subplots(rows=1, cols=2)
# fig.add_trace(
#     go.Scatter(
#         x=all_inone.loc[all_inone["b"] == 0, "Q_norm"],
#         y=all_inone.loc[all_inone["b"] == 0, "ratio_lr"],
#         mode="markers",
#         marker=dict(
#             color=all_inone.loc[all_inone["b"] == 0, "round_m_tar"],
#             colorscale="Viridis",
#         ),
#         name="data",
#     ),
#     row=1,
#     col=1,
# )

# fig.add_trace(
#     go.Scatter(
#         x=all_inone.loc[all_inone["b"] == 0, "Q_norm"],
#         y=all_inone.loc[all_inone["b"] == 0, "Z_Fe_lr"],
#         mode="markers",
#         marker=dict(
#             color=all_inone.loc[all_inone["b"] == 0, "round_m_tar"],
#             colorscale="Viridis",
#         ),
#         name="Target planet mass $M_{\oplus}$",
#     ),
#     row=1,
#     col=2,
# )
# for trace in fig_mlr["data"]:
#     fig.add_trace(go.Scatter(trace), row=1, col=1)

# for trace in fig_zfe["data"]:
#     fig.add_trace(go.Scatter(trace), row=1, col=2)

# Add a shared coloraxis
p_m_z = st.radio(label="Visulization", options=["Mass ratio", "Core fraction"])
if p_m_z == "Mass ratio":
    y_out = "ratio_lr"
    y_label = "Largest remnant mass ratio"
    y_plot = ratio_mlr
else:
    y_out = "Z_Fe_lr"
    y_label = "Largest remnant core fraction"
    y_plot = Zfe

if b_data_widget == 0.0:
    if target_mass < 1.0:
        all_inone_select = all_inone.loc[
            (all_inone["b"] == b_data_widget) & (all_inone["M_tar"] < 1.0)
        ]
    else:
        all_inone_select = all_inone.loc[
            (all_inone["b"] == b_data_widget) & (all_inone["M_tar"] > 1.0)
        ]
    fig = px.scatter(
        data_frame=all_inone_select,
        x="Q_norm",
        y=y_out,
        color="round_m_tar",
        hover_name="M_tar",
        log_y=False,
        width=500,
        labels={"round_m_tar": "Target planet mass"},
    )
    fig.update_layout(xaxis_title="Normalized impact energy")
    fig.update_layout(yaxis_title=y_label)

else:
    all_inone_select = all_inone.loc[all_inone["b"] > 0.1]

    # fig_tmp1 = go.Figure()
    # for cat_tar in all_inone_select["round_m_tar"].unique():
    #     fig_tmp1.add_trace(
    #         go.Scatter(
    #             x=all_inone_select.loc[
    #                 all_inone_select["round_m_tar"] == cat_tar, "Q_norm"
    #             ],
    #             y=all_inone_select.loc[
    #                 all_inone_select["round_m_tar"] == cat_tar, y_out
    #             ],
    #             mode="markers",
    #             # marker=dict(color=cat_tar),
    #         )
    #     )
    # fig_tmp2 = go.Figure()
    # for cat_b in all_inone_select["b_cat"].unique():
    #     fig_tmp2.add_trace(
    #         go.Scatter(
    #             x=all_inone_select.loc[
    #                 all_inone_select["b_cat"] == cat_b, "Q_norm"
    #             ],
    #             y=all_inone_select.loc[all_inone_select["b_cat"] == cat_b, y_out],
    #             mode="markers",
    #             marker=dict(color=float(cat_b)),
    #             showlegend=False,
    #         )
    #     )
    # fig = sp.make_subplots()
    # for trace in fig_tmp1["data"]:
    #     fig.add_trace(trace)
    # for trace in fig_tmp2["data"]:
    #     fig.add_trace(trace)

    fig = px.scatter(
        data_frame=all_inone_select,
        x="Q_norm",
        y=y_out,
        color="b_cat",
        symbol="round_m_tar",
        hover_name="M_tar",
        width=500,
    )
    # hide the colorbar

    for trace in fig.data:
        trace.marker.showscale = False

fig.add_trace(
    go.Scatter(
        x=[Q_norm],  # Replace with the x-coordinate of your point
        y=[y_plot],  # Replace with the y-coordinate of your point
        mode="markers",
        marker=dict(
            symbol="star",  # This sets the marker as a star
            size=15,  # This sets the marker size
            color="tomato",  # This sets the marker color
            line=dict(
                color="Black",  # This sets the outline color
                width=2,  # This sets the outline width
            ),
        ),
        name="Prediction",  # This sets the trace name
    )
)
fig.update_layout(coloraxis=dict(colorscale="plotly3"))

st.plotly_chart(fig, theme="streamlit")

# elif page == "Inverse Prediction":
#     st.info(
#         "Predict the result of a collision given: Mass of target planet ($M_{\oplus}$), impact velocity (km/s), impact parameter ($sin(\\theta)$)."
#     )
#     st.info("Current model only predict same-sized collision: $M_{tar}$ = $M_{imp}$")
#     target_mass = st.text_input("Enter target planet mass", "1.0")
#     impact_velocity = st.text_input("Enter impact velocity", "20.0")
#     b_data_widget = st.radio(
#         label="Impact parameter", options=[0.0, 0.2, 0.3, 0.4, 0.5]
#     )
# else:
#     st.write("visualization tab")
# with st.sidebar:
#     st.write("planet bar")
#     planet_mass = st.text_input("Enter planet mass", "1.0")
#     planet_zfe = st.text_input("Enter planet core fraction", "0.33")

#     column_names = [
#         "HDI index",
#         "GDP per capita",
#         "Life expectancy",
#         "CO2 per capita",
#         "Services",
#     ]
#     x_data_widget = st.radio(label="X-axis data", options=column_names)
#     y_data_widget = st.radio(label="Y-axis data", options=column_names)


# tab1, tab2 = st.tabs(["Impact Prediction", "Inverse Prediction"])

# with tab1:
#     demo_df = pd.read_csv("demo_dataset.csv")

#     st.dataframe(demo_df)

# with tab2:
#     st.write("visualization tab")

#     animate_vis = st.checkbox(label="Animate")

#     year_widget = st.slider(
#         label="Year to chart", min_value=1998, max_value=2018, disabled=animate_vis
#     )
#     log_or_x = st.checkbox(label="log x scale", value=False)
#     log_or_y = st.checkbox(label="log y scale", value=False)

#     if not animate_vis:
#         chart = px.scatter(
#             data_frame=demo_df[demo_df["Year"] == year_widget],
#             x=x_data_widget,
#             y=y_data_widget,
#             color="Continent",
#             size="CO2 per capita",
#             hover_name="Country",
#             log_y=log_or_y,
#         )
#     else:
#         chart = px.scatter(
#             data_frame=demo_df,
#             x=x_data_widget,
#             y=y_data_widget,
#             log_x=log_or_x,
#             log_y=log_or_y,
#             color="Continent",
#             size="CO2 per capita",
#             hover_name="Country",
#             animation_frame="Year",
#             animation_group="Country",
#         )

#     st.plotly_chart(fig, theme="streamlit")
