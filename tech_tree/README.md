# V2 JSON Data Structure
```json
{
	"LMS": [
		"learning_targets":[
		],
		"skills": [
			{
				"skill_name":"exacto blades and box cutters", 
				"type":"tool", 
		        "sub_type":"cutting", 
		        "core":true, 
				"skill_id":"TOO001", 
				"dependency":[],
				"skill_link": "link_here_01",
			},
			{
				"name":"foam board construction", 
				"type":"assembly", 
		        "sub_type":"sheet material", 
		        "core":true, 
				"skill_id":"ASS001", 
				"dependency":["TOO001"],
				"skill_link": "link_here_01",
			}	
		],
		"projects": [
			{
				"project_name":"build a perfect 1 liter cube",
				"skills_required": ["TOO01","ASS001"],
				"project_id:":"P001",
				"dependency":[],
				"project_link":"link_here",
				"materials": ["M001", "M002", "M003"]
			},
			{
				"project_name":"construct a model RV in foam board",
				"skills_required": ["TOO01","ASS001"],
				"project_id:":"P002",
				"dependency":["P001"],
				"project_link":"link_here",
				"materials": ["M001", "M002", "M003"]
				...
			},
			...
		],
		"contracts": [
			{
				"contract_name":"foam core glider",
				"skills_required": ["TOO001","ASS001",...],
				"contract_id:":"C001",
				"dependency":[],
				"contract_link":"link_here"
				"materials": ["M001", "M002", "M003"]
			},
			{
				"contract_name":"foam core scale model of Eifel tower",
				"skills_required": ["TOO001","ASS001",...],
				"contract_id:":"C002",
				"dependency":[],
				"contract_link":"link_here"
				"materials": ["M001", "M002", "M003"]
			},
			...
		],
		"students":[
		!!!!!!ADDTHINGSHEREHREHREHR!!!!!!!
		]
	],
	"IMS":[
		"materials": [
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
		"orders": [
		]
	]
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



