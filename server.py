#dependencies
from fastapi import FastAPI,Request,UploadFile, File,BackgroundTasks
from fastapi.templating import Jinja2Templates
import shutil
import os
import ocr
import uuid
#code...
app = FastAPI()

templates = Jinja2Templates(directory = 'templates')

@app.get("/") # making a get call
def home(request: Request): # var is request of type Request from fastapi
    return templates.TemplateResponse("index.html", {'request':request})

@app.post("/extract_text")
async def perform_ocr(image: UploadFile = File(...)):
    temp_file = _save_file_to_disk(image,path = "temp", save_as = "temp")
    text = await ocr.read_image(temp_file)
    return {"filename": image.filename, "text":text}
@app.post('/bulk_extract_text')
async def bulk_perform_ocr(request:Request, bg_tasks: BackgroundTasks):
    images = await request.form()

    # save the images
    folder_name = str(uuid.uuid4())
    os.mkdir(folder_name)

    for image in images.values():
        temp_file = _save_file_to_disk(image, path=folder_name, save_as=image.filename)
    bg_tasks.add_task(ocr.read_images_from_dir, folder_name, write_to_file=True)
    return{'task_id': folder_name, 'num_files': len(images)}

@app.get('/bulk_output/{task_id}')
async def bulk_output(task_id):
    text_map = {}
    for file_ in os.listdir(task_id):
        if(file_.endswith('txt')):
            text_map[file_] = open(os.path.join(task_id,file_)).read()
    return{'task_id': task_id,'output': text_map}


def _save_file_to_disk(uploaded_file, path = ".",save_as="default"):
    extension = os.path.splitext(uploaded_file.filename)[-1]
    temp_file = os.path.join(path,save_as+extension)
    with open(temp_file,"wb") as buffer: #opens empty file with same name i.e. default
        shutil.copyfileobj(uploaded_file.file, buffer) # copies the file obj to new file
    return temp_file #returns the name of the file
