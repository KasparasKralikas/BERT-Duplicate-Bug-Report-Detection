import json, random, numpy as np

ISSUES_FILE = 'esn.json'
GENERATED_PAIRS_FILE = 'esn_pairs.json'

def main():
    f = open(ISSUES_FILE, 'rb')
    issues = np.asarray(json.load(f))
    pairs = generate_pairs(issues, 100, 0.5)
    f = open(GENERATED_PAIRS_FILE, 'w')
    json.dump(pairs, f)

    

def generate_pairs(issues, count, duplicate_pairs_part):
    duplicates_count = int(count * duplicate_pairs_part)
    non_duplicates_count = int(count - duplicates_count)
    pairs = list()
    # Generate non-duplicate pairs
    for i in range(non_duplicates_count):
        pairs.append(get_non_duplicate_pair(issues))
    # Generate duplicate pairs
    duplicate_issues = duplicate_issues = np.array([issue for issue in issues if issue['dup_id']])
    for i in range(duplicates_count):
        pairs.append(get_duplicate_pair(issues, duplicate_issues))
    random.shuffle(pairs)
    return pairs

def get_non_duplicate_pair(issues):
    issue_1 = np.random.choice(issues)
    filtered_issues = np.array([issue for issue in issues if (issue['bug_id'] != issue_1['bug_id'] and not (issue['bug_id'] == issue_1['dup_id'] or issue['dup_id'] == issue_1['bug_id'] or (issue['dup_id'] and issue_1['dup_id'] and issue['dup_id'] == issue_1['dup_id'])))])
    issue_2 = np.random.choice(filtered_issues)
    return {
        'bug_id_1': issue_1['bug_id'],
        'dup_id_1': issue_1['dup_id'],
        'description_1': issue_1['description'],
        'bug_id_2': issue_2['bug_id'],
        'dup_id_2': issue_2['dup_id'],
        'description_2': issue_2['description'],
        'label': 0
    }

def get_duplicate_pair(issues, duplicate_issues):
    issue_1 = np.random.choice(duplicate_issues)
    filtered_issues = np.array([issue for issue in issues if (issue['bug_id'] != issue_1['bug_id'] and (issue['bug_id'] == issue_1['dup_id'] or issue['dup_id'] == issue_1['bug_id'] or (issue['dup_id'] and issue_1['dup_id'] and issue['dup_id'] == issue_1['dup_id'])))])
    issue_2 = np.random.choice(filtered_issues)
    return {
        'bug_id_1': issue_1['bug_id'],
        'dup_id_1': issue_1['dup_id'],
        'description_1': issue_1['description'],
        'bug_id_2': issue_2['bug_id'],
        'dup_id_2': issue_2['dup_id'],
        'description_2': issue_2['description'],
        'label': 1
    }

if __name__ == '__main__':
    main()