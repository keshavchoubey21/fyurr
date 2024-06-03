#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
from flask import Flask, render_template, request, Response, flash, redirect, url_for
from flask_moment import Moment
import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
from flask_migrate import Migrate
from models import db, Venue, Artist, Show, Venue_Genre, Artist_Genre
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
app.app_context().push()
# db = SQLAlchemy(app)
db.init_app(app)
migrate = Migrate(app,db)

#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format, locale='en')

app.jinja_env.filters['datetime'] = format_datetime

#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  
  data = []
  areas = db.session.query(Venue.city,Venue.state).distinct().all();
  # print(areas);
  for area in areas:
     city = area[0]
     state= area[1]
     sub_list = {
        "city": city,
        "state": state,
        "venues": []
     }
    #  print('area value == '+ str(area))
     venues = Venue.query.filter_by(city=city,state=state).all();
    #  print(venues)
     venues_list = []
     for venue in venues:
        venues_sub_list = {
           "id": venue.id,
           "name": venue.name,
           "num_upcoming_shows": venue.upcoming_show_count
        }
        # print('for venue=' + str(venue) + ' sub_list = ' + str(venues_sub_list))
        venues_list.append(venues_sub_list)
    #  print('venues_list === '+ str(venues_list))
     sub_list = {
        "city": city,
        "state": state,
        "venues": venues_list
     }
     data.append(sub_list)

     
  return render_template('pages/venues.html', areas=data);

@app.route('/venues/search', methods=['POST'])
def search_venues():

  search_term = request.form.get("search_term");
  venues_query_result = db.session.query(Venue).filter(Venue.name.ilike('%' + search_term + '%')).all();
  list_of_venues = []
  for venue in venues_query_result:
     venue_list = {
        "id": venue.id,
        "name": venue.name,
        "num_upcoming_shows": venue.upcoming_show_count
     }
     list_of_venues.append(venue_list);
  response = {
     "count": len(list_of_venues),
     "data": list_of_venues
  }


  return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id

  data2={
    "id": 2,
    "name": "The Dueling Pianos Bar",
    "genres": ["Classical", "R&B", "Hip-Hop"],
    "address": "335 Delancey Street",
    "city": "New York",
    "state": "NY",
    "phone": "914-003-1132",
    "website": "https://www.theduelingpianos.com",
    "facebook_link": "https://www.facebook.com/theduelingpianos",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1497032205916-ac775f0649ae?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=750&q=80",
    "past_shows": [],
    "upcoming_shows": [],
    "past_shows_count": 0,
    "upcoming_shows_count": 0,
  }
  data3={
    "id": 3,
    "name": "Park Square Live Music & Coffee",
    "genres": ["Rock n Roll", "Jazz", "Classical", "Folk"],
    "address": "34 Whiskey Moore Ave",
    "city": "San Francisco",
    "state": "CA",
    "phone": "415-000-1234",
    "website": "https://www.parksquarelivemusicandcoffee.com",
    "facebook_link": "https://www.facebook.com/ParkSquareLiveMusicAndCoffee",
    "seeking_talent": False,
    "image_link": "https://images.unsplash.com/photo-1485686531765-ba63b07845a7?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=747&q=80",
    "past_shows": [{
      "artist_id": 5,
      "artist_name": "Matt Quevedo",
      "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      "start_time": "2019-06-15T23:00:00.000Z"
    }],
    "upcoming_shows": [{
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-01T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-08T20:00:00.000Z"
    }, {
      "artist_id": 6,
      "artist_name": "The Wild Sax Band",
      "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      "start_time": "2035-04-15T20:00:00.000Z"
    }],
    "past_shows_count": 1,
    "upcoming_shows_count": 1,
  }

  venue = Venue.query.get(venue_id);
  genres = Venue_Genre.query.filter_by(venue_id=venue_id).all();
  print(venue)
  genre_list = []
  for g in genres:
     genre_list.append(g.genre)

  #fetching past & upcoming shows
  current_datetime = datetime.now()
  past_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id == venue_id, Show.start_time < current_datetime).all()
  past_shows_list = []
  past_show_count = 0
  for show in past_shows_query:
     past_show = {
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
     }
     past_show_count +=1
     past_shows_list.append(past_show)
  
  upcoming_shows_query = db.session.query(Show).join(Artist).filter(Show.venue_id == venue_id, Show.start_time > current_datetime).all()
  upcoming_shows_list = []
  upcoming_show_count = 0
  for show in upcoming_shows_query:
     upcoming_show = {
        "artist_id": show.artist.id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
     }
     upcoming_show_count +=1
     upcoming_shows_list.append(upcoming_show)

  data = {
     "id": venue.id,
    "name": venue.name,
    "genres": genre_list,
    "address": venue.address,
    "city": venue.city,
    "state": venue.state,
    "phone": venue.phone,
    "website": venue.webiste,
    "facebook_link": venue.facebook_link,
    "seeking_talent": venue.seeking_talent,
    "image_link": venue.image_link,
    "seeking_description": venue.seeking_desc,
    "past_shows": past_shows_list,
    "upcoming_shows": upcoming_shows_list,
    "past_shows_count": past_show_count,
    "upcoming_shows_count": upcoming_show_count,
  }

  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():

  venue = None
  genre_item = None
  try:
    form = VenueForm(request.form)
    if form.validate():
       venue = Venue(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        address=form.address.data,
        phone=form.phone.data,
        facebook_link=form.facebook_link.data,
        image_link=form.image_link.data,
        webiste=form.website_link.data,
        seeking_talent=form.seeking_talent.data,
        seeking_desc=form.seeking_description.data
      )
       db.session.add(venue)
       db.session.commit()
       for genre in form.genres.data:
         genre_item = Venue_Genre(genre = genre, venue_id = venue.id)
         db.session.add(genre_item)

       db.session.commit()
       flash('Venue: {0} created successfully'.format(venue.name))
    else:
       flash('Form validation failed. Please check the form inputs.')
  except Exception as err:
    flash('An error occurred creating the Venue: {0}. Error: {1}'.format(venue.name, err))
    db.session.rollback()
  finally:
     db.session.close()
     return render_template('pages/home.html')

