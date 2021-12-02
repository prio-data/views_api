# escwaapi

A ViEWS2-based API for retrieving predictions, based on ESCWA-discussed specifications.

Works, including basic filtering, but code is throwaway quality, as it is built around the flat prediction files produced by ViEWS2. It's a terrible mess rightnow.

## Supported ViEWS facilities:

- Multiple ViEWS _runs_ simultaneously. Runs can be based on different ViEWS model definitions. Register runs using `escwatransfer`.
- Hierarchically nested ViEWS models (e.g. ensembles based on smaller ensembles based on components). Arbitrary depth can be specified, limited only by Python's recurssion. The tree-based metadata is delivered
- Delivery of both models (`sc`) and prediction `steps` for the models that have `steps`, if so desired. 
- `PG` and `C` levels of analysis, with all categories of violence.

## Supported paths and filters:

### Paths:
- LOA (required)
- sb/ns/os/px (optional)
- individual model (optional)

Due to limitations in FastAPI, fuzzy paths (eg `sb,ns`) will not be possible at this time. Go one level above or run the API twice

### Filters
- space (priogrid, countries (lists allowed, as well as GWNO et., BoundingBox, ISO))
- time (month, ISO dates)
- **TODO** : stored filtersets (`escwa`, `africa` etc.)

**Won't do** : Due to FastAPI limitations, `country=AFG,ALG` type filters are not available. You will have to work with `country=AFG&country=ALG` for multiple (Array-based) filters.

### Paging
- works. Implemented next_url and prev_url URL scheme for user convenience.

### Security and 
- No SQL injection should be possible (dual layer of abstraction via FastAPI and SQLAlchemy) but no ORM (so no guarantees)
- **TODO** : API key (maybe?)

## Requires :

- a Postgres Database (edit `libdb/config.py`).
- a ViEWS2 `model hierarchy`, manually built in the database in the `structure`. I did not write a dependency compiler from `yaml`or from Frederick's model dataclasses since that in itself is a huge amount of work, for something that has been very static until now. Ideally, start with a simple structure dump (in `escwatransfer`).
- `escwatransfer` to transfer data from `views2` (`janus` or `hermes`) into ESCWA. Access to `views2` or `views2 dumps` is required for transferring data.
- **TODO** : dockerize this whole mess and write an INSTALL file.
