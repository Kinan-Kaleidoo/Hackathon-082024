from views import index, media, doc, search,audio,video
from auth import register, login, logout


def configure_routes(app):
    app.add_url_rule('/', 'login', login)
    app.add_url_rule('/login', 'login', login, methods=["GET", "POST"])
    app.add_url_rule('/logout', 'logout', logout, methods=["GET"])
    app.add_url_rule('/register', 'register', register, methods=[ "POST"])
    app.add_url_rule('/homepage', 'index', index)
    app.add_url_rule('/media', 'media', media, methods=["GET", "POST"])
    app.add_url_rule('/search', 'search', search, methods=["GET", "POST"])
    app.add_url_rule('/doc', 'doc', doc, methods=["GET", "POST"])
    app.add_url_rule('/audio', 'audio', audio, methods=["GET", "POST"])
    app.add_url_rule('/video', 'video', video, methods=["GET", "POST"])


