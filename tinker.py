import marimo

__generated_with = "0.23.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import pandas as pd

    df = pd.DataFrame({"ingredient": ["Vitamin C", "Vitamin B12", "Omega-3"]})
    editor = mo.ui.data_editor(data=df, label="Edit Data")
    editor
    return (editor,)


@app.cell
def _(editor):
    data_frame = editor.value
    data_as_JSON = data_frame.to_json()
    data_as_JSON
    return


if __name__ == "__main__":
    app.run()
