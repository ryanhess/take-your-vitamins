import marimo

__generated_with = "0.23.0"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo

    return


@app.cell(hide_code=True)
def _():
    import httpx
    response = httpx.get("https://api.ods.od.nih.gov/dsld/v9/label/260891")
    label = response.json()
    label
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
