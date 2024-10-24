
from shiny import ui, App, render

# Import Modules
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

# Impot data set
from palmerpenguins import load_penguins

# Define ui
app_ui = ui.page_fluid(
    # Create Title
    ui.panel_title("PyShiny App with Plot"),
    # Create a sidebar with slider input
    ui.input_slider("selected_number_of_bins", "Number of Bins", 0, 100, 20),
    ui.input_select(
        "species", "Which species is your favorite?", ["Adelie", "Gentoo", "Chinstrap"]
    ),
    ui.output_plot("draw_histogram"),
    ui.output_plot("penguin_plot"),
)


# Server Logic
def server(input, output, session):

    # Render a plot with random data
    @output
    @render.plot(alt="A histogram showing random data distribution")
    def draw_histogram():
        count_of_points: int = 437
        np.random.seed(5000)
        random_data_array = 100 + 15 * np.random.randn(count_of_points)
        plt.hist(random_data_array, input.selected_number_of_bins(), density=True)
        plt.xlabel("Number of Bins")
        plt.ylabel("Frequency")

    # Penguin Plot
    @output
    @render.plot(alt=" Palmer Penguin Data")
    def penguin_plot():
        penguins = load_penguins()
        penguins = penguins[penguins["species"] == input.species()]
        g = sns.lmplot(
            x="flipper_length_mm",
            y="body_mass_g",
            hue="species",
            height=7,
            data=penguins,
            palette=["#FF8C00", "#159090", "#A034F0"],
        )
        g.set_xlabels("Flipper Length")
        g.set_ylabels("Body Mass")
        return g


app = App(app_ui, server, debug=True)
