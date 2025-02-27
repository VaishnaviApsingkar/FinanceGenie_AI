
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Table, Column, Integer, ForeignKey, Date, Float, String, MetaData
from werkzeug.security import generate_password_hash
from flask_login import UserMixin
from sqlalchemy import create_engine

db = SQLAlchemy()

class User(db.Model, UserMixin):
    # __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    @property
    def is_authenticated(self):
        # Flask-Login calls this to check if the user is authenticated
        return True

    @property
    def is_active(self):
        # Add this to avoid the error; return True to always mark the user as active
        return True

    @property
    def is_anonymous(self):
        # Flask-Login calls this; return False to ensure it's not an anonymous user
        return False

    def get_id(self):
        # This is required by Flask-Login
        return str(self.id)
    
    @property  
    def transaction_table_name(self):
        """
        Returns the table name for the user's transaction table.
        """
        return f"transactions_user_{self.id}"
    
    def create_transaction_table(self):
        """
        Creates a user-specific transaction table dynamically.
        """
        table_name = self.transaction_table_name

        # Dynamically create the table if it doesn't exist
        metadata = MetaData()
        transactions_table = Table(
            table_name,
            metadata,
            Column('id', Integer, primary_key=True),
            Column('bank_id', Integer, nullable=False),
            Column('transaction_date', Date, nullable=False),
            Column('amount', Float, nullable=False),
            Column('type', String(50), nullable=False),
            Column('transaction_name', String(255), nullable=True),
            Column('transaction_id', String(255), nullable=True)
        )
        # Bind to the engine and create the table
        metadata.create_all(bind=db.engine)

    def drop_transaction_table(self):
        """
        Drops the user's transaction table.
        """
        table_name = self.transaction_table_name
        engine = create_engine(db.engine.url)
        with engine.connect() as connection:
            connection.execute(f"DROP TABLE IF EXISTS {table_name}")
    

class BankAccount(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bank_name = db.Column(db.String(150), nullable=False)
    account_nickname = db.Column(db.String(150), nullable=False)
    account_number = db.Column(db.String(20), nullable=False)

    balance = db.Column(db.Float, nullable=False)
