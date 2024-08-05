package com.ladbrokescoral.oxygen.cms.api.repository.impl;

import com.ladbrokescoral.oxygen.cms.api.entity.SportQuickLink;
import com.ladbrokescoral.oxygen.cms.api.repository.SportQuickLinkExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import java.time.Instant;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;

@Repository
public class SportQuickLinkExtendedRepositoryImpl implements SportQuickLinkExtendedRepository {

  private MongoTemplate mongoTemplate;

  @Autowired
  public SportQuickLinkExtendedRepositoryImpl(MongoTemplate mongoTemplate) {
    this.mongoTemplate = mongoTemplate;
  }

  @Override
  public List<SportQuickLink> findAll(String brand) {
    Query query = createQuery(brand, null);
    return mongoTemplate.find(query, SportQuickLink.class);
  }

  @Override
  public List<SportQuickLink> findAll(String brand, Integer sportId) {
    Query query = createQuery(brand, sportId);
    return mongoTemplate.find(query, SportQuickLink.class);
  }

  private Query createQuery(String brand, Integer sportId) {
    Query query = new Query();
    setCriteria(query, brand, sportId);
    query.with(SortableService.SORT_BY_SORT_ORDER_ASC);
    return query;
  }

  private Criteria setCriteria(Query query, String brand, Integer sportId) {
    Instant now = Instant.now();
    Criteria criteria =
        Criteria.where("disabled")
            .is(false)
            .and("brand")
            .is(brand)
            .and("destination")
            .ne("")
            .and("validityPeriodEnd")
            .gt(now)
            .and("validityPeriodStart")
            .lt(now);

    if (sportId != null) {
      criteria.and("sportId").is(sportId);
    }

    query.addCriteria(criteria);
    return criteria;
  }
}
