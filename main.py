import gradio as gr

gr.Interface.load("models/yangy50/garbage-classification").launch()
# if ml_scanner.py doesn't work, execute this, that usually fixes it after a few seconds


"""
To see the barcode mechanism in action, run barcode_scanner.py

To see the machine learning mechanism in action, run ml_scanner.py
"""