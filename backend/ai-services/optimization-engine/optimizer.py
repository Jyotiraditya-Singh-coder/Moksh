from ortools.linear_solver import pywraplp
import numpy as np

def optimize_study_plan(weak_topics, strong_topics, available_hours, difficulty_pref, dropout_risk, career_goal):
    # Combine topics with gain
    all_topics = weak_topics + strong_topics
    topic_names = [t[0] for t in all_topics]
    gains = [t[1] for t in all_topics]

    solver = pywraplp.Solver.CreateSolver('GLOP')
    if not solver:
        return None

    x = [solver.NumVar(0, available_hours, f'hours_{i}') for i in range(len(topic_names))]

    objective = solver.Objective()
    for i, gain in enumerate(gains):
        objective.SetCoefficient(x[i], gain)
    objective.SetMaximization()

    # Total hours constraint
    solver.Add(sum(x) <= available_hours)

    # Max 3 hours per topic
    for i in range(len(topic_names)):
        solver.Add(x[i] <= 3)

    # If dropout risk high, allocate at least 1 hour to weak topics
    if dropout_risk > 0.7 and weak_topics:
        weak_indices = [i for i, t in enumerate(all_topics) if t in weak_topics]
        if weak_indices:
            solver.Add(sum(x[i] for i in weak_indices) >= 1)

    status = solver.Solve()
    if status == pywraplp.Solver.OPTIMAL:
        hours = [x[i].solution_value() for i in range(len(topic_names))]
        # Build sequence sorted by gain descending
        sorted_indices = np.argsort(gains)[::-1]
        sequence = [topic_names[i] for i in sorted_indices if hours[i] > 0]
        daily_plan = []
        day = 1
        for i, h in enumerate(hours):
            if h > 0:
                daily_plan.append({"day": day, "topic": topic_names[i], "hours": round(h, 1)})
                day += 1
        return {
            "recommendedStudyHours": sum(hours),
            "optimizedTopicSequence": sequence,
            "dailyPlan": daily_plan
        }
    else:
        # Fallback: simple allocation
        hours_per_topic = available_hours / len(topic_names) if topic_names else 0
        daily_plan = []
        for i, topic in enumerate(topic_names):
            daily_plan.append({"day": i+1, "topic": topic, "hours": round(min(3, hours_per_topic), 1)})
        return {
            "recommendedStudyHours": available_hours,
            "optimizedTopicSequence": topic_names,
            "dailyPlan": daily_plan
        }