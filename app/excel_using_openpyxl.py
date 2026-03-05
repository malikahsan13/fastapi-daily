from fastapi import FastAPI, HTTPException
from openpyxl import Workbook
from fastapi.responses import StreamingResponse
from io import BytesIO

app = FastAPI()


@app.get("/create-spreadhseet/")
async def create_spreadsheet():

    wb = Workbook()
    ws = wb.active

    ws.append(["Name", "Age"])
    ws.append(["Alice", 32])
    ws.append(["Bob", 45])
    ws.append(["Charlie", 40])

    # save the workbook to a BytesIO object
    excel_io = BytesIO()
    wb.save(excel_io)
    excel_io.seek(0)

    # Return the excel file as a streaming response
    return StreamingResponse(BytesIO(excel_io.getvalue()), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={
        'Content-Disposition': 'attachment; filename="example.xlsx"'})
