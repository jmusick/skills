# 1. Store invoices in one JSON file

Status: accepted

We keep every invoice in a single JSON file instead of a database. The tool runs once a night on
one machine for one office, with a few hundred invoices a year. A database would add a server to
run and back up for no gain at this size. Revisit if more than one process ever writes the file.
