# Database directory
This acts as the core SQLite database file storage directory. `dungeonBot.db` is targeted to
generate within this directory and a filepath `./Database` must exist or DungeonBot will
fail to launch.

`dungeonBot.db` will be uniquely generated and maintained via the `DBHelper` package included
in the DungeonBot source code.