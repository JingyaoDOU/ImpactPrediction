import streamlit as st
import numpy as np
import pandas as pd
import colorcet as cc
import plotly.subplots as sp
from st_pages import Page, show_pages, add_page_title

# import colorcet as cc

# import seaborn as sns
from bokeh.models import (
    BasicTicker,
    ColorBar,
    ColumnDataSource,
    LogColorMapper,
    FixedTicker,
    NumeralTickFormatter,
    PrintfTickFormatter,
)
from bokeh.transform import transform
import matplotlib.colors as mcolors
from bokeh.models import HoverTool
from bokeh.plotting import figure, show
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import streamlit.components.v1 as components
import prediction

R_earth = 6.371e6  # m
M_earth = 5.97240e24  # kg
G = 6.67408e-11  # m^3 kg^-1 s^-2

# from st_metric import style_metric_cards
# st.set_page_config(layout="wide")

all_inone = pd.read_csv(
    "./data/all_in_one.csv", dtype={"round_m_tar": str, "b_cat": str}
)

hit_and_run = pd.read_csv("./data/hitandrun.csv")


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
impact_velocity = st.number_input("Enter impact velocity in km/s", value=25.0, step=2.0)
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
    if (ratio_mlr >= 1.0) & (b_data_widget == 0.0):
        # st.warning("Terminating...", icon="🚨")
        st.warning(
            'Current velocity is lower than the mutual escape velocity and the impact will be a "perfect merging".'
        )
        mlr = 2 * target_mass
        Zfe = 0.3
        ratio_mlr = 1.0
    elif (ratio_mlr >= 0.5) & (b_data_widget > 0.1):
        st.error("Terminating...", icon="🚨")
        st.error(
            "The oblique scaling law is only valid when mass raito is less than 0.5, below which impact transits from clean hit-and-run to erosive hit-and-run, where dense planets could form."
        )
        st.error("please increase the impact velocity.")

        col1.metric("Largest remnant mass ($M_{\oplus}$)", "Unknown")
        col2.metric("Core fraction", "Unknown")
        col3.metric("$M_{lr}$/$M_{total}$", "Unknown")
    else:
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


# Add a shared coloraxis
if b_data_widget == 0.0:
    p_m_z = st.radio(label="Visulization", options=["Mass ratio", "Core fraction"])
else:
    p_m_z = st.radio(
        label="Visulization",
        options=["Mass ratio", "Core fraction", "hit-and-run check"],
    )

if p_m_z == "Mass ratio":
    y_out = "ratio_lr"
    y_label = "Largest remnant mass ratio"
    y_plot = ratio_mlr
elif p_m_z == "Core fraction":
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
        color_discrete_sequence=px.colors.sequential.Turbo,
    )
    fig.update_layout(xaxis_title="Normalized impact energy")
    fig.update_layout(yaxis_title=y_label)
    fig.update_layout(autosize=False, width=650, height=600)

elif (b_data_widget > 0.1) & (p_m_z != "hit-and-run check"):
    all_inone_select = all_inone.loc[
        (all_inone["b"] > 0.1)
        & (all_inone["ratio_lr"] > 0.1)
        & (all_inone["round_m_tar"] != 1.58)
    ]

    fig = px.scatter(
        data_frame=all_inone_select,
        x="Q_norm",
        y=y_out,
        color="b_cat",
        # symbol="round_m_tar",
        hover_name="M_tar",
        width=500,
        labels={"b_cat": "Impact parameters", "round_m_tar": "M target"},
    )
    # hide the colorbar
    fig.update_traces(marker=dict(size=4))
    fig.update_layout(autosize=False, width=650, height=600)
    fig.update_layout(xaxis_title="Normalized impact energy")
    fig.update_layout(yaxis_title=y_label)

    for trace in fig.data:
        trace.marker.showscale = False

if p_m_z != "hit-and-run check":
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

if (b_data_widget > 0.1) & (p_m_z == "hit-and-run check"):
    target_R = target_mass**0.262
    vmutual = np.sqrt(2 * G * 2 * target_mass * M_earth / (2 * target_R * R_earth))

    cmap_ = cc.cm.CET_R2
    cmap = cc.b_rainbow_bgyr_35_85_c72

    norm = mcolors.PowerNorm(gamma=0.3, vmin=0.05, vmax=20)
    mapper = LogColorMapper(palette=cmap, low=0.06, high=19.95)

    source = ColumnDataSource(
        data=dict(
            x=hit_and_run["hnr_b"],
            y=hit_and_run["hnr_vvesc"],
            hnr_mtar=hit_and_run["hnr_mtar"],
            norm_hnr_mtar=norm(np.array(hit_and_run["hnr_mtar"])),
        )
    )
    TOOLTIPS = [
        ("b", "@x{(0.0)}"),
        ("Vimp/Vesc", "@y"),
        ("M_tar", "@hnr_mtar"),
    ]
    TOOLS = "hover,crosshair,pan,wheel_zoom,zoom_in,zoom_out,box_zoom,undo,redo,reset,tap,save,box_select,poly_select,lasso_select"

    p = figure(
        x_range=(0.0, 0.6),
        y_range=(1.3, 2.7),
        tools=[TOOLS],
        tooltips=TOOLTIPS,
        sizing_mode="stretch_width",
        max_width=800,
        height=600,
        x_axis_label="Impact parameter b",
        y_axis_label=r"V-imp / V-esc",
    )

    r = p.circle(
        x="x",
        y="y",
        size=10,
        # legend_label="Target mass",
        source=source,
        fill_color=transform("hnr_mtar", mapper)
        # fill_color={"field": "colors"},  # , "transform": exp_cmap},
    )

    color_bar = ColorBar(
        title="Target mass [M_Earth]",
        color_mapper=mapper,
        formatter=NumeralTickFormatter(format="0.00 a"),
        ticker=FixedTicker(
            ticks=[0.05, 0.1, 0.25, 0.5, 0.75, 1.0, 2.5, 5.0, 7.5, 10.0, 15.0, 20.0]
        )
        # ticker=BasicTicker(desired_num_ticks=len(cmap)),
        # formatter=PrintfTickFormatter(format="%d"),
    )

    p.add_layout(color_bar, "right")

    p.scatter(
        x=b_data_widget,
        y=impact_velocity / (vmutual * 1e-3),
        fill_color=cmap_(norm(target_mass)),
        size=20,
        legend_label="Input impact",
        marker="star",
        line_color="black",
        # tooltips="b:@b_data_widget{(0.0)}\nV-imp/V-esc:@impact_velocity{(0.0)}\nM_tar:@target_mass{(0.00)}",
    )

    b_kg = np.linspace(0, 0.55, 100)
    v_ratio_kg = 1.86 * (1 - b_kg) ** 2.5 + 1.04
    v_ratio_ga = 1.88 * (1 - b_kg) ** 2.5 + 1.13
    v_ratio_tom = np.sqrt(1 / b_kg)

    p.line(
        b_kg,
        v_ratio_kg,
        line_dash="dashed",
        legend_label=r"K&G 2010 et al. gamma=1",
        alpha=0.7,
        line_color="coral",
        line_width=2,
    )
    p.line(
        b_kg,
        v_ratio_ga,
        line_dash="dotted",
        legend_label=r"Gabriel et al. 2020",
        alpha=0.7,
        line_width=3,
        line_color="olivedrab",
    )

    p.line(
        b_kg,
        v_ratio_tom,
        line_dash="dotdash",
        legend_label=r"Denman et al. 2022",
        alpha=0.7,
        line_width=2,
        line_color="royalblue",
    )
    st.bokeh_chart(p, use_container_width=True)
