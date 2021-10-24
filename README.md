
# **Yatube_api**  
  
## **Project description:**  

Implementation of the REST API for the yatube project (Social network for publishing personal diaries).

What has been implemented?

 1. Authentication by token. JWT + Djoser.
 2. Displaying a list of posts, viewing individual posts. Full or partial editing for authenticated users.
 3. Create and edit comments to posts for authenticated users.
 4. Unauthenticated users have read-only access to the API. The exception is the `/ follow /` endpoint: only authenticated users are allowed access to it.
 5. Authenticated users are allowed to change and delete only their content; otherwise, read-only access.
  
## How to start a project:    
Clone the repository and go to it on the command line:
  
```
https://github.com/skarabey147/api_final_yatube.git
```
  
```
cd api_final_yatube
```
  
Create and activate a virtual environment:
  
```
python3 -m venv env
```

```
source env / scripts / activate
```
Update pip package manager
```
python3 -m pip install --upgrade pip
```
  
Install dependencies from requirements.txt file:
  
```
pip install -r requirements.txt
```
  
Run migrations:
  
```
python3 manage.py migrate
```
  
Run the project:
  
```
python3 manage.py runserver
```
## Examples of API requests:  
An example of a POST request with a user token: create a new post.  
_POST .../api/v1/posts/_  
```JSON  
{  
	"text": "Post text", 
	"group": 1
}   
```  
Response:  
```JSON  
{  
"id": 14, 
	"text": "Post text", 
	"author": "anton", 
	"image": null, 
	"group": 1, 
	"pub_date": "2021-06-01T08:47:11.084589Z"
}
```  
An example of a POST request with a user token: send a new comment to a post with `id = 14`.  
_POST .../api/v1/posts/14/comments/_  
  
```JSON  
{
	"text": "Comment text"
}  
```  
Response:  
  
```JSON  
{  
	"id": 4, 
	"author": "anton", 
	"post": 14, 
	"text": "Comment text", 
	"created": "2021-06-01T10:14:51.388932Z"
}
```  
An example of a GET request with a user token: getting information about a group.  
GET  _.../api/v1/groups/1/_  
  
Response:  
```JSON  
{  
    "id": 1, 
	"title": "Group title", 
	"slug": "group-1", 
	"description": "Group description"
} 
```