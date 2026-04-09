import marimo

__generated_with = "0.23.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    df = pd.DataFrame({"A": [1, 2, 3], "B": ["a", "b", "c"]})
    editor = mo.ui.data_editor(data=df, label="Edit Data")
    editor
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
