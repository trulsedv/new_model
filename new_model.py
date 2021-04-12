import time

def main():
	mean_hg = 2.94
	mean_ag = 0.63
	d = 0.00

	sum_max = 8
	n_iter = 10000

	p_hg = mean_hg / n_iter
	p_ag = mean_ag / n_iter
	dict_p = get_prob_dict(p_hg, p_ag, d)
	pretty(dict_p)

	dict_n = get_probabilities_of_results_at_n(n_iter, sum_max, dict_p)
	# pretty(dict_n)
	print_output(dict_n)

	(sum_P, sum_nZP) = calc_sums(dict_n)
	# print(sum_P)
	# print(sum_nZP/sum_P)

def get_probabilities_of_results_at_n(n_iter, sum_max, dict_p):
	beg = time.time()
	dict_nm1 = {}
	for n in range(n_iter + 1):
		dict_nm1 = probabilities_of_results_at_n(n, sum_max, dict_nm1, dict_p)
		if n % (n_iter / 10) == 0 and n != 0:
			print("Iteration {}, time {:.2f}".format(n, time.time() - beg), flush=True)
	print("Done!")
	return dict_nm1

def probabilities_of_results_at_n(n_iter, sum_max, dict_nm1, dict_p):
	if n_iter == 0:
		dict_n = {"n": n_iter, "0-0": {"hg": 0, "ag": 0, "P": 1}}
	else:
		dict_n = {"n": n_iter}
		for sum_g in range(min(n_iter, sum_max)+1):
			for hg in range(sum_g + 1):
				dict_n["{}-{}".format(hg,sum_g - hg)] = {}
				dict_n["{}-{}".format(hg,sum_g - hg)]["hg"] = hg
				dict_n["{}-{}".format(hg,sum_g - hg)]["ag"] = sum_g - hg
				P = calculate_probability_of_result(dict_p, dict_nm1, hg, sum_g - hg)
				dict_n["{}-{}".format(hg,sum_g - hg)]["P"] = P
	return dict_n

def calculate_probability_of_result(dict_p, dict_nm1, home_goals, away_goals):
	if "{}-{}".format(home_goals - 1, away_goals) in dict_nm1.keys():
		P1 = dict_nm1["{}-{}".format(home_goals - 1, away_goals)]["P"]
		if home_goals - away_goals == 1:
			P1 = P1 * dict_p["from_draw"]["p_hg"]
		elif home_goals == away_goals:
			P1 = P1 * dict_p["to_draw"]["p_hg"]
		else:
			P1 = P1 * dict_p["norm"]["p_hg"]	
	else:
		P1 = 0

	if "{}-{}".format(home_goals, away_goals - 1) in dict_nm1.keys():
		P2 = dict_nm1["{}-{}".format(home_goals, away_goals - 1)]["P"]
		if home_goals - away_goals == - 1:
			P2 = P2 * dict_p["from_draw"]["p_ag"]
		elif home_goals == away_goals:
			P2 = P2 * dict_p["to_draw"]["p_ag"]
		else:
			P2 = P2 * dict_p["norm"]["p_ag"]
	else:
		P2 = 0

	if "{}-{}".format(home_goals, away_goals) in dict_nm1.keys():
		P3 = dict_nm1["{}-{}".format(home_goals, away_goals)]["P"]
		if home_goals - away_goals == 1:
			P3 = P3 * dict_p["to_draw"]["p_ng_1h"]
		elif home_goals - away_goals == -1:
			P3 = P3 * dict_p["to_draw"]["p_ng_1a"]
		elif home_goals == away_goals:
			P3 = P3 * dict_p["from_draw"]["p_ng"]
		else:
			P3 = P3 * dict_p["norm"]["p_ng"]
	else:
		P3 = 0

	return P1 + P2 + P3

