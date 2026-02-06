@echo off
echo Setting up MariaDB database...
"C:\Program Files\MariaDB 12.1\bin\mysql.exe" -u root -p1234 < setup.sql
echo Database setup completed!
pause
