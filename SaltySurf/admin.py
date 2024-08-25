'''
CREATING A NEW DATABASE
-----------------------
Read explanation here: https://flask-sqlalchemy.palletsprojects.com/en/2.x/contexts/

In the terminal navigate to the project folder just above the miltontours package
Type 'python' to enter the python interpreter. You should see '>>>'
In python interpreter type the following (hitting enter after each line):
    from miltontours import db, create_app
    db.create_all(app=create_app())
The database should be created. Exit python interpreter by typing:
    quit()
Use DB Browser for SQLite to check that the structure is as expected before 
continuing.

ENTERING DATA INTO THE EMPTY DATABASE
-------------------------------------

# Option 1: Use DB Browser for SQLite
You can enter data directly into the brands or surfboards table by selecting it in
Browse Data and clicking the New Record button. The id field will be created
automatically. However be careful as you will get errors if you do not abide by
the expected field type and length. In particular the DateTime field must be of
the format: 2020-05-17 00:00:00.000000

# Option 2: Create a database seed function in an Admin Blueprint
See below. This blueprint needs to be enabled in __init__.py and then can be 
accessed via http://127.0.0.1:5000/admin/dbseed/
Database constraints mean that it can only be used on a fresh empty database
otherwise it will error. This blueprint should be removed (or commented out)
from the __init__.py after use.

Use DB Browser for SQLite to check that the data is as expected before 
continuing.
'''

from flask import Blueprint
from . import db
from .models import Brand, Surfboard
import datetime

admin_bp = Blueprint('admin', __name__)

