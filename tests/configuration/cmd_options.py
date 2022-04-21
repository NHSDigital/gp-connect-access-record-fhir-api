options = [
    {
        "name": "--service-name",
        "required": True,
        "action": "store",
        "help": "The name of the service. This is should be the same name as proxy "
                "without appending env name or PR number."
    },
    {
        "name": "--pr-no",
        "required": False,
        "action": "store",
        "help": "The github pull request number. Example --pr-no=42."
    },
    {
        "name": "--proxy-base-path",
        "required": True,
        "action": "store",
        "help": "The base path for the deployed proxy without appending env name or PR number."
    },
    {
        "name": "--access-token",
        "required": False,
        "action": "store",
        "help": "NHS Login access token. It can be empty only when, apigee-environment is 'local'",
    },
    {
        "name": "--apigee-environment",
        "required": True,
        "action": "store",
        "help": "Apigee environment",
    },
    {
        "name": "--status-api-key",
        "required": True,
        "action": "store",
        "help": "apikey for /_status endpoint"
    }
]


def create_cmd_options(get_cmd_opt_value) -> dict:
    cmd_options = {}
    for opt in options:
        opt_name = opt["name"]
        value = get_cmd_opt_value(opt_name)

        cmd_options.update({opt_name: value})
        if opt["required"] and not value:
            raise Exception(f"Option {opt_name} is required but it's value is empty or null")

    _validate_options(cmd_options)

    return cmd_options


def _validate_options(cmd_options):
    """Whether some values are required or not might change depending on deployment environment"""
    current_env = cmd_options["--apigee-environment"]
    access_token = cmd_options["--access-token"]
    if "local" not in current_env and access_token == "":
        raise Exception("--access-token is required")
