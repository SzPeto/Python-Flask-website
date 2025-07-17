from website.db_models import db
from website import create_app, port

app = create_app()

if __name__ == "__main__":
    
    with app.app_context():
        db.create_all()
    
    app.run(host = "0.0.0.0", debug=False, port=port)