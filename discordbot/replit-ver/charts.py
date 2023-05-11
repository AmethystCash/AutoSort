import matplotlib.pyplot as plt
import io
from firebase import *


def return_plot_file(generate_chart):
    def wrapper(data):
        plt.clf()
        generate_chart(data)
        
        img_data = io.BytesIO()
        plt.savefig(img_data, format='png')
        img_data.seek(0)
        
        return img_data
        
    return wrapper


@return_plot_file
def generate_barchart(data):
    totals = get_totals(data)  # filters all data
    plt.bar(list(totals.keys()), list(totals.values()))


@return_plot_file
def generate_piechart(data):
    totals = get_totals(data)  # filters all data
    # you might want to filter data differently, that's why this appears in both funcs instead of the decorator
    plt.pie(list(totals.values()), labels=list(totals.keys()))



charts = {
    'Bar chart': {
        'emoji': '📊',
        'short_desc': 'Representing the amounts of each material',

        'long_desc': '',
        'image_gen': generate_barchart
    },
    'Pie chart': {
        'emoji': '🥧',
        'short_desc': 'Representing the percentages of each material',

        'long_desc': '',
        'image_gen': generate_piechart
    }
}