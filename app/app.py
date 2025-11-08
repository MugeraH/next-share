from fastapi import FastAPI,HTTPException,File,UploadFile,Form,Depends
from app.schemas import PostCreate,PostResponse
from app.db import Post,create_db_and_tables,get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from contextlib import asynccontextmanager
from sqlalchemy import select
from app.images import imagekit
from imagekitio.models.UploadFileRequestOptions import UploadFileRequestOptions
import os
import shutil
import uuid
import tempfile

@asynccontextmanager
async def lifespan(app:FastAPI):
    await create_db_and_tables()
    yield

app= FastAPI(lifespan=lifespan)

@app.post("/upload")
async def upload_file(
    file:UploadFile=File(...),
    caption:str=Form(""),
    session:AsyncSession = Depends(get_async_session)

):
    temp_file_path=None
    try:
        with tempfile.NamedTemporaryFile(delete=False,suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_file_path=temp_file.name
            shutil.copyfileobj(file.file,temp_file)
        upload_result=imagekit.upload_file(
            file=open(temp_file_path,"rb"),
            file_name=file.filename,
            options=UploadFileRequestOptions(
                use_unique_file_name=True,
                tags=["backend-upload"]
            )
        )
        file_name=upload_result.file_name or upload_result.name or file.filename
     
        if upload_result.response_metadata.http_status_code == 200:
            post = Post(
                caption=caption,
                url=upload_result.url,
                file_type="video" if file.content_type.startswith("video/") else "image",
                file_name=file_name

            )
            session.add(post)
            await session.commit()
            await session.refresh(post)
            return post


    except Exception as e:
       raise HTTPException(status_code=500,detail=str(e))
    finally:
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)
        file.file.close()
        


   


@app.get("/feed")
async def get_feed(
    session:AsyncSession = Depends(get_async_session)
):
    result= await session.execute(select(Post).order_by(Post.created_at.desc()))
    posts = [row[0] for row in result.all()]

    posts_data = []
    for post in posts:
        posts_data.append({
            "id":post.id,
            "caption":post.caption,
            "url":post.url,
            "file_type":post.file_type,
            "file_name":post.file_name,
            "created_at":post.created_at
        })
    return {"posts":posts_data}






# text_posts={
#     1: {"title": "The Future of Remote Work", "content": "Remote work has transformed how we approach productivity and work-life balance. Companies are discovering that flexible arrangements often lead to increased employee satisfaction and better results. The key is finding the right balance between autonomy and collaboration."},
#     2: {"title": "Sustainable Living Tips", "content": "Small changes in our daily routines can make a big environmental impact. Try switching to reusable water bottles, composting organic waste, and choosing public transportation when possible. Every action counts toward a greener future."},
#     3: {"title": "Learning Python in 2024", "content": "Python continues to be one of the most versatile programming languages. Whether you're interested in web development, data science, or automation, Python offers excellent libraries and frameworks. Start with the basics and build projects to solidify your understanding."},
#     4: {"title": "Coffee Culture Around the World", "content": "From Italian espresso to Ethiopian coffee ceremonies, each culture has its unique relationship with coffee. Exploring different brewing methods and bean origins can transform your daily coffee routine into a global adventure."},
#     5: {"title": "The Art of Minimalism", "content": "Minimalism isn't just about owning fewer things; it's about focusing on what truly matters. By decluttering our physical and mental spaces, we create room for experiences and relationships that bring genuine joy and fulfillment."},
#     6: {"title": "Urban Gardening for Beginners", "content": "You don't need a large yard to grow your own food. Container gardening, vertical gardens, and windowsill herbs are perfect for apartment living. Start with easy plants like basil, mint, or cherry tomatoes to build your confidence."},
#     7: {"title": "Digital Photography Basics", "content": "Great photos aren't just about expensive equipment. Understanding composition, lighting, and timing can dramatically improve your photography. Practice the rule of thirds, experiment with natural light, and don't be afraid to take multiple shots."},
#     8: {"title": "Healthy Meal Prep Strategies", "content": "Spending a few hours on Sunday preparing meals can save time and promote healthier eating throughout the week. Focus on versatile ingredients that can be mixed and matched, and don't forget to include plenty of vegetables and lean proteins."},
#     9: {"title": "The Benefits of Reading Fiction", "content": "Reading fiction does more than entertain; it builds empathy, improves vocabulary, and enhances critical thinking skills. Regular reading can reduce stress and provide a healthy escape from daily pressures while expanding our understanding of different perspectives."},
#     10: {"title": "Getting Started with Meditation", "content": "Meditation doesn't require hours of practice or special equipment. Even five minutes of focused breathing can help reduce anxiety and improve concentration. Start small, be consistent, and remember that wandering thoughts are normal and part of the process."}
# }

# @app.get("/posts")
# def get_all_posts(limit:int=None)->list[PostResponse]:
#     posts_list = [PostResponse(**post) for post in text_posts.values()]
#     if limit:
#         return posts_list[:limit]
#     return posts_list


# @app.get("/posts/{id}")
# def get_post(id: int)->PostResponse:
#     if id not in text_posts:
#         raise HTTPException(status_code=404,detail="Post not found")
#     return PostResponse(**text_posts[id])
#     return text_posts[id]



# @app.post("/posts")
# def create_post(post: PostCreate)-> PostResponse:
#     new_post = {"title": post.title, "content": post.content}
#     text_posts[max(text_posts.keys())+1]=new_post
#     return new_post

# @app.put("/posts/{id}")
# def update_post(id: int, post: PostCreate):
#     if id not in text_posts:
#         raise HTTPException(status_code=404,detail="Post not found")
#     text_posts[id] = {"title": post.title, "content": post.content}
#     return text_posts[id]


# @app.delete("/posts/{id}")
# def delete_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404,detail="Post not found")
    del text_posts[id]
    return {"message": "Post deleted successfully"}