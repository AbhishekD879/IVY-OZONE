# General
TBD

# Tasks

### TODO
-

### FIXME

- Spring Boot 2 Migration

  - drop MongoDB indexes:

    - `users:email_1`
    - `users:email_deduplicate`
    - `promotions.brand_promotionId_deduplicate`
    - `sportmodules:brand_sport_type`
    - `sportmodules:brand_sport_type_page`

    ``` mongodb
    use bma;
    db.users.dropIndex("email_1");
    db.users.dropIndex("email_deduplicate");
    db.promotions.dropIndex("brand_promotionId_deduplicate");
    db.sportmodules.dropIndex("brand_sport_type");
    db.sportmodules.dropIndex("brand_sport_type_page");
    ```

  - delete possiable duplicaates, ex:
    `db.sportmodules.deleteOne({"_id": ObjectId("if any")})`

### DONE
- sonarcloud
- log4j2


mongodb://cms-api:password@10.101.130.69:27017/?authSource=admin&readPreference=primary&ssl=false
10.101.131.45
