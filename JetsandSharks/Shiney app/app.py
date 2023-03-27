from shiny import App, render, ui
from jetandshark import equilibrium

app_ui = ui.page_fluid(
    ui.input_text("x", "Enter space separated list for all items you want to query on for the Jets and Sharks model",
                     placeholder="For example: Jets 20's sing."),
    ui.input_text("y", "Enter a key for which you would like the activation value",
                     placeholder="For example: burglar"),
    ui.output_text_verbatim("txt"),
)


def server(input, output, session):
    @output
    @render.text
    def txt():
        query = input.x().split()
        final_values = equilibrium(query)
        val = final_values[input.y()]
        key = input.y()
        return f'y: "{key, val}"'


app = App(app_ui, server, debug=True)
