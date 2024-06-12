# Data Product Canvas - Hamburg Geodata

## Input Ports

**Input ports define the format and protocol in which data can be read (database, file, API, visualizations)**

This data product uses geodata provided by [Freie und Hansestadt Hamburg, Landesbetrieb Geoinformation und Vermessung](https://www.hamburg.de/bsw/landesbetrieb-geoinformation-und-vermessung/) available under the following URLs
 * [verwaltungsgrenzen_json.zip](https://metaver.de/trefferanzeige?docuuid=F35EAC11-C236-429F-B1BF-751C0C18E8B7#detail_links:~:text=Download%20ALKIS%20Verwaltungsgrenzen%20Hamburg%20(GeoJSON))
 
## Data Product Design

**Describe everything you need to design a data product on a conceptual level.**
**Ingestion, storage, transport, wrangling, cleaning, transformations, enrichment, augmentation, analytics, SQL
statements, or used data platform services.**

This data product
* [cleans geojson features](../lib/transform/data_property_cleaner.py) by applying properties such as `id`, `name` and `area` across all files 
* [cleans geojson geometry](../lib/transform/data_geometry_cleaner.py) by removing exclaves (that prevent rendering using map services such as [Mapbox](https://www.mapbox.com/))
* [extends properties](../lib/transform/data_property_extender.py) by adding missing area property 
* [calculates a bounding box](../lib/transform/data_bounding_box_converter.py) for each feature based on their coordinates

## Output Ports

**Output ports define the format and protocol in which data can be exposed (db, file, API, visualizations)**

The data of this data product is available under the following URLs
* [hamburg-administrative-boundaries/hamburg-city.geojson](https://raw.githubusercontent.com/open-lifeworlds/open-lifeworlds-data-product-hamburg-geodata/main/data/hamburg-administrative-boundaries/hamburg-city.geojson)
* [hamburg-administrative-boundaries/hamburg-districts.geojson](https://raw.githubusercontent.com/open-lifeworlds/open-lifeworlds-data-product-hamburg-geodata/main/data/hamburg-administrative-boundaries/hamburg-districts.geojson)
* [hamburg-administrative-boundaries/hamburg-quarters.geojson](https://raw.githubusercontent.com/open-lifeworlds/open-lifeworlds-data-product-hamburg-geodata/main/data/hamburg-administrative-boundaries/hamburg-quarters.geojson)
* [hamburg-administrative-boundaries/hamburg-areas.geojson](https://raw.githubusercontent.com/open-lifeworlds/open-lifeworlds-data-product-hamburg-geodata/main/data/hamburg-administrative-boundaries/hamburg-areas.geojson)

## Metadata

### Ownership

**Domain, data product owner, organizational unit, license, version and expiration date**

* ownership: Open Lifeworlds
* domain: geodata
* license: CC-BY-4.0

### Schema

**Attributes, data types, constraints, and relationships to other elements**

The files provided within this data product are using the [geojson format](https://geojson.org/). Properties being added or altered are
* `id`: unique feature ID (string)
* `name`: feature name (string)
* `area`: feature area in sqm (float)
* `bounding_box`: feature bounding box (float array)

### Semantics

**Description, logical model**

The files provided within this data product are arranged in the following hierarchy
* city (Stadt)
* districts (Bezirke)
* quarters (Stadtteile)
* areas (Ortsteile)

### Security

**Security rules applied to the data product usage e.g. public org, internal, personally identifiable information (PII)
attributes**

## Observability

### Quality metrics

**Requirements and metrics such as accuracy, completeness, integrity, or compliance to Data Governance policies**

Completeness of this data product is verified via [data_completeness.py](../lib/metrics/data_completeness.py).

### Operational metrics

**Interval of change, freshness, usage statistics, availability, number of users, data versioning, etc.**

### SLOs

**Thresholds for service level objectives to up alerting**

## Consumer

**Who is the consumer of the Data Product?**

Consumers of this data product may include
* projects that display LOR area
* other data products that combine geospatial data with statistics data

## Use Case

**We believe that ...**
**We help achieving ...**
**We know, we are getting there based on ..., ..., ...**

We believe that this data product can be used to display data related to LOR areas in Berlin on an interactive map. 

## Classification

**The nature of the exposed data (source-aligned, aggregate, consumer-aligned)**

This data product is source-aligned since it only makes small adjustments in terms of variable naming, projection and bounding boxes.

## Ubiquitous Language

**Context-specific domain terminology (relevant for Data Product), Data Product polysemes which are used to create the current Data Product**

* **city**: (German: Stadt)
* **district**: (German: Bezirk)
* **quarter**: (German: Stadtteil)
* **area**: (German: Ortsteil)

---
This data product canvas uses the template
of [datamesh-architecture.com](https://www.datamesh-architecture.com/data-product-canvas).