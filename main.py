import gradio as gr

gr.Interface.load("models/yangy50/garbage-classification").launch()
# if the api doesn't work, execute the code snippet above, that usually fixes it after like a minute


# the actual machine learning part
# getting packaging info from a picture
"""import ml_api

ml_api.query("images/bottle.jpg")"""
