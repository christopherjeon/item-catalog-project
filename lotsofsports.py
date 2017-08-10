from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from catalog_database import Base, Sport, Jersey, User

engine = create_engine('sqlite:///sportscatalog.db')
# Bind the engine to the metadata of the Base class so that the
# declaratives can be accessed through a DBSession instance
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# User list
user1 = User(name="Chris Jeon", email="cjeon97@gmail.com",
picture='http://perfectfitcomputers.ca/wp-content/uploads/2014/08/aviato-logo.jpg')
session.add(user1)
session.commit()

user2 = User(name="Richard Hendriks", email="richard@piedpiper.com",
picture='https://ih0.redbubble.net/image.222702072.4474/flat,800x800,075,f.jpg')
session.add(user2)
session.commit()

# Catalog for Soccer
sport1 = Sport(name = "Soccer")
session.add(sport1)
session.commit()

jersey1 = Jersey(name = "Manchester United Home Kit 17/18",
                 description = "Made by Adidas",
                 price = "$199", sport = sport1, user = user1)
session.add(jersey1)
session.commit()

jersey2 = Jersey(name = "FC Bayern Munich Home Kit 17/18",
                 description = "Made by Adidas",
                 price = "$119", sport = sport1, user = user2)
session.add(jersey2)
session.commit()

jersey3 = Jersey(name = "PSG Home Kit 17/18",
                 description = "Made by Nike",
                 price = "$149", sport = sport1, user = user2)
session.add(jersey3)
session.commit()

jersey4 = Jersey(name = "FC Barcelona  Home Kit 17/18",
                 description = "Made by Nike",
                 price = "$179", sport = sport1, user = user1)
session.add(jersey4)
session.commit()


# Catalog for Baksetball
sport2 = Sport(name = "Basketball")
session.add(sport2)
session.commit()

jersey1 = Jersey(name = "Golden State Warriors Home Jersey",
                 description = "GS Warriors NBA Home Jersey made by Nike",
                 price = "$175", sport = sport2, user = user1)
session.add(jersey1)
session.commit()

jersey2 = Jersey(name = "Toronto Raptors Home Jersey",
                 description = "Raptors NBA Home Jersey made by Nike",
                 price = "$175", sport = sport2, user = user2)
session.add(jersey2)
session.commit()

jersey3 = Jersey(name = "Philadelphia 76ers Home Jersey",
                 description = "76ers NBA Home Jersey made by Nike",
                 price = "$175", sport = sport2, user = user1)
session.add(jersey3)
session.commit()

jersey4 = Jersey(name = "Minnesota Timberwolves Home Jersey",
                 description = "Timberwolves NBA Home Jersey made by Nike",
                 price = "$175", sport = sport2, user = user2)
session.add(jersey4)
session.commit()


# Catalog for Football
sport3 = Sport(name = "Football")
session.add(sport3)
session.commit()

jersey1 = Jersey(name = "Washington Redskins Home Jersey",
                 description = "Redskins NFL Home Jersey made by Nike",
                 price = "$175", sport = sport3, user = user2)
session.add(jersey1)
session.commit()

jersey2 = Jersey(name = "Seattle Seahawks Home Jersey",
                 description = "Seahawks NFL Home Jersey made by Nike",
                 price = "$175", sport = sport3, user = user2)
session.add(jersey2)
session.commit()

jersey3 = Jersey(name = "Oakland Raiders Home Jersey",
                 description = "Raiders NFL Home Jersey made by Nike",
                 price = "$185", sport = sport3, user = user1)
session.add(jersey3)
session.commit()

jersey4 = Jersey(name = "Atlanta Falcons Home Jersey",
                 description = "Falcons NFL Home Jersey made by Nike",
                 price = "$185", sport = sport3, user = user1)
session.add(jersey4)
session.commit()


# Catalog for Hockey
sport4 = Sport(name = "Hockey")
session.add(sport4)
session.commit()

jersey1 = Jersey(name = "Vancouver Canucks Home Jersey",
                 description = "Canucks NHL Home Jersey made by Adidas",
                 price = "$225", sport = sport4, user = user1)
session.add(jersey1)
session.commit()

jersey2 = Jersey(name = "Tampa Bay Lightning Home Jersey",
                 description = "Lightning NHL Home Jersey made by Adidas",
                 price = "$205", sport = sport4, user = user1)
session.add(jersey2)
session.commit()

jersey3 = Jersey(name = "New York Rangers Home Jersey",
                 description = "Rangers NHL Home Jersey made by Adidas",
                 price = "$215", sport = sport4, user = user2)
session.add(jersey3)
session.commit()

jersey4 = Jersey(name = "Ottawa Senators Home Jersey",
                 description = "Senators NHL Home Jersey made by Adidas",
                 price = "$235", sport = sport4, user = user1)
session.add(jersey4)
session.commit()


# Catalog for Baseball
sport5 = Sport(name = "Baseball")
session.add(sport5)
session.commit()

jersey1 = Jersey(name = "Toronto Blue Jays Home Jersey",
                 description = "Blue Jays MLB Home Jersey made by Majestic",
                 price = "$225", sport = sport5, user = user1)
session.add(jersey1)
session.commit()

jersey2 = Jersey(name = "Los Angeles Dodgers Home Jersey",
                 description = "Dodgers MLB Home Jersey made by Majestic",
                 price = "$205", sport = sport5, user = user1)
session.add(jersey2)
session.commit()

jersey3 = Jersey(name = "Washington Nationals Home Jersey",
                 description = "Nationals MLB Home Jersey made by Majestic",
                 price = "$215", sport = sport5, user = user2)
session.add(jersey3)
session.commit()

jersey4 = Jersey(name = "Houston Astros Home Jersey",
                 description = "Astros MLB Home Jersey made by Majestic",
                 price = "$235", sport = sport5, user = user2)
session.add(jersey4)
session.commit()
