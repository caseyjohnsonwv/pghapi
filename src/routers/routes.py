class Routes:
    healthcheck = '/healthcheck/'
    healthcheck_prefix = healthcheck[:-1]

    users = '/users/'
    users_prefix = users[:-1]

    locations = '/locations/'
    locations_prefix = locations[:-1]

    userlocations = '/user-locations/'
    userlocations_prefix = userlocations[:-1]

    maplookup = '/map-lookup/'
    maplookup_prefix = maplookup[:-1]


class _MapLookup(Routes):
    address_suffix = '/address/'
    address = Routes.maplookup_prefix + address_suffix

    traveltime_suffix = '/travel-time/'
    traveltime = Routes.maplookup_prefix + traveltime_suffix


# nest MapLookup inside Routes
Routes.MapLookup = _MapLookup
