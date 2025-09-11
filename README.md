# projects

When adding a project, follow this organizational structure:
```
/project_name
  ├── README.md
  ├── code/
  │     ├── run.py
  ├── design/                 
  │     ├── part1.stl
  │     ├── part2.dxf
  ├── docs/
  │     ├── instructions.pdf
  │     ├── overview.md
  └── other/
        ├── data.csv
        ├── design.png
```

For coding projects in python, always create a venv using:
```
python3 -m venv environment_name
source environment_name/bin/activate 
```