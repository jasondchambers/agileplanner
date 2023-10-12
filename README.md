### Agile Planner

For some projects, as an Engineering Leader responsible for delivery, you can often get by with just enough planning and you leave the door open for adjusting as you execute the plan. Adjustments are in the form of flexing either or both the schedule and scope. For other projects, you might be faced with strict deadlines forcing you to fix the dates. This at least gives you some wiggle room to flex the scope as you execute the plan. 

The most challenging types of projects are where the dates are fixed, and the scope has been reduced to the bare bones. This leaves no margin for error and therefore exposes the project to significant risk. This is what is known as the [“Iron Triangle”](https://ambysoft.com/essays/brokentriangle.html). What might you do in such a situation? One option is to run. Another option is to fight it. If you do nothing, you run the real risk of having to rely on heroics to meet the dates leading to team burnout and attrition. 

There is another option. As a leader, you can take this environment as a constraint and work with it. To mitigate the risks, forces you to improve planning discipline.

These tools were conceived out of necessity when the author was faced with such a situation. 

The tools enable capacity to be determined for a team or organization, for a specific period. This is usually, but not always a quarter.

In addition, scheduling tools are provided that consider, the type of work (epic) matching the skillset of the team. The start date and end date for an epic (if the work fits) is calculated and can be subsequently plugged into your tool of choice (Jira is a popular choice). As the project progresses, you can easily determine if the project is off-track if epics are not starting or finishing on time. These indicators do not replace any metrics you might have in place at the sprint level. They can be used in addition to get a sense of whether the project is on-track or not.

For more details, refer to the [README.md](docs/README.md) contained in the package itself.

## Building
The tools are built into a Python package as follows:

```
$ python setup.py bdist_wheel
$ python setup.py sdist   
```

The build can be cleaned up as follows:

```
$ python3 setup.py clean --all
```

Once built you can install locally as follows (using a different conda environment) where location is the directory where you cloned this repo:

```
$ pip install --force-reinstall <location>/dist/agileplanner-0.0.1-py3-none-any.whl
```

Be sure to checkout the [cookbook](https://github.com/jasondchambers/agileplanner-cookbook) to learn how to use Agile Planner.

## Publishing

Agile Planner is published on the [Python Package Index](https://pypi.org) at this [location](https://pypi.org/project/agileplanner/).

Once built, a new version can be published using [twine](https://twine.readthedocs.io/en/stable/) as follows:

```
$ twine check dist/*
$ twine upload dist/*
```
