package com.ladbrokescoral.oxygen.cms.api.repository.impl;

import com.ladbrokescoral.oxygen.cms.api.entity.SsoPage;
import com.ladbrokescoral.oxygen.cms.api.repository.SsoPageExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.util.Collections;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.stereotype.Repository;

@Slf4j
@Repository
public class SsoPageExtendedRepositoryImpl implements SsoPageExtendedRepository {

  private MongoTemplate mongoTemplate;

  @Autowired
  public SsoPageExtendedRepositoryImpl(MongoTemplate mongoTemplate) {
    this.mongoTemplate = mongoTemplate;
  }

  @Override
  public List<SsoPage> findSsoPages(String brand, String osType) {
    brand = Util.updateBrand(brand);
    boolean matchingOsTypeFound = false;

    Query query = new Query();
    Criteria criteria = Criteria.where("disabled").is(false).and("brand").is(brand);
    if (osType.equalsIgnoreCase("ios")) {
      criteria.and("showOnIOS").is(true);
      matchingOsTypeFound = true;
    }
    if (osType.equalsIgnoreCase("android")) {
      criteria.and("showOnAndroid").is(true);
      matchingOsTypeFound = true;
    }
    query.addCriteria(criteria);
    query.with(SortableService.SORT_BY_SORT_ORDER_ASC);

    if (!matchingOsTypeFound) {
      log.info("cannot match {} to defined OS types.", osType);
    }

    return matchingOsTypeFound ? mongoTemplate.find(query, SsoPage.class) : Collections.emptyList();
  }
}
