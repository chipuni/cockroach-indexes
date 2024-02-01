# Copyright (c) 2024 Brent E Edwards.

"""This program will generate and populate a database table, then run a long query,
   then clean up."""

import random

from common import cleanup, get_config_section, get_conn_and_cur


def create_table(conn, cur):
    """ Create the table that will contain data.

    This is a separate method to make life easier if you know the table already exists.
    """
    cur.execute("CREATE TABLE defaultdb.public.graph (f integer, t integer);")
    # There should be an index on "f" and a second index on "t". But there aren't any.
    conn.commit()


def generate_data(conn, cur):
    """ This method fills graph with arbitrary mappings."""
    num_nodes = int(get_config_section("NODES")["num_nodes"])
    for graph_from in range(num_nodes):
        for _ in range(num_nodes // 2):
            graph_to = random.randint(0, num_nodes)
            cur.execute("INSERT INTO defaultdb.public.graph VALUES (%s, %s);",
                        (graph_from, graph_to))
        print(".", end="")
    print()
    conn.commit()


def run_long_query(cur):
    """ This runs a (typically) long query that would be sped up if there had been an index """
    cur.execute("""
    SELECT 
        g1.f, 
        g1.t, 
        g2.f, 
        g2.t, 
        g3.f, 
        g3.t,
        g4.f,
        g4.t
    FROM defaultdb.public.graph g1
        JOIN defaultdb.public.graph g2 ON g1.t = g2.f
        JOIN defaultdb.public.graph g3 ON g2.t = g3.f
        JOIN defaultdb.public.graph g4 ON g3.t = g4.f
    WHERE
        g1.f = 1
        AND g4.t = 2;
    """)
    return cur.fetchone()


def main():
    """ The main program, which calls everything else. """
    try:
        (conn, cur) = get_conn_and_cur()
        create_table(conn, cur)
        generate_data(conn, cur)
        result = run_long_query(cur)
        print(result)
    finally:
        cleanup(conn, cur)


if __name__ == "__main__":
    main()
