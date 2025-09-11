# V3

## functions
1 - import google sheet ground truth

2 - create json data file for curriculum 

3 - create json data file for student progression and responce

4 - hold updates from users in a queue that updates every minute if there are any updates

5 - update google sheet from json and queued updates from users


## processes
1 - web service (user interaction handling)
	1a -Done- log user in with username and password
	2a -Done- show student users their tech tree and provide links to docs for learning
	2b -Done- allow students to comment on items in the tech tree
	2c -Done- put student comments into user_input_json_file 
	3a -Done- allow teacher to see class wide tech tree
	3b -Done- allow teachers to see student specific tech tree
	3c -Done- allow teachers to put in completion for items in student's tech tree

2 - data handler (avoid data collisions)
	1a -Done- keeps information in google sheet, and json data set up to date
	1b -Done- creates resources from template
	1c -Done- removes resources (if at least doc_link and id are deleted on google sheet)
	2a -Done- go through list of people on status page and create student and teacher login creds
	3a -Done- keep ids up to date with ids for techs, projects and contracts
	3b -Done- per student put gsheet data into json dict structure and save to status file
	4a -Done- run through user input queue and update comments from student inputs
	4b -Done- run through user input queue and update points from teacher inputs
	5a -InProgress- update status gsheet



## JSON Data Structures
### ims_data.json
[
	{
		"name":"",
		"type":"",
		"sub_type":"",
		"core":"",
		"id":"",
		"dependency":"",
		"doc_link":""
	},
]	
### status.json
[
	{
		"first":"",
		"last":"",
		"class":"",
		"type":"",
		"username":"",
		"password":"",
		"tech_count": 0,
		"tech_mastery": 0,
		"tech_completion":0,
		"project_count": 0,
		"project_mastery": 0,
		"project_completion":0,
		"contract_count": 0,
		"contract_mastery": 0,
		"contract_completion":0,
		"raw_data": [
			{			
				"id":"",
				"points": 0,
				"comments": ""
			}
		]	
	}
]
### updates.json
[
	{
	    "username": "",
	    "item_id": "",
	    "timestamp": "",
	    "points": 0
	},
	{
	    "username": "",
	    "item_id": "",
	    "timestamp": "",
	    "comment": ""
	}
]


























# V2 

## setup

### postgreSQL database
#### rpi os and ssh setup
using a rasperry pi 4 and a 32gb sd card, setup the pi using raspberry pi imager. choose rasperry pi 4 as the "raspberry pi device", choose "raspberry pi os light (64-bit)" as the operating system and then choose the sd card as the "storage device". before you image the card make sure that the os is setup to connect to the network you want it connected to for your setup. all programming from here on out wil be done over ssh so setup either ssh through usrname and password or setup some keys for a more secure setup. image this onto the sd card and when complete plug this into the rpi and power it up.

run the following command to connect to rpi through ssh. when prompted, allow ssh and put in the password for the rpi. 
```
"ssh user_name@rpi.local"
```

#### pull techtree project from git
```
sudo apt update
sudo apt install git -y
git --version
git clone https://github.com/codeginge/projects.git
```


#### remove/wipe previous postgresql instance
```
sudo systemctl stop postgresql
sudo apt purge postgresql* -y
sudo apt autoremove -y
sudo rm -rf /var/lib/postgresql/
sudo rm -rf /etc/postgresql/
sudo rm -rf /var/log/postgresql/
```

#### install and setup postgreSQL database and user
now that the rpi is up and running and you are connected through ssh run these command to setup the postgreSQL database we will be using in this case.

```
sudo apt update && sudo apt upgrade -y
sudo apt install postgresql -y
sudo systemctl start postgresql
sudo systemctl enable postgresql
```
run this command to check that the dabase has been built
```
sudo systemctl status postgresql
```
switch to postgresql user and open postgres shell to create the database and database user
```
sudo -i -u postgres
psql
CREATE DATABASE techdb;
CREATE USER techuser WITH ENCRYPTED PASSWORD 'your_secure_password';
\q
```
login to techtreedb using postgres user and grant perms to techtreeuser
```
psql -U postgres -d techtreedb
```
add permissions to techuser in techdb
```
GRANT CONNECT, CREATE ON DATABASE techdb TO techuser;
GRANT USAGE, CREATE ON SCHEMA public TO techuser;
GRANT ALL PRIVILEGES ON SCHEMA public TO techuser;
GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO techuser;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO techuser;
ALTER ROLE techuser WITH LOGIN;
ALTER USER techuser CREATEDB;
```

