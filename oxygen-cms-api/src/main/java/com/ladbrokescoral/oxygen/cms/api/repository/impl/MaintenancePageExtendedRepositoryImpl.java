package com.ladbrokescoral.oxygen.cms.api.repository.impl;

import com.ladbrokescoral.oxygen.cms.api.entity.MaintenancePage;
import com.ladbrokescoral.oxygen.cms.api.repository.MaintenancePageExtendedRepository;
import java.time.Instant;
import java.util.Arrays;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;

@Repository
public class MaintenancePageExtendedRepositoryImpl implements MaintenancePageExtendedRepository {

  private static final List<String> SUPPORTED_DEVICES =
      Arrays.asList("mobile", "tablet", "desktop");
  public static final String BRAND_PROPERTY = "brand";
  public static final String VALIDITY_PERIOD_END_PROPERTY = "validityPeriodEnd";
  public static final String VALIDITY_PERIOD_START_PROPERTY = "validityPeriodStart";

  private MongoTemplate mongoTemplate;

  @Autowired
  public MaintenancePageExtendedRepositoryImpl(MongoTemplate mongoTemplate) {
    this.mongoTemplate = mongoTemplate;
  }

  @Override
  public List<MaintenancePage> findMaintenancePages(String brand, String deviceType) {
    if (!SUPPORTED_DEVICES.contains(deviceType)) {
      deviceType = "mobile";
    }

    Query query = new Query();
    query.addCriteria(
        Criteria.where(BRAND_PROPERTY)
            .is(brand)
            .and(deviceType)
            .is(true)
            .and(VALIDITY_PERIOD_END_PROPERTY)
            .gt(Instant.now()));
    query.with(Sort.by(VALIDITY_PERIOD_START_PROPERTY));

    return mongoTemplate.find(query, MaintenancePage.class);
  }

  @Override
  public List<MaintenancePage> findMaintenancePagesWithEndDateAfter(String brand, Instant endDate) {
    Query query = new Query();
    query.addCriteria(
        Criteria.where(BRAND_PROPERTY).is(brand).and(VALIDITY_PERIOD_END_PROPERTY).gt(endDate));
    query.with(Sort.by(VALIDITY_PERIOD_START_PROPERTY));

    return mongoTemplate.find(query, MaintenancePage.class);
  }
}
