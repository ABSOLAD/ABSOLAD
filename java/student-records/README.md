# Student Records

A desktop student-record manager built with Java Swing. Records persist locally in a CSV-style file.

## Features

- Add students with a unique positive ID.
- List records in a table.
- Search by student ID.
- Delete the selected record.
- Save records to `students.csv` between runs.
- Uses only the Java standard library.

## Run

Requires JDK 17 or newer.

```bash
javac Main.java
java Main
```

The application creates `students.csv` in the current working directory. Back up this file if you need to preserve records.

## Current limitations

This starter project uses a simple local flat file rather than a relational database. It is intended for learning Java GUI programming, collections, input validation and file I/O.