#### make database accessable locally to techuser
add the following line at the end of this file /etc/postgresql/15/main/pg_hba.conf
```
local   all             all                                     md5
```
restart postgresql
```
sudo systemctl restart postgresql
```
to make sue it is working try accessing the techdb using the techuser 
```
psql -U techuser -d techdb
```
if it works you should see something like this
```
psql (15.12 (Debian 15.12-0+deb12u2))
Type "help" for help.

techdb=>
```
use this command to exit the database
```
\q 
```

#### setup python environment on rpi
run the following command to make rpi4_setup.sh executable and then run it to install python venv
```
chmod +x rpi4_setup.sh
./rpi4_setup.sh
```


## run server
```
source myenv/bin/activate 
```

## formats

### JSON Data Structure
```json
{
  "LMS": {
    "learning_targets": [
      {
        "name": "",
        "type": "",
        "sub_type": "",
        "learning_target_id": "LT001",
        "dependency": [],
        "learning_target_link": "link_here"
      },
      {
        "name": "",
        "type": "",
        "sub_type": "",
        "learning_target_id": "LT002",
        "dependency": ["LT001"],
        "learning_target_link": "link_here"
      }
    ],
    "skills": [
      {
        "skill_name": "exacto blades and box cutters",
        "type": "tool",
        "sub_type": "cutting",
        "core": true,
        "skill_id": "TOO001",
        "dependency": [],
        "skill_link": "link_here_01"
      },
      {
        "skill_name": "foam board construction",
        "type": "assembly",
        "sub_type": "sheet material",
        "core": true,
        "skill_id": "ASS001",
        "dependency": ["TOO001"],
        "skill_link": "link_here_02"
      }
    ],
    "projects": [
      {
        "project_name": "build a perfect 1 liter cube",
        "skills_required": ["TOO001", "ASS001"],
        "project_id": "P001",
        "dependency": [],
        "project_link": "link_here",
        "materials": ["M001", "M002", "M003"]
      },
      {
        "project_name": "construct a model RV in foam board",
        "skills_required": ["TOO001", "ASS001"],
        "project_id": "P002",
        "dependency": ["P001"],
        "project_link": "link_here",
        "materials": ["M001", "M002", "M003"]
      }
    ],
    "contracts": [
      {
        "contract_name": "foam core glider",
        "skills_required": ["TOO001", "ASS001"],
        "contract_id": "C001",
        "dependency": [],
        "contract_link": "link_here",
        "materials": ["M001", "M002", "M003"],
        "measured_variables": [
        	{
        		"name":"distance",
        		"variabele":"D",
        		"description":"distance travelled from start position in a straight line",
        		"units":"inches",
        		"value":4
        	},
        	{
        		"name":"time in air",
        		"variabele":"t",
        		"description":"time that the glider is in the air for",
        		"units":"seconds",
        		"value":30
        	}
        ]
      },
      {
        "contract_name": "foam core scale model of Eiffel Tower",
        "skills_required": ["TOO001", "ASS001"],
        "contract_id": "C002",
        "dependency": [],
        "contract_link": "link_here",
        "materials": ["M001", "M002", "M003"]
      }
    ],
    "students": [
      {
        "name": "student_01",
        "skills": [
          {
            "skill_id": "TOO001",
            "levels": [
              { "level": 1, "knowledge": false, "application": false },
              { "level": 2, "knowledge": false, "application": false }
            ],
            "comments": [
              { "date": "MMDDYYYY", "text": "liked this project because..." },
              { "date": "MMDDYYYY", "text": "failed this project because..." }
            ]
          }
        ],
        "projects": [
          {
            "project_id": "P001",
            "levels": [
              { "level": 1, "knowledge": false, "application": false, "engagement": false, "reflection": false },
              { "level": 2, "knowledge": false, "application": false, "engagement": false, "reflection": false },
              { "level": 3, "knowledge": false, "application": false, "engagement": false, "reflection": false },
              { "level": 4, "knowledge": false, "application": false, "engagement": false, "reflection": false }
            ],
            "comments": [
              { "date": "MMDDYYYY", "text": "liked this project because.." },
              { "date": "MMDDYYYY", "text": "failed this project because..." }
            ]
          }
        ],
        "contracts": [
          {
            "contract_id": "C001",
            "levels": [
              { "level": 1, "knowledge": false, "application": false, "engagement": false, "reflection": false },
              { "level": 2, "knowledge": false, "application": false, "engagement": false, "reflection": false },
              { "level": 3, "knowledge": false, "application": false, "engagement": false, "reflection": false },
              { "level": 4, "knowledge": false, "application": false, "engagement": false, "reflection": false }
            ],
            "comments": [
              { "date": "MMDDYYYY", "text": "liked this contract because..." },
              { "date": "MMDDYYYY", "text": "struggled with this contract because..." }
            ]
          }
        ],
        "materials_used": [
          { "material_id": "M001", "material_use": 3 },
          { "material_id": "M002", "material_use": 1 },
          { "material_id": "M003", "material_use": 0 }
        ]
      }
    ]
  },
  "IMS": {
    "materials": [
      {
        "name": "exacto knife",
        "type": "tool",
        "sub_type": "cutting",
        "fabricated": false,
        "amz_link": "",
        "stl_link": "",
        "price": 9.00,
        "count": 10,
        "unit_measure": "handle",
        "unit_cost": 0.90,
        "material_id": "M001",
        "sop_link": "",
        "storage_type": "small parts",
        "storage_location": "ENG",
        "labelled": true,
        "current_inventory": 7,
        "desired_inventory": 20
      }
    ],
    "orders": [
      {
        "name": "",
        "type": "",
        "cost": "",
        "materials": [
          { "material_id": "M002", "count": 10 },
          { "material_id": "M001", "count": 14 }
        ],
        "reimbursement_form_link": ""
      }
    ]
  }
}


```
# V1 
this project aims to 
-create a techTree from a google sheet to give a flow chart visualization of learning for any subject
-simplify resouce creation and linking to each technology
-show tracking through individualized techTree visualizations
-track material use to help with inventory management

