import marimo

__generated_with = "0.23.0"
app = marimo.App(width="medium")


@app.cell
def _():
    suppliments_headers = ["suppliments (ingredient name)"]
    return (suppliments_headers,)


@app.cell
def _(mo, suppliments_headers):
    import marimo as mo

    # fmt: off
    suppliment_data = {
        suppliments_headers[0]: [
            "Vitamin C",
            "Vitamin B12",
            "Omega-3"
        ]
    }
    # fmt: on
    suppliment_data_editor = mo.ui.data_editor(
        data=suppliment_data, label="Edit Data"
    ).form(bordered=True)
    mo.output.append(suppliment_data_editor)
    return mo, suppliment_data_editor


@app.cell
def _():
    import httpx

    url = "http://localhost:8000/"

    def get_suppliment_schedule(suppliments):
        try:
            response = httpx.post(url, json=suppliments)
            response.raise_for_status()
            suppliment_schedule = response.json()
            return suppliment_schedule
        except httpx.ConnectError:
            return "Could not reach server"
        except httpx.HTTPStatusError as e:
            return f"{e.response.status_code}: {e.response.text}"
        except httpx.TimeoutException:
            return "Request timed out"

    return (get_suppliment_schedule,)


@app.cell
def _(
    get_suppliment_schedule,
    mo,
    suppliment_data_editor,
    suppliments_headers,
):
    import asyncio
    import time

    edited_suppliment_data = suppliment_data_editor.value
    if edited_suppliment_data is None:
        mo.output.append(mo.md("## Nothing to send yet. Hit Submit."))
    else:
        suppliments = edited_suppliment_data[suppliments_headers[0]]

        with mo.status.spinner(title="Sending. Waiting for response...") as spinner:
            start_time = time.perf_counter()
            schedule_json_or_error = get_suppliment_schedule(
                suppliment_data_editor.value
            )
            end_time = time.perf_counter()
            response_time = round((end_time - start_time) * 1000)

        mo.output.replace(mo.md(f"Response received in {response_time}ms"))
        mo.output.append(schedule_json_or_error)

    return


if __name__ == "__main__":
    app.run()
