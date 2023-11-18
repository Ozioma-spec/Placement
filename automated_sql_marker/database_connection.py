# imports
import oracledb


def create_connection():
    """
    create a connection to the oracle database
    :return:
    """
    oracledb.init_oracle_client(
        # Uncomment the below line while at home - you need to change this to point to where you download and
        # install Oracle instant client
        lib_dir=r"C:\oml4rclient_install_dir\instantclient_21_11"
    )

    connection = oracledb.connect(
        user="admin", password="Paschal23481$", dsn="aryv8ynqn1il7pyq_high"
    )
    # Add your Oracle user id - probably admin, the Oracle password and find the DSN - use the _high instance

    cursor = connection.cursor()
    return cursor


# if __name__ == '__main__':