@app.route('/venues/<venue_id>/delete', methods=['DELETE'])
def delete_venue(venue_id):
  try:
     venue = Venue.query.get(venue_id)
     if venue:
        db.session.delete(venue)
        db.session.commit()
        flash('Venue: {0} deleted successfully'.format(venue.name))
        return render_template('pages/home.html')
     else:
        print('venue not deleted')
  except Exception as e:
     db.session.rollback()
     print('venue except blocks')

#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():

  data=[]
  artists = db.session.query(Artist).all();
  for artist in artists:
     data.append({
        "id": artist.id,
        "name": artist.name
     })
  return render_template('pages/artists.html', artists=data)

@app.route('/artists/search', methods=['POST'])
def search_artists():

  search_term = request.form.get("search_term");
  artists_query_result = db.session.query(Artist).filter(Artist.name.ilike('%' + search_term + '%')).all();
  list_of_artists = []
  for artist in artists_query_result:
     artist_list = {
        "id": artist.id,
        "name": artist.name,
        "num_upcoming_shows": artist.upcoming_show_count
     }
     list_of_artists.append(artist_list);
  response = {
     "count": len(list_of_artists),
     "data": list_of_artists
  }
  return render_template('pages/search_artists.html', results=response, search_term=request.form.get('search_term', ''))

@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):

  artist = Artist.query.get(artist_id);
  genres = Artist_Genre.query.filter_by(artist_id=artist_id).all();
  genre_list = []
  for g in genres:
     genre_list.append(g.genre)

  #fetching past & upcoming shows
  current_datetime = datetime.now()
  past_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id, Show.start_time < current_datetime).all()
  past_shows_list = []
  past_show_count = 0
  for show in past_shows_query:
     past_show = {
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
     }
     past_show_count +=1
     past_shows_list.append(past_show)
  
  upcoming_shows_query = db.session.query(Show).join(Venue).filter(Show.artist_id == artist_id, Show.start_time > current_datetime).all()
  upcoming_shows_list = []
  upcoming_show_count = 0
  for show in upcoming_shows_query:
     upcoming_show = {
        "venue_id": show.venue.id,
        "venue_name": show.venue.name,
        "venue_image_link": show.venue.image_link,
        "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
     }
     upcoming_show_count +=1
     upcoming_shows_list.append(upcoming_show)

  data = {
     "id": artist.id,
    "name": artist.name,
    "genres": genre_list,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "image_link": artist.image_link,
    "seeking_description": artist.seeking_desc,
    "past_shows": past_shows_list,
    "upcoming_shows": upcoming_shows_list,
    "past_shows_count": past_show_count,
    "upcoming_shows_count": upcoming_show_count,
  }

  return render_template('pages/show_artist.html', artist=data)
  

#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  form = ArtistForm()
  artist_data = Artist.query.get(artist_id);

  if artist_data is None:
    flash(f'Artist with ID {artist_id} does not exist.')
    return redirect(url_for('artists'))

  genres = Artist_Genre.query.filter_by(artist_id=artist_id).all();
  genre_list = []
  for g in genres:
     genre_list.append(g.genre)
  
  artist={
    "id": artist_data.id,
    "name": artist_data.name,
    "genres": genre_list,
    "city": artist_data.city,
    "state": artist_data.state,
    "phone": artist_data.phone,
    "website_link": artist_data.website,
    "facebook_link": artist_data.facebook_link,
    "seeking_venue": artist_data.seeking_venue,
    "seeking_description": artist_data.seeking_desc,
    "image_link": artist_data.image_link
  }
  form.process(id=artist_data.id, name=artist_data.name, genres=genre_list, city=artist_data.city, state=artist_data.state, phone=artist_data.phone, website_link=artist_data.website, facebook_link=artist_data.facebook_link,
               seeking_venue=artist_data.seeking_venue, seeking_description=artist_data.seeking_desc, image_link=artist_data.image_link)

  return render_template('forms/edit_artist.html', form=form, artist=artist)

