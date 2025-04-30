import streamlit as st
from streamlit_back_camera_input import back_camera_input
from models.food_item import to_dataframe
from services.image_reader_service import analyze_image

st.set_page_config(page_title="Shelf Life App")

picture = back_camera_input()

if picture:
  with st.spinner("Analyzing receipt...", show_time=True):
    food_items = analyze_image(picture)

    if food_items:
      df = to_dataframe(food_items)
      st.table(df)
    else:
      st.error("No food items found in the receipt.")