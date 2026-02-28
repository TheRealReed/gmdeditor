# gmd_generator.py
import json
from gmdkit.models.level import Level
from gmdkit.models.object import Object
from gmdkit.mappings import obj_prop

class gmdeditor:
    def __init__(self, template_path: str):
        """
        Initialize the builder with a template GMD file.
        """
        self.template_path = template_path
        self.level = Level.from_file(template_path)
        self.level.load()
        self.objs = self.level.objects
        self.objs.clear()

    def set_metadata(
        self,
        level_id="",
        name="New Level",
        description="",
        difficulty=1,
        version=21,
        creator="Unknown",
        password="",
        downloads=0,
        likes=0,
        song_id=0,
        coins=0,
        length=0
    ):
        """
        Set the common k# headers.
        """
        self.level["k1"] = level_id
        self.level["k2"] = name
        self.level["k3"] = description
        self.level["k4"] = difficulty
        self.level["k5"] = len(self.objs)  # Will update after adding objects
        self.level["k6"] = version
        self.level["k7"] = creator
        self.level["k8"] = password
        self.level["k9"] = downloads
        self.level["k10"] = likes
        self.level["k11"] = song_id
        self.level["k12"] = ""  # Will rebuild from objects automatically
        self.level["k13"] = coins
        self.level["k14"] = length

    def add_object(self, obj_id: int, x: float, y: float, **extra):
        """
        Add an object to the level.
        """
        o = Object.default(obj_id)
        o[obj_prop.X] = float(x)
        o[obj_prop.Y] = float(y)
        for k, v in extra.items():
            o[k] = v
        self.objs.append(o)

    def add_player_start(self, x=0, y=30):
        """
        Add the default player start object (31).
        """
        self.add_object(31, x, y)

    def add_from_json(self, json_path: str, max_objects=None):
        """
        Load object data from a JSON file.
        Each item should have 'obj_id', 'x', 'y', and optional extra props.
        """
        with open(json_path) as f:
            data = json.load(f)

        for i, item in enumerate(data):
            if max_objects and i >= max_objects:
                break
            self.add_object(
                item.get("obj_id", i),
                item.get("x", 0),
                item.get("y", 0),
                **item.get("extra", {})
            )

    def build(self, out_path: str):
        """
        Finalize level headers and export to GMD.
        """
        self.level["k5"] = len(self.objs)  # Update object count
        self.level.to_file(out_path)