@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):

  form = ArtistForm()
  try:
    form = ArtistForm(request.form)
    print(form.genres.data)
    if form.validate():
       artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        facebook_link=form.facebook_link.data,
        image_link=form.image_link.data,
        website=form.website_link.data,
        seeking_venue=form.seeking_venue.data,
        seeking_desc=form.seeking_description.data
      )
       db.session.add(artist)
       db.session.commit()
       for genre in form.genres.data:
         genre_item = Artist_Genre(genre = genre, artist_id = artist.id)
         db.session.add(genre_item)

       db.session.commit()
       flash('Artist: {0} updated successfully'.format(artist.name))
    else:
       flash('Form validation failed. Please check the form inputs.')
  except Exception as err:
    flash('An error occurred updating the Artist: {0}. Error: {1}'.format(artist.name, err))
    db.session.rollback()
  finally:
     db.session.close()
     return redirect(url_for('show_artist', artist_id=artist_id))

@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  form = VenueForm()
  venue_data = Venue.query.get(venue_id);

  if venue_data is None:
    flash(f'Venue with ID {venue_data} does not exist.')
    return redirect(url_for('venues'))

  genres = Venue_Genre.query.filter_by(venue_id=venue_id).all();
  genre_list = []
  for g in genres:
     genre_list.append(g.genre)

  venue={
    "id": venue_data.id,
    "name": venue_data.name,
    "genres": genre_list,
    "address": venue_data.address,
    "city": venue_data.city,
    "state": venue_data.state,
    "phone": venue_data.phone,
    "website": venue_data.webiste,
    "facebook_link": venue_data.facebook_link,
    "seeking_talent": venue_data.seeking_talent,
    "seeking_description": venue_data.seeking_desc,
    "image_link": venue_data.image_link
  }
  form.process(id=venue_data.id, name=venue_data.name, genres=genre_list, address=venue_data.address, city=venue_data.city, state=venue_data.state, phone=venue_data.phone, website_link=venue_data.webiste, facebook_link=venue_data.facebook_link,
               seeking_venue=venue_data.seeking_talent, seeking_description=venue_data.seeking_desc, image_link=venue_data.image_link)

  return render_template('forms/edit_venue.html', form=form, venue=venue)

@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  
  form = VenueForm()
  try:
    form = VenueForm(request.form)
    if form.validate():
       venue = Venue(
        name=form.name.data,
        address=form.address.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        facebook_link=form.facebook_link.data,
        image_link=form.image_link.data,
        webiste=form.website_link.data,
        seeking_talent=form.seeking_talent.data,
        seeking_desc=form.seeking_description.data
      )
       db.session.add(venue)
       db.session.commit()
       for genre in form.genres.data:
         genre_item = Venue_Genre(genre = genre, venue_id = venue.id)
         db.session.add(genre_item)

       db.session.commit()
       flash('Venue: {0} updated successfully'.format(venue.name))
    else:
       flash('Form validation failed. Please check the form inputs.')
  except Exception as err:
    flash('An error occurred updating the Venue: {0}. Error: {1}'.format(venue.name, err))
    db.session.rollback()
  finally:
     db.session.close()
     return redirect(url_for('show_venue', venue_id=venue_id))

  

#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)

@app.route('/artists/create', methods=['POST'])
def create_artist_submission():

  artist = None
  genre_item = None
  try:
    form = ArtistForm(request.form)
    if form.validate():
       artist = Artist(
        name=form.name.data,
        city=form.city.data,
        state=form.state.data,
        phone=form.phone.data,
        facebook_link=form.facebook_link.data,
        image_link=form.image_link.data,
        website=form.website_link.data,
        seeking_venue=form.seeking_venue.data,
        seeking_desc=form.seeking_description.data
      )
       db.session.add(artist)
       db.session.commit()
       for genre in form.genres.data:
         genre_item = Artist_Genre(genre = genre, artist_id = artist.id)
         db.session.add(genre_item)

       db.session.commit()
       flash('Artist ' + request.form['name'] + ' was successfully listed!')
    else:
       flash('Form validation failed. Please check the form inputs.')
  except Exception as err:
    flash('An error occurred creating the Artist: {0}. Error: {1}'.format(artist.name, err))
    db.session.rollback()
  finally:
     db.session.close()
     return render_template('pages/home.html')
  


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():

  shows = db.session.query(Show).join(Artist).all()
  data = []
  for show in shows:
     sub_list = {
        "venue_id": show.venue_id,
        "venue_name": show.venue.name,
        "artist_id": show.artist_id,
        "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link,
        "start_time": show.start_time.strftime("%Y-%m-%dT%H:%M:%S.000Z")
     }
     data.append(sub_list)

  return render_template('pages/shows.html', shows=data)

@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)

@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  
  form = ShowForm()
  try:
     form = ShowForm(request.form)
     show = Show(
        artist_id = form.artist_id.data,
        venue_id = form.venue_id.data,
        start_time = form.start_time.data
     )
     db.session.add(show)
     db.session.commit()
  except:
    flash('An error occurred. Show could not be listed.')
    db.session.rollback()
  finally:
    return render_template('pages/home.html')

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
