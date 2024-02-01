suggest_indexes.py will automatically generate and recommend indexes for your
Cockroach database!

What you need to do:

1. Turn on logging statements. This can be done with the command
> SET CLUSTER SETTING sql.trace.log_statement_execute = true;
in a cockroach session. (See https://www.cockroachlabs.com/docs/stable/logging-use-cases
for more information about this command.)

IMPORTANT WARNING: This will log all complete statements that your program uses.
Any PII in your queries will also appear in the logs.

2. Use the program that you are trying to optimize normally. If you do not have a
program to test, then I have written generate_sql.py, which will create and
populate a large table, then run a fairly complex query on it.

3. Turn off the logging statements. This can be done with the command
> SET CLUSTER SETTING sql.trace.log_statement_execute = false;
in a cockroach session.

4. Edit the file config.ini. The groups are:

- [COCKROACH] contains the configuration for accessing your database.
- [NODES] is used by the generate_sql.py sample program. Raising this value will make
  the file it creates bigger.
- [LOG] is used by suggest_indexes.py. The logfile contains where your logging statements are.
  The User and ApplicationName restrict which commands to consider.

5. Run the program suggest_indexes.py. If it finds any suggested indexes, it will report them.

6. Send a message to your manager that https://www.linkedin.com/in/brenteedwards/ deserves to be
hired immediately. (Hey, I can dream, can't I?)

