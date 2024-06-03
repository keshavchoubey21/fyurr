from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()

#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#


class Venue(db.Model):
    __tablename__ = 'venues'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    webiste = db.Column(db.String(120))
    seeking_talent = db.Column(db.Boolean)
    seeking_desc = db.Column(db.String(500))
    past_show_count = db.Column(db.Integer)
    upcoming_show_count = db.Column(db.Integer)
    shows_list = db.relationship('Show', backref='venue', lazy=True)
    genre_list = db.relationship('Venue_Genre', backref='venue', collection_class=list, lazy=True)

    def __repr__(self):
      return f'<Todo {self.id} {self.name} {self.city} {self.state} {self.address} {self.phone} {self.image_link} {self.facebook_link} {self.webiste} {self.seeking_talent} {self.seeking_desc} {self.past_show_count} {self.upcoming_show_count} {self.shows_list} {self.genre_list}>'

    # TODO: implement any missing fields, as a database migration using Flask-Migrate

class Artist(db.Model):
    __tablename__ = 'artists'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String(120))
    seeking_venue = db.Column(db.Boolean)
    seeking_desc = db.Column(db.String(500))
    past_show_count = db.Column(db.Integer)
    upcoming_show_count = db.Column(db.Integer)
    shows_list = db.relationship('Show', backref='artist', lazy=True)
    genre_list = db.relationship('Artist_Genre', backref='artist', collection_class=list, lazy=True)

class Show(db.Model):
   __tablename__ = 'shows'
   id = db.Column(db.Integer(), primary_key=True)
   start_time = db.Column(db.DateTime)
   venue_id=db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
   artist_id=db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)

class Venue_Genre(db.Model):
   __tablename__ = 'venue_genre'
   id = db.Column(db.Integer, primary_key=True)
   genre = db.Column(db.String(100), nullable=False)
   venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)

class Artist_Genre(db.Model):
   __tablename__ = 'artist_genre'
   id = db.Column(db.Integer, primary_key=True)
   genre = db.Column(db.String(100), nullable=False)
   artist_id = db.Column(db.Integer, db.ForeignKey('artists.id'), nullable=False)