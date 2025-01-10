from enum import Enum

class DatasourceType(str, Enum):
    postgres = "postgres"
    mysql = "mysql"
    sqlite = "sqlite"