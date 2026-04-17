import marimo

__generated_with = "0.23.0"
app = marimo.App(width="medium")


@app.cell
def _():
    supplements_header = "supplements (ingredient name)"
    return (supplements_header,)


@app.cell
def _(mo, supplements_header):
    import marimo as mo
    from sample_data import ingredients
    from dataclasses import dataclass

    @dataclass
    class DefaultInputs:
        blank = [""]
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
        entire_sample_database = list(ingredients.keys())

    # fmt: off
    supplement_data = {
        supplements_header: DefaultInputs.default_test_input
    }
    # fmt: on
    supplement_data_editor = mo.ui.data_editor(
        data=supplement_data, label="Edit Data"
    ).form(bordered=True)
    mo.output.append(supplement_data_editor)
    return mo, supplement_data_editor


@app.cell
def _():
    import httpx

    url = "http://localhost:8000/"

    def fetch_supplement_schedule_from_api(supplements):
        try:
            response = httpx.post(url, json=supplements)
            response.raise_for_status()
            supplement_schedule = response.json()
            return {"code": 200, "json": supplement_schedule}
        except httpx.ConnectError:
            return {"code": None, "detail": "Could not reach server"}
        except httpx.HTTPStatusError as e:
            return {"code": e.response.status_code, "detail": e.response.text}
        except httpx.TimeoutException:
            return {"code": None, "detail": "Request timed out"}

    return (fetch_supplement_schedule_from_api,)


@app.cell
def _(mo, supplement_data_editor, supplements_header):
    raw_supplement_data = supplement_data_editor.value
    if raw_supplement_data is None or raw_supplement_data[supplements_header] == [""]:
        shaped_supplement_data = None
    else:
        shaped_supplement_data = [
            {"name": supplement_name}
            for supplement_name in raw_supplement_data[supplements_header]
        ]
    return shaped_supplement_data


@app.cell
def _(fetch_supplement_schedule_from_api, mo, shaped_supplement_data):
    import time

    if shaped_supplement_data is None:
        mo.output.append(mo.md("## Nothing to send yet. Hit Submit."))
        schedule_json_or_none = None
    else:
        with mo.status.spinner(title="Sending. Waiting for response..."):
            start_time = time.perf_counter()
            fetch_result = fetch_supplement_schedule_from_api(shaped_supplement_data)
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
        print(schedule_json_or_none)
        for slot in schedule_json_or_none["schedule"].items():
            slot_name, supplements = slot
            row = {"Time Slot": slot_name} | {
                f"Supplement {i + 1}": supplement
                for i, supplement in enumerate(supplements)
            }
            table_ready_data.append(row)

        header = mo.md("## Supplement Schedule")
        total_conflicts = (
            f"{schedule_json_or_none['DEV_total_conflict_count']} schedule conflicts"
        )

        max_supplements = max(len(row) - 1 for row in table_ready_data)
        supplement_columns = [f"Supplement {i + 1}" for i in range(max_supplements)]

        format_mapping = {col: lambda val: val["name"] for col in supplement_columns}

        def hover_template(row_id, column_name, value):
            supplement_obj = value

            constraints = supplement_obj["constraints"]
            take_not_with = constraints["take_not_with"]

            tooltip_text = [
                f"Take {constraints['before_after_food']} food.",
                "Do not take with:",
            ] + ["- " + name for name in take_not_with]

            return "\n".join(tooltip_text)

        table = mo.ui.table(
            data=table_ready_data,
            format_mapping=format_mapping,
            hover_template=hover_template,
            label=total_conflicts,
        )

        supplements_not_in_db = schedule_json_or_none["supplements_not_found"]
        ui_of_not_in_db = mo.md(
            "### Supplements Not in Database:\n"
            + "\n".join(f"- {ingred}" for ingred in supplements_not_in_db)
        )

        layout_stack = [header, table]
        if supplements_not_in_db:
            layout_stack.append(ui_of_not_in_db)

        layout = mo.vstack(layout_stack)
        mo.output.append(layout)

    return


if __name__ == "__main__":
    app.run()
