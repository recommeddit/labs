#!/usr/bin/python

import sys

import recommendations


def search(request):
    if request.args and 'query' in request.args:
        query = request.args.get('query')
    else:
        query = ""
    results = recommendations.get_recommendations(query)

    return results


def main():
    # assume first argument is query. Default query is 'C++ IDE'
    try:
        query = sys.argv[1]
    except IndexError:
        query = "C++ IDE"

    results = recommendations.get_recommendations(query)

    print(results)


if __name__ == "__main__":
    main()
