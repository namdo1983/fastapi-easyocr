from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pathlib import Path
import uvicorn, os
import easyocr
import cv2
import glob


from fastapi import FastAPI, File, UploadFile


CURDIR = Path(__file__).parent


reader = easyocr.Reader(
    ["vi", "en"]
)  # this needs to run only once to load the model into memory
app = FastAPI()


@app.post("/upload")
def upload(file: UploadFile = File(...)):
    upload_path = os.path.join(
        CURDIR,
        f"upload/{file.filename}",
    )
    try:
        with open(upload_path, "wb") as f:
            while contents := file.file.read(1024 * 1024):
                f.write(contents)
    except Exception:
        return {"message": "There was an error uploading the file"}
    finally:
        file.file.close()

    return {"message": f"Successfully uploaded {file.filename}"}


@app.get("/get_image")
async def get_image():
    # files = glob.glob(f"{upload_path}/*")
    # for f in files:
    #     os.remove(f)
    upload_path = "upload/cap1.jpg"
    image_path = Path(upload_path)
    if not image_path.is_file():
        return HTTPException(status_code=404, detail="Image not found on the server")

    check_img = os.path.join(CURDIR, upload_path)
    img = cv2.imread(check_img, cv2.IMREAD_GRAYSCALE)
    res = reader.readtext(img)
    print(res)
    return {"Threshold": round(res[0][2], 2), "Result": res[0][1]}


if __name__ == "__main__":
    uvicorn.run("app:app", host="127.0.0.1")
