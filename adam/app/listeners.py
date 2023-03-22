from torpedo.constants import ListenerEventTypes
from torpedo import CONFIG
from sanic.log import error_logger

config = CONFIG.config

background_tasks = []

# Initializing listeners with background task only if
# the background worker flag is enabled.
listeners = background_tasks
