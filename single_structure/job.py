from jarvis.tasks.vasp.vasp import VaspJob
from jarvis.db.jsonutils import loadjson
d=loadjson("job.json")
v=VaspJob.from_dict(d)
v.runjob()
