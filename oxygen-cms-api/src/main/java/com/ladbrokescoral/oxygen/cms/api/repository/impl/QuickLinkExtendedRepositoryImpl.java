package com.ladbrokescoral.oxygen.cms.api.repository.impl;

import com.ladbrokescoral.oxygen.cms.api.entity.QuickLink;
import com.ladbrokescoral.oxygen.cms.api.repository.QuickLinkExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import java.time.Instant;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;

@Repository
public class QuickLinkExtendedRepositoryImpl implements QuickLinkExtendedRepository {

  private MongoTemplate mongoTemplate;

  @Autowired
  public QuickLinkExtendedRepositoryImpl(MongoTemplate mongoTemplate) {
    this.mongoTemplate = mongoTemplate;
  }

  @Override
  public List<QuickLink> findQuickLinks(String brand, String raceType) {
    Query query = new Query();
    query.addCriteria(
        Criteria.where("disabled")
            .is(false)
            .and("brand")
            .is(brand)
            .and("raceType")
            .is(raceType)
            .and("validityPeriodEnd")
            .gt(Instant.now()));
    query.with(SortableService.SORT_BY_SORT_ORDER_ASC);

    return mongoTemplate.find(query, QuickLink.class);
  }
}
