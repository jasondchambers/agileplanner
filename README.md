### Agile Planner

For some projects, you can get by with just enough planning and you leave the door open for making adjustments as you execute the plan. Adjustments are in the form of flexing either or both the schedule and scope. For other projects, you might be faced with strict deadlines forcing you to fix the dates. This at least gives you some wiggle room to flex the scope as you execute the plan. 

The most challenging types of projects are where the dates are fixed, and the scope has been reduced to the bare bones. There is no margin for error. To execute these kinds of projects successfully, requires significant planning discipline. These tools were developed out of necessity when the author was faced with
such a situation. 

The tools enable capacity to be determined for the team for a given planning time period.

In addition, scheduling tools are provided that take into account, the type of work (epic) matching the skillset of the team. The start date and end date for an epic (if the work fits) is calculated and can be subsequently plugged into your tool of choice (e.g. Jira). As the project progresses, you can easily determine if the project is off-track if epics are not starting or finishing on time. These indicators do not replace any metrics you might have in place at the sprint level. They can be used in addition to get a sense of whether the project is on-track or not.

For more details, refer to the README.md contained in the package itself.

## Building
The tools are built into a Python package as follows:

```
$ python setup.py bdist_wheel
```

The build can be cleaned up as follows:

```
$ python3 setup.py clean --all
```

Agile Planner is not ready yet to be published to PyPi. There is still much work to be done. However, once built you can install locally as follows (using a different conda environment) where location is the directory where you cloned this repo:

```
$ pip install --force-reinstall <location>/dist/agileplanner-0.0.1-py3-none-any.whl
```

Then, to use in your own code, simply to get started.

```
import agileplanner as ap 
```

Example code can be found in the repo aptest (details to be provided).

