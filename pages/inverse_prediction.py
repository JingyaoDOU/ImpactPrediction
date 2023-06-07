import streamlit as st
import numpy as np
import pandas as pd
import prediction

st.info(
    "Given a planet mass ($M_{\oplus}$) and core fraction, predicting the potential target mass and impact velocity."
)
st.info(
    "Inverse prediction for head-on collision is only using scaling law when $M_{tar}$ > 1.0 $M_{\oplus}$ as lower mass head-on can achieve up most 50% core fraction."
)
st.warning(
    "Current model only predict same-sized collision: $M_{tar}$ = $M_{imp}$  or  $\gamma$ = 1"
)

rem_mass = st.number_input(
    "Enter planet mass in $M_{\oplus}$",
    min_value=0.05,
    max_value=20.0,
    value=0.5,
    step=0.1,
)
core_fraction = st.number_input(
    "Enter core fraction of the planet", value=0.6, step=0.05
)

b_data_widget = st.radio(
    label="Impact parameter", options=[0.0, 0.2, 0.3, 0.4, 0.5], horizontal=True
)

if b_data_widget == 0.0:
    m_tar, v_i = prediction.head_on_predict_inverse(rem_mass, core_fraction)
else:
    m_tar, v_i = prediction.ob_predict_inverse(rem_mass, core_fraction, b_data_widget)

col1, col2, col3 = st.columns(3)

if m_tar > 20:
    st.warning(
        "The predict target mass is larger than 20 $M_{\oplus}$, the model might be fail in this regiem."
    )

col1.metric("Target planet mass ($M_{\oplus}$)", "%.2f" % m_tar)
col2.metric("Impact velocity (km/s)", "%.1f " % (v_i))
col3.metric("$M_{lr}$/$M_{total}$", "%.1f %%" % (100 * rem_mass / (2 * m_tar)))
