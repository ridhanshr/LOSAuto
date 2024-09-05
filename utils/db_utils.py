import pyodbc
import re

def update_appflag(no_aplikasi_data: str, ap_currtrcode: str , ap_lasttrcode: str, server='172.24.141.60,1433', database='LOSBRICC', username='sa', password='P@ssw0rd'):
    """
    Update the APPFLAG column in LOSBRICC database.

    Parameters:
    - no_aplikasi_data (str): The application number to be updated.
    - ap_currtrcode (str): The currtrcode flag to be updated.
    - ap_lasttrcode (str): The lasttrcode flag to be updated.
    - server (str): SQL Server address and port.
    - database (str): The database name.
    - username (str): The username for SQL Server.
    - password (str): The password for SQL Server.

    Returns:
    - App Flag Update
    """
    # Setup DB connection string
    conn_str = (
        f'DRIVER={{ODBC Driver 18 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
        'TrustServerCertificate=yes;'
    )

    try:
        # Connect to the database
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()
        
        # SQL query
        sql_query = f"""
            UPDATE APPFLAG
            SET AP_CURRTRCODE = '{ap_currtrcode}', AP_LASTTRCODE = '{ap_lasttrcode}'
            WHERE AP_REGNO = '{no_aplikasi_data}'
        """
        
        # Execute query
        cursor.execute(sql_query)
        
        # Commit changes
        connection.commit()
        
    except pyodbc.Error as e:
        print(f"Database error: {e}")
    finally:
        # Close the connection
        cursor.close()
        connection.close()

def update_user(no_aplikasi_data, ap_nexttrby='cc_dam', server='172.24.141.60,1433', database='LOSBRICC', username='sa', password='P@ssw0rd'):
    """
    Update the AP_NEXTTRBY column in LOSBRICC database.

    Parameters:
    - no_aplikasi_data (str): The application number to be updated.
    - ap_nexttrby (str): The user to be updated.
    - server (str): SQL Server address and port.
    - database (str): The database name.
    - username (str): The username for SQL Server.
    - password (str): The password for SQL Server.

    Returns:
    - User Update
    """
    # Setup DB connection string
    conn_str = (
        f'DRIVER={{ODBC Driver 18 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
        'TrustServerCertificate=yes;'
    )

    try:
        # Connect to the database
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()

        # SQL query
        sql_query = f"""
            UPDATE APPFLAG
            SET AP_NEXTTRBY = '{ap_nexttrby}'
            WHERE AP_REGNO = '{no_aplikasi_data}'
        """
        
        # Execute query
        cursor.execute(sql_query)
        
        # Commit changes
        connection.commit()
        
    except pyodbc.Error as e:
        print(f"Database error: {e}")
    finally:
        # Close the connection
        cursor.close()
        connection.close()

def update_norek(no_aplikasi_data, norek, server='172.24.141.60,1433', database='LOSBRICC', username='sa', password='P@ssw0rd'):
    """
    Update the A4_ACHACCT column in LOSBRICC database.

    Parameters:
    - no_aplikasi_data (str): The application number to be updated.
    - ap_nexttrby (str): The user to be updated.
    - server (str): SQL Server address and port.
    - database (str): The database name.
    - username (str): The username for SQL Server.
    - password (str): The password for SQL Server.

    Returns:
    - Norek Update
    """
    # Setup DB connection string
    conn_str = (
        f'DRIVER={{ODBC Driver 18 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
        'TrustServerCertificate=yes;'
    )

    try:
        # Connect to the database
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()

        # SQL query
        sql_query = f"""
            UPDATE DATATOCARDLINK
            SET A4_ACHACCT = '{norek}'
            WHERE AP_REGNO = '{no_aplikasi_data}'
        """
        
        # Execute query
        cursor.execute(sql_query)
        
        # Commit changes
        connection.commit()
        
    except pyodbc.Error as e:
        print(f"Database error: {e}")
    finally:
        # Close the connection
        cursor.close()
        connection.close()

def check_appflag(no_aplikasi_data: str,  server='172.24.141.60,1433', database='LOSBRICC', username='sa', password='P@ssw0rd'):
    """
    Check the APPFLAG column in LOSBRICC database.

    Parameters:
    - no_aplikasi_data (str): The application number to be checked.
    - server (str): SQL Server address and port.
    - database (str): The database name.
    - username (str): The username for SQL Server.
    - password (str): The password for SQL Server.

    Returns:
    - App Flag
    """
    # Setup DB connection string
    conn_str = (
        f'DRIVER={{ODBC Driver 18 for SQL Server}};'
        f'SERVER={server};'
        f'DATABASE={database};'
        f'UID={username};'
        f'PWD={password};'
        'TrustServerCertificate=yes;'
    )

    try:
        # Connect to the database
        connection = pyodbc.connect(conn_str)
        cursor = connection.cursor()
        
        # SQL query
        sql_query = f"""
            SELECT AP_CURRTRCODE FROM appflag
            WHERE AP_REGNO = '{no_aplikasi_data}'
        """
        
        # Execute query
        cursor.execute(sql_query)
        
        # Mengambil dan mencetak hasil query
        rows = cursor.fetchall()
        AP_CURRTRCODE = rows[0]

        
    except pyodbc.Error as e:
        print(f"Database error: {e}")
    finally:
        # Close the connection
        cursor.close()
        connection.close()
    
    return AP_CURRTRCODE


# EXAMPLE
# code = check_appflag('KNP2024073000004')
# pattern = re.compile(r"'(.*?)'")
# match = pattern.search(str(code))
# print(match.group(1))