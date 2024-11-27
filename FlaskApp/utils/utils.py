import os
import yaml
import platform
from datetime import datetime
from configparser import ConfigParser
from typing import Optional, Dict, AnyStr, Any
import fernet

from FlaskApp.exceptions import UnSupportedPlatform
from FlaskApp.constants import AppEnum
from FlaskApp.database import get_connection
from FlaskApp.log_configs import logger


def get_current_date(date_format=None) -> datetime.date:
    today = datetime.now().date()
    try:
        if date_format:
            return today.strftime(date_format)
        return today
    except:
        return today


def get_current_datetime(datetime_format=None) -> datetime.now:
    now = datetime.now()
    try:
        if datetime_format:
            return now.strftime(datetime_format)
        return now
    except:
        return now


def create_dir(dirs):
    """This function will create the parent directories for the given path
        If the path already exists, it'll skip
    """
    try:
        os.makedirs(os.path.dirname(dirs), exist_ok=True)
    except Exception as create_dir_err:
        print(f"Exception occurred while creating the directories @ {dirs}, Exception: {create_dir_err}")


def get_abs_path(file_path):
    """This function wil return the absolute path for the given file path"""
    try:
        file_path = os.path.normpath(os.path.join(os.path.dirname(__file__), file_path))
        return file_path
    except Exception as get_abs_path_err:
        print(f"Exception occurred while fetching the abs path @ {file_path}, Exception: {get_abs_path_err}")


def get_properties(file_path, section: str, option: Optional[str] = None) -> Dict | str | None:
    """This function wil read the data form the given configuration file
        and returns the data for the given section and optional option (key).
        if the given section is not exists, it'll return None
    :param file_path: configuration file path
    :param section: configuration section
    :param option: configuration option (Key)

    """
    try:
        file_path = get_abs_path(file_path)
        cfg = ConfigParser()
        cfg.read(file_path)
        if section and cfg.has_section(section=section):
            if option and cfg.has_option(section=section, option=option):
                return cfg[section][option]
            return cfg[section]
    except Exception as get_props_err:
        print(f"Exception occurred while fetching the properties @ {file_path}, Exception: {get_props_err}")


def get_yaml_content(file_path, key: Optional[str] = None) -> Optional[Dict | AnyStr | Any]:
    """
    This function will read the yaml content from the given file path and returns the data,
    If the key specified, it'll return the associated value
    If the key specified and key doesn't exist, it will return raise KeyError Exception
    :param file_path: relative Yaml file path
    :param key: key name in the Yaml file
    :return:
    """
    try:
        file_path = get_abs_path(file_path)
        with open(file_path, 'r') as yml_file:
            yaml_data = yaml.safe_load(yml_file.read())
        if key is not None:
            if key not in yaml_data:
                raise KeyError("Couldn't find the specified key!")
            return yaml_data.get(key)
        return yaml_data
    except KeyError as yaml_key_err:
        logger.error(f"Exception occurred while fetching the yaml content @ {file_path}, Exception: {yaml_key_err}")
        raise yaml_key_err
    except Exception as get_yaml_data_err:
        logger.error(
            f"Exception occurred while fetching the yaml content @ {file_path}, Exception: {get_yaml_data_err}")


def check_platform_compatibility():
    """This function checks for the platform compatibility
    :returns True if it supports
             raises an Exception if it does not support
    """
    current_platform = platform.system()
    supported_platforms = get_properties(
        AppEnum.app_config_file_path.value, section="SupportedPlatforms", option="platforms"
    )
    supported_platforms = supported_platforms.lower() if supported_platforms else supported_platforms
    if current_platform.lower() not in supported_platforms:
        raise UnSupportedPlatform(f"Detected Unsupported Platform\n Supported Platforms: {supported_platforms}")
    return True


def get_server_properties():
    server_properties = get_properties(AppEnum.app_config_file_path.value, section="Server")
    return server_properties


def check_db_status() -> bool:
    """
    This will create a database connection and close, To determine whether the app can connect to the database or not
    :return True if the database connection established else False
    """
    is_connection_available = False
    connection = get_connection()
    if connection:
        logger.debug("Database connection established")
        logger.debug("Closing database connection.")
        connection.close()
        is_connection_available = True
    return is_connection_available


def format_release_version(release_version, released_date):
    current_date = datetime.strptime(released_date, "%m/%d/%Y")
    print("current_date: ", current_date, current_date.day)
    return AppEnum.current_release_version_format_UI.value.format(
        version=release_version, day=current_date.day, month=current_date.month, year=current_date.year
    )


def get_current_version(formatted=True):
    try:
        current_release_details = get_properties(
            file_path=AppEnum.current_release_file_path.value,
            section="CurrentRelease"
        )
        current_release_version = current_release_details.get('version')
        current_release_date = current_release_details.get('date')
        if formatted:
            return format_release_version(current_release_version, released_date=current_release_date)
        return current_release_version
    except:
        return


def get_all_releases(release_version=None):
    try:
        release_notes = []
        releases_dir = AppEnum.release_dir_path.value
        yaml_files = os.listdir(get_abs_path(releases_dir))
        if release_version:
            if (yaml_file := f"{release_version}.yml") in yaml_files:
                yaml_data = get_yaml_content(os.path.join(releases_dir, yaml_file))
                release_notes.append(yaml_data)
        else:
            for yaml_file in yaml_files:
                current_yaml_file_content = get_yaml_content(os.path.join(releases_dir, yaml_file))
                release_notes.append(current_yaml_file_content)
        return release_notes
    except Exception as rel_err:
        print(f"Exception occurred while fetching the releases @ {release_version}, Exception: {rel_err}")
        return False


def get_current_release_notes():
    try:
        current_version = get_current_version(formatted=False)
        current_release = get_all_releases(release_version=current_version)
        return current_release
    except:
        return False


def generate_encrypt_key():
    return fernet.Fernet.generate_key()


def encrypt_data(data, key):
    if not key:
        raise ValueError("No encryption key was provided!")
    fernet_obj = fernet.Fernet(key)
    encrypted_data = fernet_obj.encrypt(data)
    return encrypted_data.decode('utf-8')


def decrypt_data(data, key):
    if not key:
        raise ValueError("No decryption key was provided!")
    fernet_obj = fernet.Fernet(key)
    decrypted_data = fernet_obj.decrypt(data)
    return decrypted_data.decode('utf-8')
