#
# Database access functions for the web forum.
#
import bleach
import psycopg2


## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    DB = psycopg2.connect("dbname=forum")
    posts = []
    cur = DB.cursor()
    cur.execute("select content, time from posts order by time desc;")
    results = cur.fetchall()
    for post in results:
        posts.append({'content': post[0], 'time': post[1]})
    cur.close()
    DB.close()
    return posts


## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    DB = psycopg2.connect("dbname=forum")
    cur = DB.cursor()
    cur.execute("insert into posts (content) values (%s);",
                (bleach.clean(content),))
    DB.commit()
    cur.close()
    DB.close()
