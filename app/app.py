from fastapi import FastAPI,HTTPException
from app.schemas import PostCreate

app= FastAPI()

text_posts={
    1: {"title": "The Future of Remote Work", "content": "Remote work has transformed how we approach productivity and work-life balance. Companies are discovering that flexible arrangements often lead to increased employee satisfaction and better results. The key is finding the right balance between autonomy and collaboration."},
    2: {"title": "Sustainable Living Tips", "content": "Small changes in our daily routines can make a big environmental impact. Try switching to reusable water bottles, composting organic waste, and choosing public transportation when possible. Every action counts toward a greener future."},
    3: {"title": "Learning Python in 2024", "content": "Python continues to be one of the most versatile programming languages. Whether you're interested in web development, data science, or automation, Python offers excellent libraries and frameworks. Start with the basics and build projects to solidify your understanding."},
    4: {"title": "Coffee Culture Around the World", "content": "From Italian espresso to Ethiopian coffee ceremonies, each culture has its unique relationship with coffee. Exploring different brewing methods and bean origins can transform your daily coffee routine into a global adventure."},
    5: {"title": "The Art of Minimalism", "content": "Minimalism isn't just about owning fewer things; it's about focusing on what truly matters. By decluttering our physical and mental spaces, we create room for experiences and relationships that bring genuine joy and fulfillment."},
    6: {"title": "Urban Gardening for Beginners", "content": "You don't need a large yard to grow your own food. Container gardening, vertical gardens, and windowsill herbs are perfect for apartment living. Start with easy plants like basil, mint, or cherry tomatoes to build your confidence."},
    7: {"title": "Digital Photography Basics", "content": "Great photos aren't just about expensive equipment. Understanding composition, lighting, and timing can dramatically improve your photography. Practice the rule of thirds, experiment with natural light, and don't be afraid to take multiple shots."},
    8: {"title": "Healthy Meal Prep Strategies", "content": "Spending a few hours on Sunday preparing meals can save time and promote healthier eating throughout the week. Focus on versatile ingredients that can be mixed and matched, and don't forget to include plenty of vegetables and lean proteins."},
    9: {"title": "The Benefits of Reading Fiction", "content": "Reading fiction does more than entertain; it builds empathy, improves vocabulary, and enhances critical thinking skills. Regular reading can reduce stress and provide a healthy escape from daily pressures while expanding our understanding of different perspectives."},
    10: {"title": "Getting Started with Meditation", "content": "Meditation doesn't require hours of practice or special equipment. Even five minutes of focused breathing can help reduce anxiety and improve concentration. Start small, be consistent, and remember that wandering thoughts are normal and part of the process."}
}

@app.get("/posts")
def get_all_posts(limit:int=None):
    if limit:
        return list(text_posts.values())[:limit]
    return text_posts


@app.get("/posts/{id}")
def get_post(id: int):
    if id not in text_posts:
        raise HTTPException(status_code=404,detail="Post not found")
    return text_posts[id]



@app.post("/posts")
def create_post(post: PostCreate):
    new_post = {"title": post.title, "content": post.content}
    text_posts[max(text_posts.keys())+1]=new_post
    return new_post
