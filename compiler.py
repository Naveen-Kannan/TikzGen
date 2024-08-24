from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.path.exists("uploaded_files"):
        os.mkdir("uploaded_files")
    if not os.path.exists("processed_files"):
        os.mkdir("processed_files")
    yield
    # cleanup

app = FastAPI(lifespan=lifespan)

@app.post("/uploadfile/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()

    #save the file to uploads directory
    with open(f"uploaded_files/{file.filename}", "wb") as f:
        f.write(contents)

    # if file not of .tex return error
    if not file.filename.endswith(".tex"):
        raise HTTPException(detail="File must end with .tex", status_code=400)
        
    # run pdflatex on the uploaded file with subprocess or os.system
    os.system(f"pdflatex -output-directory=processed_files uploaded_files/{file.filename}")
    
    # return successfully processed message
    return JSONResponse(content={"message": "File processed successfully"}, status_code=200)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)