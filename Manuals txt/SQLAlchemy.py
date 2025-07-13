# App configuration
app = Flask(__name__)
    # configure Flask database
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///database.db" # It has to be in root folder
db = SQLAlchemy(app)

# Model class
class Entry(db.Model):
    # You can't have the self parameter, since we are inheriting from SQLAlchemy model
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    description = db.Column(db.String(100), nullable = False) # NULL in SQL
    category = db.Column(db.String(50))
    price = db.Column(db.Float)
    date = db.Column(db.String(20), default = today)

    def __repr__(self) -> str: # Repr dunder method represents the string representation of object
                               # -> This symbol means type hinting, mostly for autocomplete purposes
        return f"Task {self.id}"

# Most important commands
# 1. Add a new entry
new_entry = Entry(
     description="Coffee",
     price=2.5,
     category="Food",
     date="2025-06-10"
)
db.session.add(new_entry)
db.session.commit()

# 2. Get all entries
entries = Entry.query.all()

# 3. Get one entry by ID (SQLAlchemy 2+)
entry = db.session.get(Entry, 1)

# 4. Get one entry by ID (older way)
entry = Entry.query.get(1)

# 5. Filter entries by column
filtered = Entry.query.filter_by(category="Food").all()

# 6. Order entries by a column (ascending)
ordered = Entry.query.order_by(Entry.price).all()

# 7. Delete a specific entry
entry = db.session.get(Entry, 1)
db.session.delete(entry)
db.session.commit()

# 8. Delete all entries
Entry.query.delete()
db.session.commit()

# 9. Update an existing entry
entry = db.session.get(Entry, 1)
entry.price = 4.0
db.session.commit()