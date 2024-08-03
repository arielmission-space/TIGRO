from shiny import App, ui, render
import matplotlib.pyplot as plt
import numpy as np
import mpld3

# Define the UI
app_ui = ui.page_fluid(
    ui.panel_title("Interactive Matplotlib Plot with mpld3"),
    ui.layout_sidebar(
        ui.sidebar(
            ui.input_slider("num_points", "Number of points", min=10, max=100, value=50)
        ),
        ui.output_ui("scatter_plot"),
    ),
)


# Define the server logic
def server(input, output, session):
    @output
    @render.ui
    def scatter_plot():
        num_points = input.num_points()
        x = np.random.rand(num_points)
        y = np.random.rand(num_points)

        fig, ax = plt.subplots()
        scatter = ax.scatter(x, y, c="blue", s=50, alpha=0.7)
        ax.set_title("Interactive Scatter Plot")
        ax.set_xlabel("X-axis")
        ax.set_ylabel("Y-axis")

        # Use mpld3 to create an interactive plot
        mpld3.plugins.connect(fig, mpld3.plugins.MousePosition())
        html = mpld3.fig_to_html(fig)
        plt.close(fig)

        return ui.HTML(html)


# Create the Shiny app
app = App(app_ui, server)

if __name__ == "__main__":
    app.run()
