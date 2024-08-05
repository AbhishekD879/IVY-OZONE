package com.ladbrokescoral.oxygen.cms.api.repository.impl;

import com.ladbrokescoral.oxygen.cms.api.entity.Offer;
import com.ladbrokescoral.oxygen.cms.api.repository.OfferExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import java.time.Instant;
import java.util.List;
import org.bson.types.ObjectId;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;

@Repository
public class OfferExtendedRepositoryImpl implements OfferExtendedRepository {

  private MongoTemplate mongoTemplate;

  @Autowired
  public OfferExtendedRepositoryImpl(MongoTemplate mongoTemplate) {
    this.mongoTemplate = mongoTemplate;
  }

  @Override
  public List<Offer> findOffers(String brand, String deviceType, List<ObjectId> moduleIds) {
    Query query = new Query();
    query.addCriteria(
        Criteria.where("disabled")
            .is(false)
            .and("brand")
            .is(brand)
            .and("showOfferOn")
            .in(deviceType, "both")
            .and("module")
            .in(moduleIds)
            .and("displayTo")
            .gt(Instant.now()));
    query.with(SortableService.SORT_BY_SORT_ORDER_ASC);

    return mongoTemplate.find(query, Offer.class);
  }
}