# function to put some seed data in the database
@admin_bp.route('/dbseed')
def dbseed():
    brand1 = Brand(name='Billabong', image='billabong.jpg', \
        description='''With humble beginnings in 1969, Billabong has proven to be one of the industry leaders when it comes to durfboards. When buying from billabong you can be assured that functionality as well as design is meticulously thought out in all of their products.''')
    brand2 = Brand(name='Quiksilver', image='quicksilver.jpg', \
        description='''One of the world's leaders in outdoor sports. Quiksilver produces a diversified mix of beginner, intermediate and expert surf products suitable for all skill levels.''')
    brand3 = Brand(name='Ripcurl', image='ripcurl.jpg', \
        description='''An Australian brand founded in 1969 at the beautiful Torquay, Victoria. When creating Ripcurl these blokes knew what they were doing! They are proud winners of several awards for their products including the SIMA (Surf Industry Manufacturers Association) Award.''')
      
    try:
        db.session.add(brand1)
        db.session.add(brand2)
        db.session.add(brand3)
        db.session.commit()
    except:
        return 'There was an issue adding the brands in dbseed function'

    b1 = Surfboard(brand_id=brand1.id, boardlevel = 'Intermediate', image='billabong1.jpg', price=459.99,\
        name='Tang Fish Shortboard',\
        description= 'This Billabong shortboard approximately 5.6ft will make sure you impress everyone on the beach with the waves you catch. Equipped with three fins in a thruster formation you will have all the speed you need for your next beach trip!') 
    b2 = Surfboard(brand_id=brand1.id, boardlevel = 'Expert', image='billabong2.jpg', price=569.99,\
        name='Timber Tantrum Shortboard',\
        description= 'This Billabong shortboard measures approximately 5.4ft with a smooth timber finish. You will be sure to carve through the waves like an axe through logs. This is aparts of Billabongs eco-series boards that donate 5 percent of every purchase to a global charity working to reduce greenhouse emissions.')
    b3 = Surfboard(brand_id=brand1.id, boardlevel = 'Expert', image='billabong3.jpg', price=519.99,\
        name='Absolute Air Shortboard',\
        description= 'The name says it all! Billabongs newest model includes a fair amount of customizable options for those with the appetite for adrenaline. This was the official board of Kelly Slater during his 2023 Pipeline conpetition win in Hawaii.')
    b4 = Surfboard(brand_id=brand2.id, boardlevel = 'Beginner', image='quicksilver1.jpg', price=399.99,\
        name='Never Winter Longboard',\
        description= 'This 9.1ft Quiksilver board is the perfect edition to add to your quiver of boards. This is a board for the days meant to cruise and just enjoy yourself. A great board for beginners and intermediates alike!')                
    b5 = Surfboard(brand_id=brand2.id, boardlevel = 'Beginner', image='quicksilver2.jpg', price=478.99,\
        name='Wave Rider Longboard',\
        description= 'Quiksilver\'s Wave Rider 9.6ft longboard is designed for surfers who crave speed and agility on medium to large waves. Its sleek, streamlined shape allows for quick turns and smooth transitions, making it perfect for carving through the surf with precision.')
    b6 = Surfboard(brand_id=brand2.id, boardlevel = 'Intermediate', image='quicksilver3.jpg', price=705.99,\
        name='Maverick Longboard',\
        description= 'The Ocean Maverick is a versatile board built for both beginners and advanced surfers. With a wider nose and a rounded tail, this board offers great stability and ease of paddling, while still allowing for impressive maneuverability on a variety of wave conditions.')
    b7 = Surfboard(brand_id=brand3.id, boardlevel = 'Intermediate', image='ripcurl1.jpg', price=590.99,\
        name='Storm Chaser Shortboard',\
        description= 'The Storm Chaser is crafted for surfers who thrive in big wave conditions. With its reinforced construction and increased volume, this board provides the stability and buoyancy needed to tackle towering waves, ensuring both performance and safety during extreme surf sessions. Mark (pictured left) is carrying the Storm Chaser.')
    b8 = Surfboard(brand_id=brand3.id, boardlevel = 'Expert', image='ripcurl2.jpg', price=569.99,\
        name='Tidal Charger Shortboard',\
        description= 'Ripcurl\'s newest shortboard is designed for surfers who thrive on powerful, challenging waves, the Tidal Charger offers exceptional performance and control. Its high-performance shortboard design features a narrow tail and sharp rails, allowing for explosive turns and rapid acceleration.')
    b9 = Surfboard(brand_id=brand3.id, boardlevel = 'Intermediate', image='ripcurl3.jpg', price=349.99,\
        name='Reef Seeker Shortboard',\
        description= 'Tailored for adventurous surfers who love exploring reef breaks, the Reef Seeker is built tough with extra durability to withstand rocky conditions. Its concave bottom and pointed nose ensure precise control and excellent grip on the face of the wave, allowing surfers to navigate challenging breaks with confidence.')
    b10 = Surfboard(brand_id=brand3.id, boardlevel = 'Intermediate', image='ripcurl4.jpg', price=759.99,\
        name='Sapphire Drifter Longboard',\
        description= 'The Sapphire Drifter is a beautifully crafted fish surfboard, ideal for those looking to enjoy a playful and lively ride. Its wide nose, thick rails, and swallow tail offer excellent floatation and stability, allowing surfers to effortlessly glide and maneuver on smaller waves.')
    b11 = Surfboard(brand_id=brand3.id, boardlevel = 'Expert', image='ripcurl5.jpg', price=659.99,\
        name='Aqua Phantom Shortboard',\
        description= 'The Aqua Phantom is a high-performance shortboard designed for advanced surfers who crave agility and speed. Its narrow outline, pronounced rocker, and sharp rails allow for rapid, precise maneuvers, making it perfect for carving up steep waves and performing aerials.')
    b12 = Surfboard(brand_id=brand3.id, boardlevel = 'Beginner', image='ripcurl6.jpg', price=319.99,\
        name='Breeze Rider Longboard',\
        description= 'The Breeze Rider is a lightweight, easy-to-handle board tailored for beginners and casual surfers. Its soft-top construction and rounded shape provide maximum stability and safety, making it the perfect choice for those learning the basics and wanting a fun, carefree surfing experience.')
    b13 = Surfboard(brand_id=brand2.id, boardlevel = 'Beginner', image='quicksilver4.jpg', price=259.99,\
        name='Crystal Explorer Longboard',\
        description= 'Designed for adventurous surfers who love discovering new breaks, the Crystal Explorer combines durability with versatility. Its hybrid shape features a slightly wider outline and a swallow tail, providing stability in various wave conditions while maintaining the agility needed for quick maneuvers and fast paddling.')

    try:
        db.session.add(b1)
        db.session.add(b2)
        db.session.add(b3)
        db.session.add(b4)
        db.session.add(b5)
        db.session.add(b6)
        db.session.add(b7)
        db.session.add(b8)
        db.session.add(b9)
        db.session.add(b10)
        db.session.add(b11)
        db.session.add(b12)
        db.session.add(b13)
        db.session.commit()
    except:
        return 'There was an issue adding a surfboard in dbseed function'

    return 'DATA LOADED'