# use case
## 1-create google sheet
-teacher creates new google sheet labeled "techs"
-teacher creates list of technologies to learn 
  -name
  -type
  -sub_type

## 2-build technologies
-program generates tech_ids for each tech
-program generates unlinked flow chart

## 3-add dependencies
-teacher links tech_ids using the dependency column

## 4-build technologies
-program generates linked flow chart based on dependencies

## (REPEAT 3 & 4 until all techs are linked)

## add resource docs and link
-teacher clicks build resources
-program generates resources sheet
  -preloaded with links to docs created
  -docs follow doc_link_template structure

## build out resources 
-teacher adds cirriculum to resource document template
-teacher adds projects to resource document that prove competence
-teacher adds point values for each project in project_points column

## build projects
-teacher clicks build projects
-code runs and generates techTree_projects.json from project_points info in techTree_techs.json
-updates projects list in related tech_id in techTree_techs.json

## build out materials
-teacher adds materials to materials sheet

## connect materials to projects
-teacher clicks "Update Materials" button
-code generates materials ids for added materials and updates techTree_materials.json
-teacher goes to tech flowchart, clicks node, inside details goes to projects, clicks a project 
	to get project_details, clicks "+" next to materials, adds material from drop down list and sets 
	materials_count, clicks save and material_id and material__count added to materials list inside 
	project in techTree_projects.json

## build progression
-teacher adds student names and class to "progress" sheet
-program generates techTree_progress.json

# user actions
## buildResources
## buildTechnologies
## buildProgression

# DATA
## google sheets (human readable data sets):
### teacher created
techs 
|--"name"--|--"type"--|--"sub_type"--|--"core"--|--"id"--|--"dependency"--|--"notes"--|

### code created
progress 
|--"name"--|--"class"--|--"core"--|--core+"--|--"non_core"--|--"non_core+"--|

## templates
### doc template
-title: type_sub_type
-subtitle: name_id
-tech overview
-links resources (internal or external)
-projects to show master
-rubric for each project


## JSON files
### techTree_techs.json
```
[
	{
		"name":"Light - LED", 
		"type":"actuators", 
        "sub_type":"light", 
        "core":true, 
		"tech_id":"ACT001", 
		"dependency":["c1_01","c1_02","c1_03"],
		"tech_link": "link_here_01",
	},
	{
		"name":"Light - LED", 
		"type":"actuators", 
        "sub_type":"light", 
        "core":true, 
		"tech_id":"ACT002", 
		"dependency":["c1_01","c1_02","c1_03"],
		"tech_link": "link_here_01",
	}
]
```

### techTree_projects.json
```
[
	{
		"name":"light up LED",
		"techs_required": ["ACT002","ACT006",...],
		"project_id:":"P001",
		"dependency":[],
		"project_link":"link_here"
		"materials": [
			{
			"material_id":"M001",
			"material_use": 3
			},
			{
			"material_id":"M002",
			"material_use": 1
			},
			{
			"material_id":"M003",
			"material_use": 0
			}
		]
	},
	{
		"project_id:":"P002",
		"dependency":["P001"],
		...
	},
	...
]
```

