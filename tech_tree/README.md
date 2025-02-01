this project aims to 
-create a techTree from a google sheet to give a flow chart visualization of learning for any subject
-simplify resouce creation and linking to each technology
-show tracking through individualized techTree visualizations

### use case
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


### google sheets (human readable data sets):
## teacher created
techs 
|--name--|--type--|--sub_type--|--core--|--id--|--dependency--|--notes--|

## code created
resources 
|--name--|--id--|--doc_link--|--project_point_values--|--points_required--|--core--|

progress 
|--student--|--points--|--id_01_p_01--|--id_02--|--id_03--|--...--|


### teacher actions

## createEnvironment 
-pull techTree google sheet
-build techTree_topic_techs.json
-create techTree_topic.png visualization
-create resource sheet
-create progress sheet

## createClass
-pull resource sheet
-create techTree_topic_resource.json
-pull progress sheet
-create techTree_topic_progress.json
-create techTree_topic_student.png for each student
-create techTree_topic_class.png for the whole class

## update
-pull techTree google sheet
-update techTree_topic.json 
-update techTree_topic.png visualization
-update resource sheet
-update techTree_topic_resource.json
-update progress sheet
-update techTree_topic_progress.json


### doc template
-title: type_sub_type
-subtitle: name_id
-tech overview
-links resources (internal or external)
-projects to show master
-rubric for each project


### json files (program readable data sets)
techTree_techs.json
[
	{
		"name":"Light - LED", 
		"type":"actuators", 
        "sub_type":"light", 
        "core":true, 
		"id":"ACT001", 
		"dependency":["c1_01","c1_02","c1_03"],
		"notes":"Basic light-emitting diode for signaling or lighting in various colors."
	},
	{
		"name":"Light - LED", 
		"type":"actuators", 
        "sub_type":"light", 
        "core":true, 
		"id":"ACT002", 
		"dependency":["c1_01","c1_02","c1_03"],
		"notes":"Basic light-emitting diode for signaling or lighting in various colors."
	}
]

techTree_resources.json
[
    {
        "name": "tech_01", 
        "id": "ACT001", 
        "doc_link": "link_here_01",
        "project_point_values": [7, 8, 9], 
        "points_required": 5,
        "core": true
    },
    {
        "name": "tech_02", 
        "id": "ACT001", 
        "doc_link": "link_here_02",
        "project_point_values": [9, 2, 3], 
        "points_required": 7,
        "core": false
    }
]


techTree_progress.json
{
    "students": [
        {
            "name": "student_01",
            "technologies": [
                {
                    "id": "ACT001",
                    "type": "circuits",
                    "sub_type": "amps",
                    "projects": [
                        {"project_id": "id_01_p_01", "points_aquired": 1},
                        {"project_id": "id_01_p_02", "points_aquired": 2}
                    ],
                    "points_required": 2,
                    "points_avaliable": 4
                },
                {
                    "id": "ACT002",
                    "type": "circuits",
                    "sub_type": "amps",
                    "projects": [
                        {"project_id": "id_02_p_01", "points_aquired": 3}
                    ],
                    "points_required": 2,
                    "points_avaliable": 4
                }
            ]
        },
        {
            "name": "student_02",
            "technologies": [
                {
                    "id": "ACT001",
                    "type": "circuits",
                    "sub_type": "amps",
                    "projects": [
                        {"project_id": "id_03_p_01", "points_aquired": 4},
                        {"project_id": "id_03_p_02", "points_aquired": 5}
                    ],
                    "points_required": 2,
                    "points_avaliable": 4
                }
            ]
        }
    ]
}


