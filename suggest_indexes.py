# Copyright (c) 2024 Brent E Edwards.

"""
This program reads a cockroach log, runs the queries through "EXPLAIN",
and returns suggested indexes.
"""

import json
import sys
from common import cleanup, get_config_section, get_conn_and_cur

# Constants
config_log = get_config_section("LOG")


def parse_line(line):
    """ Given a line, this function determines whether it has a query and
        whether it is of the right user and application. If it is, then
        it returns the query. If not, then it returns None."""

    pos_start = line.find(" ={") + 2
    if pos_start == 1:
        return None

    pos_end = line.rfind("}") + 1
    if pos_end == 0:
        return None

    json_data = json.loads(line[pos_start:pos_end])
    if ("ApplicationName" not in json_data or
            config_log["ApplicationName"] == json_data["ApplicationName"][2:]) and \
            ("User" not in json_data or config_log["User"] == json_data["User"]) and \
            ("Tag" not in json_data or json_data["Tag"] == "SELECT"):
        if "Statement" in json_data:
            statement = json_data["Statement"]
            no_indicators = statement.replace("‹", "").replace("›", "")
            return no_indicators + ";"
    return None


def next_query():
    """ This generator will return the next query from the log. """
    filename = config_log["logfile"]
    file = open(file=filename, mode="r")
    line = file.readline()
    while line != "":
        query = parse_line(line)
        if query is not None:
            yield query
        line = file.readline()


def query_to_index_recommendations(query, cur):
    """ This function returns a list of all index recommendations that it finds."""
    query_explain = "EXPLAIN " + query
    cur.execute(query_explain)
    explain_lines = cur.fetchall()
    index_recommendations = []
    for tuple_line in explain_lines:
        line = tuple_line[0]
        if "CREATE INDEX" in line:
            pos_start = line.find("CREATE INDEX")
            pos_end = line.find(";") + 1
            if pos_end == 0:
                print("It's likely that there is a multi-line index. "
                      "I am not equipped to parse that.", file=sys.stderr)
                pos_end = len(line)
            index_recommendations.append(line[pos_start:pos_end])
    return index_recommendations


def main():
    """ The main program, which calls everything else. """
    (conn, cur) = get_conn_and_cur()
    all_indexes = []
    try:
        for query in next_query():
            indexes = query_to_index_recommendations(query, cur)
            all_indexes.extend(indexes)
    finally:
        cleanup(conn, cur)

    if len(all_indexes) > 0:
        print("I recommend the following indexes be added:")
        for index in all_indexes:
            print(index)
    else:
        print("It's all good!")


if __name__ == "__main__":
    main()
