import sys, argparse, bson
import numpy as np
import pandas as pd

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help='Input bson file name')
    parser.add_argument('--output', type=str, help='Output csv file name')
    args = parser.parse_args()
    input_file, output_file = args.input, args.output
    issues = None
    f = open(input_file, 'rb')
    issues = np.asarray(bson.decode_all(f.read()))
    df = pd.DataFrame(columns=['bug_id', 'dup_id', 'master_id', 'short_desc', 'description'])
    for issue in issues:
        df = df.append({
            'bug_id': int(issue['bug_id']),
            'dup_id': None if not issue['dup_id'] else int(issue['dup_id']),
            'master_id': int(issue['bug_id']) if not issue['dup_id'] else int(issue['dup_id']),
            'short_desc': str(issue['short_desc']),
            'description': str(issue['description'])
        }, ignore_index=True)
    df = df.sort_values(by='bug_id')
    df.to_csv(output_file, index=False)
    return

if __name__ == '__main__':
    main()