# escwaapi

A ViEWS2-based API for retrieving predictions, based on ESCWA-discussed specifications.

Works, including basic filtering, but code is throwaway quality, as it is built around the flat prediction files produced by ViEWS2. It's a terrible mess rightnow.

## Supported ViEWS facilities:

- Multiple ViEWS _runs_ simultaneously. Runs can be based on different ViEWS model definitions. Register runs using `escwatransfer`.
- Hierarchically nested ViEWS models (e.g. ensembles based on smaller ensembles based on components). Arbitrary depth can be specified, limited only by Python's recurssion. The tree-based metadata is delivered
- Delivery of both models (`sc`) and prediction `steps` for the models that have `steps`, if so desired. 
- `PG` and `C` levels of analysis, with all categories of violence.

## Supported paths and filters:

- LOA (required)
- sb/ns/os (optional)
- model (optional)


## Requires :

- a PostGres Database.
- `escwatransfer` to transfer data from `views2` (`janus`) into ESCWA
- a ViEWS2 `model hierarchy`, manually built in the database. I did not write a dependency compiler from `yaml`or from Frederick's model dataclasses since that in itself is a huge amount of work, for something that has been very static until now.
