import streamlit as st
from utils import (
    load_data,
    strain_counts,
    scatter,
    line,
    img_to_bytes,
    read_markdown_file,
    colnames,
    get_top_test_table,
)
from pprint import pformat

header_html = "<img src='data:image/png;base64,{}' class='img-fluid'>".format(
    img_to_bytes("header.png")
)
st.markdown(
    header_html, unsafe_allow_html=True,
)

intro_markdown = read_markdown_file("intro.md")
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
st.altair_chart(scatter(strain_data))

st.altair_chart(line(strain_data))


st.markdown("### Top 10 Highest THC Measurements")
styled_test_table = get_top_test_table(strain_data)
st.table(styled_test_table)
