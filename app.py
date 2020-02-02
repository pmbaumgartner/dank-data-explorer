import streamlit as st
from pathlib import Path
from utils import (
    load_data,
    strain_counts,
    scatter,
    line,
    img_to_bytes,
    read_markdown_file,
    colnames,
    category_large,
)
from pprint import pformat

header_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
    img_to_bytes("header.png")
)
st.markdown(
    header_html, unsafe_allow_html=True,
)

intro_markdown = desc_markdown = Path("intro.md").read_text()
st.markdown(intro_markdown, unsafe_allow_html=True)


data = load_data()
st.sidebar.markdown("## Configuration")
st.sidebar.markdown("① ** Strain Type Selection **")
strain_options = ["Indica", "Sativa", "Hybrid"]
strain_value = st.sidebar.selectbox(label="Strain Selection", options=strain_options)
strain_category_data = data.query("strain_category == @strain_value")
st.sidebar.markdown("② ** Strain Selection **")
strains, strain_formats = strain_counts(strain_category_data)
strain_value = st.sidebar.selectbox(
    label="Strain (Test Count)", options=strains, format_func=strain_formats.get
)
strain_data = strain_category_data.query("test_strain == @strain_value")

st.sidebar.markdown("---")
st.sidebar.markdown("ℹ️ ** Details **")
desc_check = st.sidebar.checkbox("📃 Dataset Description")


desc_markdown = read_markdown_file("data_description.md")
dict_check = st.sidebar.checkbox("📕 Data Dictionary")
dict_markdown = read_markdown_file("data_dictionary.md")

if desc_check:
    st.sidebar.markdown(desc_markdown, unsafe_allow_html=True)
if dict_check:
    st.sidebar.markdown(dict_markdown, unsafe_allow_html=True)
    st.sidebar.code(pformat(colnames, indent=2))


st.markdown("---")
st.markdown("## Strain Testing Data")
st.altair_chart(scatter(strain_data), width=-1)

st.altair_chart(line(strain_data), width=-1)

most_recent_suppliers = list(strain_data["org_name"].value_counts().head(8).index)
cmap = dict(zip(most_recent_suppliers, category_large))


def colormap(supplier):
    c = cmap.get(supplier)
    if c:
        h = c.lstrip("#")
        r, g, b = tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))
        rgba = f"rgba({r}, {g}, {b}, 0.5)"
    return f"background-color: {rgba};" if c else "background-color: #fff"


top5_test = (
    strain_data.sort_values("thc_max", ascending=False)[
        ["org_name", "date_test", "thc_max"]
    ]
    .head(10)
    .assign(thc_max=lambda d: d["thc_max"].apply("{0:.1f}".format))
)

styler = top5_test.style.applymap(colormap, subset=["org_name"])
st.markdown("### Top 10 Highest THC Measurements")
st.table(styler)
