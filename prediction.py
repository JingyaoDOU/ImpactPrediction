import warnings
import pandas as pd
import numpy as np

R_earth = 6.371e6  # m
M_earth = 5.97240e24  # kg
G = 6.67408e-11  # m^3 kg^-1 s^-2


def head_on_predict(m_tar, v_i, c_head_on_star=2.92552):
    """
    m_tar in Earth mass
    v_i in km/s
    """

    m_total = 2 * m_tar
    v_i *= 1e3  # change back to m/s
    R_c1 = np.power(3 * m_total * M_earth / (1000 * np.pi * 4), 1 / 3)  # in m
    Q_RD_star = c_head_on_star * (4 * np.pi / 5) * 1000 * G * R_c1**2

    Q_norm = v_i**2 / (8 * Q_RD_star)

    if Q_norm < 0.625:
        ratio_mlr = 1 - 0.86 * Q_norm**2.77
        Zfe = 0.3 + 0.25 * Q_norm**2.6
    else:
        if m_tar < 1.0:
            if m_tar < 0.05:
                warnings.warn(
                    "The data has not covered target mass this small, the model might be fail in this regiem."
                )
            ratio_mlr = 0.5 - 0.5 * (Q_norm - 1)
            Zfe = 0.4 + 0.11 * (Q_norm - 0.625)
        else:
            if m_tar > 20:
                warnings.warn(
                    "The data has not covered target mass this large, the model might be fail in this regiem."
                )
            ratio_mlr = 0.75 - 0.86 * (Q_norm - 0.625) ** 1.24
            Zfe = 0.37 + 0.66 * (Q_norm - 0.625) ** 2

    return Q_norm, ratio_mlr * m_total, ratio_mlr, Zfe


def ob_predict(m_tar, v_i, b):
    """
    m_tar: in Earth mass
    v_i: in km/s
    b: impact parameter
    """
    c_star_ob_list = np.array([2.29, 1.67, 1.265, 1.10])  # b=0.2, 0.3, 0.4, 0.5
    ob_param = {
        "b": np.array([0.2, 0.3, 0.4, 0.5]),
        "am": np.array([1.78, 0.73, 0.64, 0.56]),
        "bm": np.array([1.55, 0.50, 0.25, 0.11]),
        "afe": np.array([0.41, 0.33, 0.29, 0.30]),
        "bfe": np.array([0.34, 0.18, 0.09, 0.04]),
        "c_star_ob": c_star_ob_list,
    }
    ob_param = pd.DataFrame(ob_param)

    c_star_ob = ob_param.loc[ob_param["b"] == b, "c_star_ob"]
    am = ob_param.loc[ob_param["b"] == b, "am"]
    bm = ob_param.loc[ob_param["b"] == b, "bm"]
    afe = ob_param.loc[ob_param["b"] == b, "afe"]
    bfe = ob_param.loc[ob_param["b"] == b, "bfe"]

    m_total = 2 * m_tar
    v_i *= 1e3  # change back to m/s
    R_c1 = np.power(3 * m_total * M_earth / (1000 * np.pi * 4), 1 / 3)  # in m
    Q_RD_star = c_star_ob * (4 * np.pi / 5) * 1000 * G * R_c1**2

    Q_norm = v_i**2 / (8 * Q_RD_star)

    ratio_mlr = am * np.exp(-bm * Q_norm)
    Zfe = afe + bfe * (Q_norm - 1)

    return float(Q_norm), float(ratio_mlr * m_total), float(ratio_mlr), float(Zfe)


def head_on_predict_inverse(mlr, zfe, c_head_on_star=2.92552):
    """
    mlr: mass of the object in Earth mass
    zfe: core fraction of the object e.g 0.6, 0.7
    """
    m_tar = mlr / (2 * (0.75 - 0.86 * ((zfe - 0.37) / 0.66) ** 0.62))
    R_c1 = np.power(3 * 2 * m_tar * M_earth / (1000 * np.pi * 4), 1 / 3)  # in m
    Q_star = c_head_on_star * (4 * np.pi / 5) * 1000 * G * R_c1**2
    vi = np.sqrt(8 * Q_star * (0.625 + np.sqrt((zfe - 0.37) / 0.66)))

    return m_tar, vi / 1e3


def ob_predict_inverse(mlr, zfe, b):
    """
    m_tar: in Earth mass
    v_i: in km/s
    b: impact parameter
    """
    c_star_ob_list = np.array([2.29, 1.67, 1.265, 1.10])  # b=0.2, 0.3, 0.4, 0.5
    ob_param = {
        "b": np.array([0.2, 0.3, 0.4, 0.5]),
        "am": np.array([1.78, 0.73, 0.64, 0.56]),
        "bm": np.array([1.55, 0.50, 0.25, 0.11]),
        "afe": np.array([0.41, 0.33, 0.29, 0.30]),
        "bfe": np.array([0.34, 0.18, 0.09, 0.04]),
        "c_star_ob": c_star_ob_list,
    }
    ob_param = pd.DataFrame(ob_param)

    c_star_ob = ob_param.loc[ob_param["b"] == b, "c_star_ob"]
    am = ob_param.loc[ob_param["b"] == b, "am"]
    bm = ob_param.loc[ob_param["b"] == b, "bm"]
    afe = ob_param.loc[ob_param["b"] == b, "afe"]
    bfe = ob_param.loc[ob_param["b"] == b, "bfe"]

    m_tar = mlr / (2 * am * np.exp(-bm * ((zfe - afe) / bfe + 1)))
    R_c1 = np.power(3 * 2 * m_tar * M_earth / (1000 * np.pi * 4), 1 / 3)  # in m
    Q_star = c_star_ob * (4 * np.pi / 5) * 1000 * G * R_c1**2

    vi = np.sqrt(8 * Q_star * ((zfe - afe) / bfe + 1))

    return float(m_tar), float(vi / 1e3)
