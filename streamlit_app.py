# Import python packages.
import streamlit as st

from snowflake.snowpark.functions import col

# Write directly to the app.
st.title(" :cup_with_straw: Customize Your Smoothie! :cup_with_straw: ")
st.write(
  """Choose the fruits you want in your custom smoothie!
  """
)



name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

cnx = st.connection("snowflake")
session = cnx.session()
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(data=my_dataframe, use_container_width=True)
rows = my_dataframe.collect()
fruit_list = [row["FRUIT_NAME"] for row in rows]

ingredients_list = st.multiselect(
    "Choose up to 5 ingredients:",
    fruit_list,
    max_selections=5
)
if ingredients_list:
    
    
    ingredients_string =''

    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + '  ';
    #st.write(ingredients_string)

    my_insert_stmt = f"""
INSERT INTO smoothies.public.orders (ingredients, name_on_order)
VALUES ('{ingredients_string}', '{name_on_order}')
"""
    #st.write(my_insert_stmt)
    #st.stop()
    
    time_to_insert = st.button("Submit Order")
    if time_to_insert:
       session.sql(my_insert_stmt).collect()
       st.success('Your Smoothie is ordered!', icon="✅")

import requests
import streamlit as st
import pandas as pd

if ingredients_list:
    for fruit_chosen in ingredients_list:

        st.subheader(f"{fruit_chosen} Nutrition Information")

        try:
            # 🔥 Use fruit_chosen in API
            response = requests.get(f"https://my.smoothiefroot.com/api/fruit/{fruit_chosen}")
            data = response.json()

            # ✅ Convert nutrition into rows (like your UI)
            df = pd.DataFrame(data["nutrition"].items(), columns=["nutrition", "value"])

            # Add other columns
            df["family"] = data["family"]
            df["genus"] = data["genus"]
            df["id"] = data["id"]
            df["name"] = data["name"]
            df["order"] = data["order"]

            st.dataframe(df, use_container_width=True)

        except:
            # ❗ If fruit not in API (like Ximenia)
            st.warning(f"Sorry, {fruit_chosen} is not in our database.")
