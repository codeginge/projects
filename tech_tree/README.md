this project aims to 
-create a techTree from a google sheet to give a flow chart visualization of learning for any subject
-simplify resouce creation and linking to each technology
-show tracking through individualized techTree visualizations

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

## build resources
-program generates resources sheet
  -preloaded with links to docs created
  -docs follow doc_link_template structure

## build progression
-program generates 

# user actions
## buildResources
## buildTechnologies
## buildProgression

# DATA
## google sheets (human readable data sets):
### teacher created
techs 
|--name--|--type--|--sub_type--|--core--|--id--|--dependency--|--notes--|

### code created
progress 
|--student--|--points--|--id_01_p_01--|--id_02--|--id_03--|--...--|

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
		"doc_link": "link_here_01",
        "project_point_values": [3, 3, 3], 
        "points_required": 6
	},
	{
		"name":"Light - LED", 
		"type":"actuators", 
        "sub_type":"light", 
        "core":true, 
		"tech_id":"ACT002", 
		"dependency":["c1_01","c1_02","c1_03"],
		"doc_link": "link_here_01",
        "project_point_values": [3, 3, 3], 
        "points_required": 5
	}
]
```

### techTree_progress.json
```
{
    "students": [
        {
            "name": "student_01",
            "projects": [
                {
                	"project_id:":"P001",
                	"points_aquired": 5
                },
                {
                	"project_id:":"P002",
                	"points_aquired": 4
                },
                                {
                	"project_id:":"P003",
                	"points_aquired": 7
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

### techTree_projects.json
```
[
	{
		"project_id:":"P001",
		"tech_id":"ACT001",
		"points_avaliable":3,
		"materials": [
			{
			"material_id":"M001",
			"material_count": 3
			},
			{
			"material_id":"M002",
			"material_count": 1
			},
			{
			"material_id":"M003",
			"material_count": 10
			}
		]
	},
	{
		...
	}
]
```

### techTre_materials.json
```
[
	{
		"material_id":"M001",
		"name":"",
		"link":"",
		"type":"",
		"sub_type":"",
		"fabricated":False,
		"order_price":5.00,
		"order_count":7,
		"current_inventory":12,
		"desired_inventory":20,
		"unit_measure":""
	},
	{
		"material_id":"M002",
		...
	}
]
```

### techTree_kits.json
```
[
	{
		"kit_id":"K001",
		"kit_name":"thermister sensor",
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




