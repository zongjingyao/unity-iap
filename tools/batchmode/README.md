# BatchMode

A tool to build IAPDemo project in batchmode.

## Requirements

* Python3
* Unity

## Usage

Copy `BuildTools.cs` to `Assets/Editor/` of your Unity project.  
Make a copy of `config.json.template` and rename it to `config.json`.  
Fill in the config file depending on your needs.  
You can override values of `default` in a certain project, like:

```json
{
    "default": {
        "unityPath": "",
        "keyaliasName": "dog",
        "projectPath": "project A"
    },
    "projects": [{
        "keyaliasName": "cat",
        "projectPath": "project B"
    }
    ...
    ]
}
```

Then run `batchmode.py`.