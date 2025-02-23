from fastapi import FastAPI
import uvicorn
from pytube.download_helper import download_video

app = FastAPI()

@app.get("/")
async def read_root():
    return {"message": "Hello, World!"}

@app.get("/get_video")
async def get_video(video_url: str):
    try:
        save_path = "videos"
        yt = download_video(video_url)
        stream = yt.streams.get_highest_resolution()
        file_path = stream.download(output_path=video_url)
        print(f"Video downloaded successfully to: {file_path}")
        return {"success": True, "file_path": file_path}
    except Exception as e:
        print(f"Error downloading video: {str(e)}")
        return {"success": False, "error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