### techTree_contracts.json
```
[
	{
		"name":"light up LED",
		"techs_required": ["ACT002","ACT006",...],
		"contract_id:":"P001",
		"dependency":[],
		"contract_link":"link_here"
		"materials": [
			{
			"material_id":"M001",
			"material_use": 3
			},
			{
			"material_id":"M002",
			"material_use": 1
			},
			{
			"material_id":"M003",
			"material_use": 0
			}
		]
	},
	{
		"project_id:":"P002",
		"dependency":["P001"],
		...
	},
	...
]
```

### techTre_materials.json
```
[
	{
		"name":"exacto knife",
		"type":"tool",
		"sub_type":"cutting",
		"fabricated":False,
		"amz_link":"",
		"stl_link":"",
		"price":9.00,
		"count":10,
		"unit_measure":"handle"
		"unit_cost":0.90,
		"material_id":"M001",
		"sop_link":"",
		"storage_type":"small parts",
		"storage_location":"ENG",
		"labelled":True,
		"current_inventory":7,
		"desired_inventory":20,

	},
	{
		"name":"exacto blade",
		...
	}
]
```

### techTree_progress.json
```
{
    "students": [
        {
            "name": "student_01",
            "techs": [
                {
                	"tech_id:":"ACT001",
                	"levels": [
			        	{
			        		"level":1,
			        		"knowledge":False,
			        		"application":False,
			        	},
			        	{
			        		"level":2,
			        		"knowledge":False,
			        		"application":False,
			        	},
			        	{
			        		"level":3,
			        		"knowledge":False,
			        		"application":False,
			        	},
			        	{
			        		"level":4,
			        		"knowledge":False,
			        		"application":False,
			        	}
        			]
                },
                {
                	"tech_id:":"ACT002",
                	"levels": [
			        	{
			        		"level":1,
			        		"knowledge":False,
			        		"application":False,
			        	},
			        	{
			        		"level":2,
			        		"knowledge":False,
			        		"application":False,
			        	},
			        	{
			        		"level":3,
			        		"knowledge":False,
			        		"application":False,
			        	},
			        	{
			        		"level":4,
			        		"knowledge":False,
			        		"application":False,
			        	}
        			]
                },
                ...
        	],
        	"projects": [
	        	{
	        		"project_id":"P001",
    				"levels":[
			        	{
			        		"level":1,
			        		"knowledge":False,
			        		"application":False,
			        		"engagement":False,
			        		"reflection":False
			        	},
			        	{
			        		"level":2,
			        		"knowledge":False,
			        		"application":False,
			        		"engagement":False,
			        		"reflection":False
			        	},
			        	{
			        		"level":3,
			        		"knowledge":False,
			        		"application":False,
			        		"engagement":False,
			        		"reflection":False
			        	},
			        	{
			        		"level":4,
			        		"knowledge":False,
			        		"application":False,
			        		"engagement":False,
			        		"reflection":False,
			        	}
        			]
	        	},
	        	{
	        		"project_id":"P002",
	        	}
	        ],
			"materials": [
				{
				"material_id":"M001",
				"material_use": 3
				},
				{
				"material_id":"M002",
				"material_use": 1
				},
				{
				"material_id":"M003",
				"material_use": 0
				}
			]
        },
        {
            "name": "student_02",
            ...
        }
    ]
}
```

# FOR LATER DEVELOPEMENT
### techTree_kits.json
```
[
	{
		"kit_id":"K001",
		"name":"thermister sensor",
		"current_inventory":2,
		"desired_inventory":5,
		"materials": [
			{
			"material_id":"M001",
			"count": 3
			},
			{
			"material_id":"M002",
			"count": 1
			},
			{
			"material_id":"M003",
			"count": 10
			}
		]
	},
	{
		"kit_id":"K002",
		...
	}
]
```

### techTree_contracts.json
```
[
	{
		"contract_id":"C001",
		"name":"thermister sensor",
		"current_inventory":2,
		"desired_inventory":5,
		"materials": [
			{
			"material_id":"M001",
			"count": 3
			},
			{
			"material_id":"M002",
			"count": 1
			},
			{
			"material_id":"M003",
			"count": 10
			}
		]
	},
	{
		"kit_id":"K002",
		...
	}
]
```



