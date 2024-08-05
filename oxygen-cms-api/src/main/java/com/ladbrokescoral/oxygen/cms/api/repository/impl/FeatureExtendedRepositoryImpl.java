package com.ladbrokescoral.oxygen.cms.api.repository.impl;

import com.ladbrokescoral.oxygen.cms.api.entity.Feature;
import com.ladbrokescoral.oxygen.cms.api.repository.FeatureExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import java.time.Instant;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;

@Repository
public class FeatureExtendedRepositoryImpl implements FeatureExtendedRepository {

  private MongoTemplate mongoTemplate;

  @Autowired
  public FeatureExtendedRepositoryImpl(MongoTemplate mongoTemplate) {
    this.mongoTemplate = mongoTemplate;
  }

  @Override
  public List<Feature> findFeatures(String brand) {
    Query query = new Query();
    query.addCriteria(
        Criteria.where("disabled")
            .is(false)
            .and("brand")
            .is(brand)
            .and("validityPeriodEnd")
            .gt(Instant.now()));
    query.with(SortableService.SORT_BY_SORT_ORDER_ASC);

    return mongoTemplate.find(query, Feature.class);
  }
}
