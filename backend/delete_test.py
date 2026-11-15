import sqlite3

conn = sqlite3.connect("assetflow.db")
cursor = conn.cursor()

cursor.execute(
    "DELETE FROM Bookings WHERE BookingID = ?",
    (3,)
)

conn.commit()
print("Rows deleted:", cursor.rowcount)

conn.close()