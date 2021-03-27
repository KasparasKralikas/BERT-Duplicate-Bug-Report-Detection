import json

ISSUES_FILE = "esn.json"

def main():
    f = open(ISSUES_FILE)
    issues = json.load(f)
    print(len(issues))
    print(issues[0]['description'])

def generate_pairs(issues, count, duplicate_pairs_part):
    return []

if __name__ == "__main__":
    main()