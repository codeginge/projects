archiver - media organization project
by: Michael Roberts
last updated: 9/12/26

GOAL:
create an archival system to store and reteive media items. this archive will connect the digital and physical 
locations to user defined context tags. when searched, the user will get physical and digital media locations
along with all of the information that was entered in the archival process. 

CONSTRAINTS:
-search archive by name, tag, or location
-search query returns item name, thumbnail, physical location, digital location, and tags
-adding to archive is straight forward

MEDIA TYPES:
-physical
    -photos
        -4x6 photos
        -slides
        -negatives
    -paper
        -drawings
        -notebooks
        -books
    -audio
        -cds
        -records
        -cassets
        -reel to reel
    -video
        -vhf tapes
        -dvd
        -blueray
-digital
    -pdf
    -photos
    -videos

SEARCH TERMS:
-date
    -month
    -day
    -year
-person
-activity
-location
-type
    -video
    -image
    -audio
    -pdf

DATA TABLES: 
Rule: all location identifiers are infinitely expandable in a grid pattern 

Room List (RL)
Rule: as you add rooms they go up cronologically in decimal
    [room number, tags
    0, "address:102_dogwood,room:garage,owner:jeb"
    1, "address:102_dogwood,room:living_room,owner:kevin"]

Physical Locations (PL)
Rule: <room decimal><cabinet letter><row number><column letter><inner row number><inner column letter>, tags
example for room 0, cabinet A, row 1, column B, cd storage:
    [location, tags
    "0A1B", "type:cd"
    "0A1C", "type:cd"]

Item List (IL)
Items can be added manually or in bulk using the code
    [name, tags, physical location
    "jeb_baby_picture", "date:1984,type:4x6photo","2B13AA"
    "in_a_sentimental_mood","type:cd,date:1935,artist:Duke_Ellington","0A1F"
    ]

FUNCTIONS:
these functions are used to build the RL, PL and add to the IL. 
add_rooms(room_names)
add_locations(room, cabinet, rows, columns, rows, columns, tags)
add_items()

TAGS:
these are used to add detail to rooms, physical locations, and items. tags are an infinately expandable list

