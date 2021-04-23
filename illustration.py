import operator
import matplotlib.pyplot as plt

inp = 6
max_iterations = inp
max_sum_goals = 4
max_goal_difference = inp

pn = 0.90
ph = 0.05
pa = max(1 - pn - ph, 0)

ddy = 0.046 * 0.2
ex = 0.11
w = 0.2

cmap = plt.get_cmap('viridis')
figname = "Figure_5"
figsize = (16, 9)
ylim = [-4.2, 4.2]
xlim = [0, inp+1]

def straight(point, i):
    diff = point["home_goals"] - point["away_goals"]
    i_gdiff = i + 1 + diff
    x0 = point["x"]
    y0 = point["y"]
    x1 = x0 + 1
    y1 = y0
    p = point["p"] * pn
    plt.plot([x0, x1], [y0, y1], c=cmap(p**ex), linewidth = w)
    points[i + 1].append({"home_goals": point["home_goals"], "away_goals": point["away_goals"], "x": x1, "y": y1, "p": p})
    if y0 % 1 == 0:
        goal_differences[i + 1][i_gdiff]["n"] += 1
    elif y0 % 1 < 0.5:
        goal_differences[i + 1][i_gdiff]["n_above"] += 1
    elif y0 % 1 > 0.5:
        goal_differences[i + 1][i_gdiff]["n_below"] += 1
    
def up(point, i):
    diff = point["home_goals"] - point["away_goals"] + 1
    i_gdiff = i + 1 + diff
    if goal_differences[i + 1][i_gdiff]["n"] == 0:
        goal_differences[i + 1][i_gdiff]["n"] = 1
        dy = 0
    else:
        goal_differences[i + 1][i_gdiff]["n_below"] += 1
        dy = -ddy * goal_differences[i + 1][i_gdiff]["n_below"]
    x0 = point["x"]
    y0 = point["y"]
    x1 = x0 + 1
    y1 = diff + dy
    p = point["p"] * ph
    plt.plot([x0, x1], [y0, y1], c=cmap(p**ex), linewidth = w)
    points[i + 1].append({"home_goals": point["home_goals"] + 1, "away_goals": point["away_goals"], "x": x1, "y": y1, "p": p})
    
def down(point, i):
    diff = point["home_goals"] - point["away_goals"] - 1
    i_gdiff = i + 1 + diff
    if goal_differences[i + 1][i_gdiff]["n"] == 0:
        goal_differences[i + 1][i_gdiff]["n"] = 1
        dy = 0
    else:
        goal_differences[i + 1][i_gdiff]["n_above"] += 1
        dy = +ddy * goal_differences[i + 1][i_gdiff]["n_above"]
    x0 = point["x"]
    y0 = point["y"]
    x1 = x0 + 1
    y1 = diff + dy
    p = point["p"] * pa
    plt.plot([x0, x1], [y0, y1], c=cmap(p**ex), linewidth = w)
    points[i + 1].append({"home_goals": point["home_goals"], "away_goals": point["away_goals"] + 1, "x": x1, "y": y1, "p": p})

goal_differences = [[[{"n_above": 0, "n_below": 0, "n": 1}]]]
points = [[{"home_goals": 0, "away_goals": 0, "x": 0, "y": 0, "p": 1}]]
plt.figure(figsize=figsize)
for i in range(max_iterations + 1):
    points.append(int(3**(i + 1)) * [])
    j = min(i, max_sum_goals)
    
    goal_differences.append([{"n_above": 0, "n_below": 0, "n": 0} for k in range(2 * (i + 1) + 1)])
    for point in points[i]:
        straight(point, i)
    for point in points[i]:
        sum_goals = point["home_goals"] + point["away_goals"]
        goal_difference = point["home_goals"] - point["away_goals"]
        if goal_difference + 1 <= max_goal_difference and sum_goals + 1 <= max_sum_goals and i < max_iterations:
            up(point, i)
    for point in reversed(points[i]):
        sum_goals = point["home_goals"] + point["away_goals"]
        goal_difference = point["home_goals"] - point["away_goals"]
        if -goal_difference + 1 <= max_goal_difference and sum_goals + 1 <= max_sum_goals  and i < max_iterations:
            down(point, i)
    points[i + 1] = sorted(points[i + 1], key=operator.itemgetter('y'), reverse=True)
plt.ylim(ylim)
plt.xlim(xlim)
plt.savefig(figname)
plt.savefig(figname+".pdf", format="pdf")
plt.show()