import marimo

__generated_with = "0.23.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    # fmt: off
    suppliment_data = {
        "suppliments (ingredient name)": [
            "Vitamin C",
            "Vitamin B12",
            "Omega-3"
        ]
    }
    # fmt: on
    suppliment_data_editor = mo.ui.data_editor(data=suppliment_data, label="Edit Data").form(bordered=True)
    suppliment_data_editor
    return (mo,)


@app.cell
async def _(mo):
    import asyncio

    with mo.status.spinner(title="Sending...") as spinner:
        await asyncio.sleep(1)
        spinner.update("Waiting for response...")
        await asyncio.sleep(1)

    mo.output.replace(mo.md("### Response received in 100ms"))
    mo.output.append()
    return


if __name__ == "__main__":
    app.run()
