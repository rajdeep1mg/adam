from torpedo import Host, CONFIG
from .routes import blueprints
from .listeners import listeners
from redis_wrapper import RegisterRedis

if __name__ == "__main__":
    # config object will be dict representation of config.json read by the utility function in torpedo

    Host._listeners = listeners

    # register combined blueprint group here. these blueprints are defined in the routes

    Host._blueprint_group = blueprints

    # register redis connection
    RegisterRedis.register_redis_cache(CONFIG.config["REDIS_CACHE_HOSTS"])

    Host.run()
