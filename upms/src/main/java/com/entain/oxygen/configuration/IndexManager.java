package com.entain.oxygen.configuration;

import java.util.Arrays;
import java.util.List;
import java.util.Objects;
import javax.annotation.PostConstruct;
import lombok.RequiredArgsConstructor;
import org.apache.commons.lang3.StringUtils;
import org.springframework.data.mongodb.core.ReactiveMongoTemplate;
import org.springframework.data.mongodb.core.index.ReactiveIndexOperations;
import org.springframework.stereotype.Component;

/** A class which is used to manage the indexes on collections in mongodb */
@Component
@RequiredArgsConstructor
public class IndexManager {

  private final ReactiveMongoTemplate mongoTemplate;

  private final MongoDbProperties mongoDbProperties;

  /** this method drops the already created indexes on collections in mongodb */
  @PostConstruct
  public void dropIndex() {
    MongoDbProperties.Index indexProps = mongoDbProperties.getIndex();
    List<String> collectionNames = Arrays.asList(indexProps.getCollectionNames().trim().split(","));
    List<String> indexes = Arrays.asList(indexProps.getIndexNames().trim().split(","));
    collectionNames.stream()
        .filter(StringUtils::isNotBlank)
        .forEach(
            (String collection) -> {
              ReactiveIndexOperations indexOperations = this.mongoTemplate.indexOps(collection);
              indexOperations
                  .getIndexInfo()
                  .filter(Objects::nonNull)
                  .filter(indexInfo -> indexes.contains(indexInfo.getName()))
                  .doOnNext(indexInfo -> indexOperations.dropIndex(indexInfo.getName()).subscribe())
                  .subscribe();
            });
  }
}
