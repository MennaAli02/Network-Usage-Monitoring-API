from db.crud import read_lines, read_quota_results, read_speed_test_results, get_total_dataused_per_line, get_count_per_renewal_cost, remaining_balance_by_line, average_speeds_per_line, average_ping_per_line

lines = read_lines()
print(lines)
# read_quota_results()
# read_speed_test_results()
# get_total_dataused_per_line()
# get_count_per_renewal_cost()
remaining_balance_by_line()
# average_speeds_per_line()
# average_ping_per_line()


