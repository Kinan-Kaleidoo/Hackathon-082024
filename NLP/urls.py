from views import summary_text,improve,subject_extract,sentiment_analysis

def configure_routes(app):
    app.add_url_rule('/improve', 'improve', improve,methods=["POST", "GET"])
    app.add_url_rule('/subject_extract', 'subject_extract', subject_extract,methods=["POST", "GET"])
    app.add_url_rule('/summary_text', 'summary_text', summary_text,methods=["POST", "GET"])
    app.add_url_rule('/sentiment_analysis', 'sentiment_analysis', sentiment_analysis,methods=["POST", "GET"])
    