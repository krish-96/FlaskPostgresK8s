from enum import Enum


class AppEnum(Enum):
    log_file_path = "/var/log/flask"
    config_file_path = "../../configs"
    app_config_file_path = "../../configs/app.ini"

    release_notes_dir_path = "../../ReleaseNotes/"
    release_dir_path = "../../ReleaseNotes/Releases/"
    current_release_file_path = "../../ReleaseNotes/CurrentRelease"

    current_release_version_format_UI = "{version}.{year}.{month}.{day}"
    current_release_version_format_BE = "{version}"

    sql_queries_path = "../database/sql_queries/queries.ini"
