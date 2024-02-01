# Copyright (c) 2024 Brent E Edwards.

"""This file contains functions that are common between programs."""

import configparser
import psycopg2


def get_config_section(section):
    """Read the configuration, get the values of one section."""
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config[section]


def get_conn_and_cur():
    """Get the two variables that are needed to execute statements.

    Everything after this method should be run inside a try...finally
    clause, and the finally clause should call cleanup."""
    config_c = get_config_section("COCKROACH")
    conn = psycopg2.connect(dbname=config_c["dbname"],
                            user=config_c["user"],
                            host=config_c["host"],
                            port=config_c["port"],
                            password=config_c["password"])
    cur = conn.cursor()
    return (conn, cur)


def cleanup(conn, cur):
    """Close everything."""
    cur.close()
    conn.close()
