import sys, argparse, bson, bson.json_util, json

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, help="Input bson file name")
    parser.add_argument('--output', type=str, help="Output json file name")
    args = parser.parse_args()
    input_file, output_file = args.input, args.output
    data = None
    f = open(input_file, 'rb')
    data = bson.decode_all(f.read())
    f = open(output_file, 'w')
    json_data = bson.json_util.dumps(data, json_options=bson.json_util.RELAXED_JSON_OPTIONS)
    f.write(json_data)
    return

if __name__ == "__main__":
    main()