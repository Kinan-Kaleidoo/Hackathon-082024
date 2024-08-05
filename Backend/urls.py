from views import  media, doc, search, audio, audio_text, video, nlp, ms_media, ms_audio, ms_search
from auth import register, login, logout


def configure_routes(app):
    app.add_url_rule('/', 'login', login)
    app.add_url_rule('/login', 'login', login, methods=["GET", "POST"])
    app.add_url_rule('/logout', 'logout', logout, methods=["GET"])
    app.add_url_rule('/register', 'register', register, methods=[ "POST"])
    app.add_url_rule('/media', 'media', media, methods=["GET", "POST"])
    app.add_url_rule('/search', 'search', search, methods=["GET", "POST"])
    app.add_url_rule('/doc', 'doc', doc, methods=["GET", "POST"])
    app.add_url_rule('/audio', 'audio', audio, methods=["GET", "POST"])
    app.add_url_rule('/audio_text', 'audio_text', audio_text, methods=["GET", "POST"])
    app.add_url_rule('/video', 'video', video, methods=["GET", "POST"])
    app.add_url_rule('/nlp', 'nlp', nlp, methods=["POST"])
    app.add_url_rule('/nlp', 'nlp', nlp, methods=["POST"])
    app.add_url_rule('/ms/media', 'ms/media', ms_media, methods=["POST"])
    app.add_url_rule('/ms/audio', 'ms/audio', ms_audio, methods=["POST"])
    app.add_url_rule('/ms/search', 'ms/search', ms_search, methods=["POST"])



