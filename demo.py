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
    from sample_data import ingredients
    from dataclasses import dataclass

    @dataclass
    class DefaultInputs:
        entire_sample_database = list(ingredients.keys())
        default_test_input = [
            "Calcium",
            "Iron",
            "Zinc",
            "Magnesium",
            "Copper",
            "Manganese",
            "Vitamin C",
            "NAC",
            "Green Tea Extract",
        ]

    # fmt: off
    supplement_data = {
        suppliments_headers[0]: DefaultInputs.default_test_input
    }
    # fmt: on
    suppliment_data_editor = mo.ui.data_editor(
        data=supplement_data, label="Edit Data"
    ).form(bordered=True)
    mo.output.append(suppliment_data_editor)
    return mo, suppliment_data_editor


@app.cell
def _():
    import httpx

    url = "http://localhost:8000/"

    def fetch_suppliment_schedule_from_api(suppliments):
        try:
            response = httpx.post(url, json=suppliments)
            response.raise_for_status()
            suppliment_schedule = response.json()
            return {"code": 200, "json": suppliment_schedule}
        except httpx.ConnectError:
            return {"code": None, "detail": "Could not reach server"}
        except httpx.HTTPStatusError as e:
            return {"code": e.response.status_code, "detail": e.response.text}
        except httpx.TimeoutException:
            return {"code": None, "detail": "Request timed out"}

    return (fetch_suppliment_schedule_from_api,)


@app.cell
def _(mo, suppliment_data_editor, suppliments_headers):
    raw_suppliment_data = suppliment_data_editor.value
    if raw_suppliment_data is None:
        shaped_suppliment_data = None
    else:
        shaped_suppliment_data = [
            {"name": suppliment_name}
            for suppliment_name in raw_suppliment_data[suppliments_headers[0]]
        ]
    return shaped_suppliment_data


@app.cell
def _(fetch_suppliment_schedule_from_api, mo, shaped_suppliment_data):
    import asyncio
    import time

    if shaped_suppliment_data is None:
        mo.output.append(mo.md("## Nothing to send yet. Hit Submit."))
        schedule_json_or_none = None
    else:
        with mo.status.spinner(title="Sending. Waiting for response...") as spinner:
            start_time = time.perf_counter()
            fetch_result = fetch_suppliment_schedule_from_api(shaped_suppliment_data)
            end_time = time.perf_counter()
            response_time = round((end_time - start_time) * 1000)

        mo.output.append(mo.md(f"Response received in {response_time}ms"))
        if fetch_result["code"] == 200:
            schedule_json_or_none = fetch_result["json"]
        else:
            err_to_display = fetch_result
            schedule_json_or_none = None
            mo.output.append(err_to_display)

    return schedule_json_or_none


@app.cell
def _(mo, schedule_json_or_none):
    if schedule_json_or_none is not None:
        table_ready_data = []
        for slot in schedule_json_or_none["schedule"].items():
            slot_name, suppliments = slot
            row = {"Time Slot": slot_name} | {
                f"Suppliment {i + 1}": suppliment["name"]
                for i, suppliment in enumerate(suppliments)
            }
            table_ready_data.append(row)

        header = mo.md("## Suppliment Schedule")
        total_conflicts = (
            f"{schedule_json_or_none['DEV_total_conflict_count']} schedule conflicts"
        )
        table = mo.ui.table(
            data=table_ready_data, selection=None, label=total_conflicts
        )
        layout = mo.vstack([header, table])
        mo.output.append(mo.md("## Suppliment Schedule"))
        mo.output.append(table)

    return


if __name__ == "__main__":
    app.run()
