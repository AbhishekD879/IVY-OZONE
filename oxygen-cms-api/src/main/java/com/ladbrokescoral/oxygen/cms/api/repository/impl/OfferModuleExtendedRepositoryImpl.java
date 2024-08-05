package com.ladbrokescoral.oxygen.cms.api.repository.impl;

import com.ladbrokescoral.oxygen.cms.api.entity.OfferModule;
import com.ladbrokescoral.oxygen.cms.api.repository.OfferModuleExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;

@Repository
public class OfferModuleExtendedRepositoryImpl implements OfferModuleExtendedRepository {

  private MongoTemplate mongoTemplate;

  @Autowired
  public OfferModuleExtendedRepositoryImpl(MongoTemplate mongoTemplate) {
    this.mongoTemplate = mongoTemplate;
  }

  @Override
  public List<OfferModule> findAllByBrandAndDeviceType(String brand, String deviceType) {
    Query query = new Query();
    query.addCriteria(
        Criteria.where("disabled")
            .is(false)
            .and("brand")
            .is(brand)
            .and("showModuleOn")
            .in(deviceType, "both"));
    query.with(SortableService.SORT_BY_SORT_ORDER_ASC);

    return mongoTemplate.find(query, OfferModule.class);
  }
}
