import json, random, numpy as np, pandas as pd

ISSUES_FILE = 'esn.csv'
GENERATED_PAIRS_FILE = 'esn_pairs.csv'

def main():
    issues = get_issues(ISSUES_FILE)
    pairs_df = generate_pairs(issues, 2, 0.5)
    pairs_df.to_csv(GENERATED_PAIRS_FILE, index=False)

def get_issues(issues_file):
  issues = pd.read_csv(issues_file)
  issues['full_description'] = issues['short_desc'].astype(str) + issues['description'].astype(str)
  return issues
    

def generate_pairs(issues, count, duplicate_pairs_part):
    duplicates_count = int(count * duplicate_pairs_part)
    non_duplicates_count = int(count - duplicates_count)
    pairs_list = []
    # Generate non-duplicate pairs
    for i in range(non_duplicates_count):
        pairs_list.append(get_non_duplicate_pair(issues))
    # Generate duplicate pairs
    duplicate_issues = issues[(issues['dup_id'].notnull())]
    for i in range(duplicates_count):
        pairs_list.append(get_duplicate_pair(issues, duplicate_issues))
    random.shuffle(pairs_list)
    df = pd.DataFrame(pairs_list)
    return df

def get_non_duplicate_pair(issues):
    issue_1 = issues.sample().iloc[0]
    filtered_issues = issues[(issues['master_id'] != issue_1['master_id'])]
    issue_2 = filtered_issues.sample().iloc[0]
    return {
        'bug_id_1': issue_1['bug_id'],
        'dup_id_1': issue_1['dup_id'],
        'description_1': str(issue_1['full_description']),
        'bug_id_2': issue_2['bug_id'],
        'dup_id_2': issue_2['dup_id'],
        'description_2': str(issue_2['full_description']),
        'label': 0
    }

def get_duplicate_pair(issues, duplicate_issues):
    issue_1 = duplicate_issues.sample().iloc[0]
    filtered_issues = issues[(issues['master_id'] == issue_1['master_id']) & (issues['bug_id'] != issue_1['bug_id'])]
    issue_2 = filtered_issues.sample().iloc[0]
    return {
        'bug_id_1': issue_1['bug_id'],
        'dup_id_1': issue_1['dup_id'],
        'description_1': str(issue_1['full_description']),
        'bug_id_2': issue_2['bug_id'],
        'dup_id_2': issue_2['dup_id'],
        'description_2': str(issue_2['full_description']),
        'label': 1
    }

if __name__ == '__main__':
    main()