import marimo

__generated_with = "0.23.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    # fmt: off
    suppliment_data = {
        "suppliments (ingredient)": [
            "Vitamin C",
            "Vitamin B12",
            "Omega-3"
        ]
    }
    # fmt: on
    editor = mo.ui.data_editor(data=suppliment_data, label="Edit Data")
    editor
    return (editor,)


@app.cell
def _(editor):
    editor.value
    return


if __name__ == "__main__":
    app.run()
