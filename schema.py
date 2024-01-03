import json
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class Post:
    article_id      : str
    title           : str 
    description     : str
    link            : str
    content         : str
    pubDate         : str
    image_url       : str

# Serialization: Data class instance to JSON string
def serialize_post(post:Post)->dict:
    return asdict(post)

# Deserialization: JSON string to data class instance
def deserialize_post(json_string :dict)->Post:
    post = Post(**json_string)
    return post