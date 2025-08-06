def find_non_overlapping_intervals(intervals):
    intervals.sort(key=lambda x: x[0])  # Sort intervals by start time
    non_overlapping = []
    for interval in intervals:
        if not non_overlapping or non_overlapping[-1][1] < interval[0]:
            non_overlapping.append(interval)
    return non_overlapping

# Example usage
intervals = [[1, 2], [3, 6], [4, 7], [7, 8]]
non_overlapping_intervals = find_non_overlapping_intervals(intervals)
print(non_overlapping_intervals)
