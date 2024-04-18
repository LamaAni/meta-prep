from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider


# Create a Cluster object.
cluster = Cluster(
    ["localhost"],
    auth_provider=PlainTextAuthProvider(
        "admin",
        "password",
    ),
)

# Connect to the cluster.
session = cluster.connect()

# Create a keyspace.
session.execute(
    "CREATE KEYSPACE IF NOT EXISTS mykeyspace WITH REPLICATION = {'class' : 'SimpleStrategy', 'replication_factor' : 1}"
)

# Use the keyspace.
session.set_keyspace("mykeyspace")

# Create a table.
session.execute(
    """CREATE TABLE IF NOT EXISTS mytable (
    key text PRIMARY KEY,
    value text
)"""
)

# Insert a key-value pair.
session.execute("INSERT INTO mytable (key, value) VALUES ('mykey', 'myvalue')")

# Get the value for a key.
row = session.execute("SELECT value FROM mytable WHERE key = 'mykey'")

# Print the value.
print(row[0].value)

# Close the session.
session.shutdown()
