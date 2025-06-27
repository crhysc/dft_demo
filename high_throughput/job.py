import os
ids = []
poscars = os.listdir('./POSCARs')
for num, file in enumerate(poscars):
    ids.append(f"./POSCARs/{file}")

from jarvis.tasks.vasp.vasp import (
    JobFactory,
    VaspJob,
    GenericIncars,
    write_jobfact,
)
from jarvis.io.vasp.inputs import Potcar, Incar, Poscar
from jarvis.db.jsonutils import dumpjson
from jarvis.db.figshare import data
from jarvis.core.atoms import Atoms
from jarvis.tasks.queue_jobs import Queue
import os
vasp_cmd = "mpirun vasp_std"
copy_files = ["/users/crc8/bin/vdw_kernel.bindat"]
#submit_cmd = ["qsub", "submit_job"]

# For slurm
 submit_cmd = ["sbatch", "submit_job"]

steps = [
    "ENCUT",
    "KPLEN",
    "RELAX",
    "BANDSTRUCT",
    "OPTICS",
    "MBJOPTICS",
    "ELASTIC",
]
incs = GenericIncars().optb88vdw().incar.to_dict()

for id in ids:
    mat = Poscar.from_file(id)
    cwd_home = os.getcwd()
    dir_name = id.split('.vasp')[0] + "_" + str("PBEBO")
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    os.chdir(dir_name)
    job = JobFactory(
        vasp_cmd=vasp_cmd,
        poscar=mat,
        steps=steps,
        copy_files=copy_files,
        use_incar_dict=incs,
    )

    dumpjson(data=job.to_dict(), filename="job_fact.json")
    write_jobfact(
        pyname="job_fact.py",
        job_json="job_fact.json",
        input_arg="v.step_flow()",
    )

    # Example job commands, need to change based on your cluster
    job_line = (
        "source activate my_jarvis \n"
        + "python job_fact.py"
    )
    name = id
    directory = os.getcwd()
    """
    Queue.pbs(
        job_line=job_line,
        jobname=name,
        #partition="",
        walltime="24:00:00",
        #account="",
        cores=12,
        directory=directory,
        submit_cmd=submit_cmd,
    )
    os.chdir(cwd_home)
    """
    # For Slurm clusters
    Queue.slurm(
        job_line=job_line,
        jobname=name,
        directory=directory,
        submit_cmd=submit_cmd,
    )
    os.chdir(cwd_home)
    
