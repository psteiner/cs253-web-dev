import webapp2
import cgi
import codecs
import jinja2
import os
import re

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                                autoescape = True)

def render_str(template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)
    
class BaseHandler(webapp2.RequestHandler):
    def render(self, template, **kw):
        self.response.out.write(render_str(template, **kw))

    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

        
USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)
    
PASSWORD_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASSWORD_RE.match(password)
    
EMAIL_RE = re.compile(r"^[\S]+@[\S]+\.[\S]+$")
def valid_email(email):
        return not email or EMAIL_RE.match(email)
    
class SignupHandler(BaseHandler):
    def get(self):
        self.render('signup-form.html')
        
    def post(self):
        has_error = False
        
        
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username = username, email = email)
        
        if not valid_username(username):
            has_error = True
            params["error_username"] = "That's not a valid username."
            
        if not valid_password(password):
            has_error = True
            params["error_password"] = "That's not a valid password."
        elif password != verify:
            has_error = True
            params["error_verify"] = "Your passwords don't match."

        if not valid_email(email):
            has_error = True
            params["error_email"] = "Your email is not a valid email address."
        
        if has_error:
            # do not return password values
            self.render('signup-form.html', **params )
        else:
            self.redirect('/unit2/welcome?username=' + username)

class WelcomeHandler(BaseHandler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render('welcome.html', username = username)
        else:
            self.redirect('/unit2/signup')

app = webapp2.WSGIApplication(
    [('/unit2/signup', SignupHandler),
     ('/unit2/welcome', WelcomeHandler)
    ], debug=True)