def get_prob_dict(p_hg, p_ag, d):
	p_ng = 1 - p_hg - p_ag
	dict_p = {}
	dict_p["norm"] = {		"p_hg": p_hg,
							"p_ag": p_ag,
							"p_ng": p_ng}
	p_hg_fd = p_hg * (1 - d)
	p_ag_fd = p_ag * (1 - d)
	p_ng_fd = 1 - p_hg_fd - p_ag_fd
	dict_p["from_draw"] = {	"p_hg": p_hg_fd,
							"p_ag": p_ag_fd,
							"p_ng": p_ng_fd}
	p_hg_td = p_hg * (1 + d)
	p_ag_td = p_ag * (1 + d)
	p_ng_1h = 1 - p_hg - p_ag_td
	p_ng_1a = 1 - p_hg_td - p_ag
	dict_p["to_draw"] = {	"p_hg": p_hg_td,
							"p_ag": p_ag_td,
							"p_ng_1h": p_ng_1h,
							"p_ng_1a": p_ng_1a}
	return dict_p

def calc_sums(dict_n):
	sum_P = 0
	sum_nZP = 0
	for key in dict_n.keys():
		if key == "n":
			continue
		sum_nZP = sum_nZP + (dict_n[key]["hg"] + dict_n[key]["ag"]) * dict_n[key]["P"]
		sum_P = sum_P + dict_n[key]["P"]
	return sum_P, sum_nZP

def pretty(d, indent=0):
	for key, value in d.items():
		print('\t' * indent + str(key),end="")
		if isinstance(value, dict):
			print("")
			pretty(value, indent+1)
		else:
			if isinstance(value, int):
				print('\t' + "{}".format(value))
			else:
				print('\t' + "{:.10f}".format(value))


def print_output(dict_nm1):
	for key in dict_nm1.keys():
		if key == "n":
			continue
		hg = dict_nm1[key]["hg"]
		ag = dict_nm1[key]["ag"]
		p = dict_nm1[key]["P"]
		print(hg, ag, "{:.3f}".format(p))

# def probability_of_result_recursive(home_goals, away_goals, rating_difference, n):
# 	p_hg = 0.08
# 	p_ag = p_hg
# 	d = 0
	
# 	P_Ng = 1 - p_hg - p_ag
# 	P_Hbd = p_hg - d
# 	P_Abd = p_ag - d
# 	P_Nbd = P_Ng + 2 * d
# 	P_Htd = p_hg + d
# 	P_Atd = p_ag + d
# 	P_Ntd = P_Ng - d

# 	if n == 0 and home_goals == 0 and away_goals == 0:
# 		return 1
# 	if n == 0 and (home_goals != 0 or away_goals != 0):
# 		print("fuck!")
# 		return -1

# 	if home_goals > 0:
# 		P1 = probability_of_result_recursive(home_goals - 1, away_goals, rating_difference, n - 1)
# 		if home_goals - away_goals == 1:
# 			P1 = P1 * P_Hbd
# 		elif home_goals == away_goals:
# 			P1 = P1 * P_Htd
# 		else:
# 			P1 = P1 * p_hg	
# 	else:
# 		P1 = 0

# 	if away_goals > 0:
# 		P2 = probability_of_result_recursive(home_goals, away_goals - 1, rating_difference, n - 1)
# 		if home_goals - away_goals ==  - 1:
# 			P2 = P2 * P_Abd
# 		elif home_goals == away_goals:
# 			P2 = P2 * P_Atd
# 		else:
# 			P2 = P2 * p_ag
# 	else:
# 		P2 = 0

# 	if n > home_goals + away_goals:
# 		P3 = probability_of_result_recursive(home_goals, away_goals, rating_difference, n - 1)
# 		if home_goals - away_goals == 1:
# 			P3 = P3 * P_Ntd_fh
# 		elif home_goals - away_goals == -1:
# 			P3 = P3 * P_Ntd_fa
# 		elif home_goals == away_goals:
# 			P3 = P3 * P_Nbd
# 		else:
# 			P3 = P3 * P_Ng
# 	else:
# 		P3 = 0

# 	return P1 + P2 + P3

if __name__ == "__main__":
	main()