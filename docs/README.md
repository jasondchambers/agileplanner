### Agile Planner

For some projects, you can get by with just enough planning and you leave the door open for making adjustments as you execute the plan. Adjustments are in the form of flexing either or both the schedule and scope. For other projects, you might be faced with strict deadlines forcing you to fix the dates. This at least gives you some wiggle room to flex the scope as you execute the plan. 

The most challenging types of projects are where the dates are fixed, and the scope has been reduced to the bare bones. There is no margin for error. To execute these kinds of projects successfully, requires significant planning discipline. These tools were developed out of necessity when the author was faced with
such a situation. 

The tools enable capacity to be determined for the team for a given planning time period.

In addition, scheduling tools are provided that take into account, the type of work (epic) matching the skillset of the team. The start date and end date for an epic (if the work fits) is calculated and can be subsequently plugged into your tool of choice (e.g. Jira). As the project progresses, you can easily determine if the project is off-track if epics are not starting or finishing on time. These indicators do not replace any metrics you might have in place at the sprint level. They can be used in addition to get a sense of whether the project is on-track or not.

Be sure to checkout the [cookbook](https://github.com/jasondchambers/agileplanner-cookbook) to learn how to use Agile Planner.

## Capacity estimation tools

- How much QE capacity do we have for a given time period? (e.g. remaining for the quarter, Q2, Q3)
- How much front end capacity do we have for a given time period for a specific team?
- How much total back end capacity do we have for the entire org for Q2?
- What is the estimated capacity for a team's sprint?

All it requires is that we have details of each team and person on that team to be captured in a YAML.

```yaml
team:
  name: SoftServe for Ed
  persons:
  - name: Billy Ted
    start_date: '2023-09-13'
    end_date: '2030-12-31'
    front_end: False
    back_end: False
    qe: False
    devops: True
    documentation: False
    reserve_capacity: 0.35
    location: Ukraine
    out_of_office_dates:
    - '2023-10-03'
    - '2023-10-04'
    - '2023-10-05'
    - '2023-10-06'
    - '2023-10-09'
    - '2023-10-10'
```

Given this, we can generate a capacity spreadsheet (CSV) broken down by person and by day for each person on the team for any time period.

You can easily combine teams together enabling capacity to be calculated for an entire organization.

A pandas DataFrame can easily be created from the team capacity, enabling querying and exploring of the available capacity. For example, you might want to query how much capacity you have for QE or Documentation.

## Epic scheduling tools

Once we have capacity calculated, it opens up the possibility to perform basic epic scheduling.

Sample use cases:

- Given capacity and epic rough sizes, what is the estimated epic start date? end date? - so that we can determine if we are on-track or not
- Will the epics allocated to a team fit in the specified time period (e.g. Q2)?

To support this simple details about the epics are required in YAML as follows:

```yaml
features:
- key: CSESC-52
  epics:
  - key: CSESC-1022
    estimated_size: 171
    epic_type: FRONTEND
  - key: CSESC-1023
    estimated_size: 50
    epic_type: BACKEND
```

Each epic can be of the following type:

- FRONTEND 
- BACKEND 
- QE 
- DEVOPS 
- DOCUMENTATION 

Epics that are of mixed types are not supported at this time. I need to figure out what that might look like.

Here's an example of basic scheduling. We have a short time-period of 4 days. Notice how there 10/22 is a weekend and so there is zero capacity. There are no US holidays detected in the time-period and the people on the team do not have any planned PTO. The team of 3 is available for the entire time-period. We use a classic ideal hours calculation of 6 hours per day (6/8 = 0.25). This allows time for the team ceremonies, PRs etc.

We load the team with 4 epics each with a size of 2 points each. The scheduler forecasts the start date and the edn date for each epic. Notice how the
scheduler notifies that the final epic CSESC-1974 is not forecast to complete within the time period.

```
           Team Person Location  Start Date    End Date Front End Back End QE DevOps Reserve Capacity  2023-10-22  2023-10-23  2023-10-24  2023-10-25  Total
0  Provisioners  Alice       US  2023-01-01  2030-12-31         T        F  F      F             0.25           0        0.75        0.75        0.75   2.25
1  Provisioners    Sue       US  2023-01-01  2030-12-31         T        F  F      F             0.25           0        0.75        0.75        0.75   2.25
2  Provisioners    Bob       US  2023-01-01  2030-12-31         T        F  F      F             0.25           0        0.75        0.75        0.75   2.25
3  Provisioners  Total        -           -           -         -        -  -      -                -           0        2.25        2.25        2.25   6.75
CSESC-1971 sized 2 starts on 2023-10-23 and is scheduled to complete on 2023-10-23 with 0 points remaining
CSESC-1972 sized 2 starts on 2023-10-23 and is scheduled to complete on 2023-10-24 with 0 points remaining
CSESC-1973 sized 2 starts on 2023-10-24 and is scheduled to complete on 2023-10-25 with 0 points remaining
CSESC-1974 sized 2 starts on 2023-10-25 and is scheduled to complete on WILL NOT COMPLETE IN TIME with 1.25 points remaining 
```

