__author__ = 'salman wahed'

import webapp2
import jinja2
import os
from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname("__file__"), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *args, **kw):
        self.response.out.write(*args, **kw)

    def render_str(self, template, **kw):
        t = jinja_env.get_template(template)
        return t.render(**kw)

    def render(self, template, **kw):
        self.write(self.render(template, **kw))


class MainPage(Handler):
    def get(self):
        self.write("My Blog Root Dir")


### Blog stuff

def blog_key(name='default'):
    return db.Key.from_path('blogs', name)


class BlogPost(db.Model):
    title = db.StringProperty(required=True)
    content = db.TextProperty(required=True)
    created = db.DateTimeProperty(auto_now_add=True)
    last_modified = db.DateTimeProperty(auto_now=True)

    def render(self):
        self._render_text = self.content.replace('\n', '<br>')
        return self.render_str('post.html', p=self)


class Blog(Handler):
    def get(self):
        posts = BlogPost.all().order('-created')
        self.render('front.html', posts=posts)


class PostPage(Handler):
    def get(self, post_id):
        key = db.Key.from_path('BlogPost', int(post_id), parent=blog_key())
        post = db.get(key)

        if not post:
            return self.error(404)

        self.render('permalink.html', post=post)


application = webapp2.WSGIApplication(
    [
        ("/", MainPage)
    ], debug=True
)