# Udacity CS253 - Web Development
# Unit 3 Assignment - blog

import webapp2
import jinja2
import os

from google.appengine.ext import db

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
    autoescape = True)

class Handler(webapp2.RequestHandler):
  def write(self, *a, **kw):
    self.response.out.write(*a, **kw)

  def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)

  def render(self, template, **kw):
    self.write(self.render_str(template, **kw))

class BlogPost(db.Model):
  subject = db.StringProperty(required = True)
  content = db.TextProperty(required = True)
  created = db.DateTimeProperty(auto_now_add = True)

class FormPage(Handler):
  def render_form(self, subject="", content="", error=""):
    self.render("form.html", subject=subject, content=content, error=error)

  def get(self):
    self.render_form()

  def post(self):
    subject = self.request.get("subject")
    content = self.request.get("content")

    if subject and content:
      posting = BlogPost(subject = subject, content = content)
      posting_key = posting.put()
      # redirect to permalink page
      self.redirect("/unit3/blog/%d" % posting_key.id())
    else:
      error = "We need both a subject and content"
      self.render_form(subject, content, error)

class PostingPage(Handler):
  def get(self, posting_id):
    posting = BlogPost.get_by_id(int(posting_id))
    self.render("blog.html", postings=[posting])


class MainPage(Handler):
  def get(self):
    postings = db.GqlQuery("SELECT * FROM BlogPost ORDER BY created DESC")
    self.render("blog.html", postings=postings)

app = webapp2.WSGIApplication([(r'/unit3/blog', MainPage),
                              (r'/unit3/blog/newpost', FormPage),
                              (r'/unit3/blog/(\d+)', PostingPage),
                              ], debug=True)

