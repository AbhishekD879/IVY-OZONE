package com.ladbrokescoral.oxygen.cms.api.repository.impl;

import com.ladbrokescoral.oxygen.cms.api.entity.BetReceiptBannerTablet;
import com.ladbrokescoral.oxygen.cms.api.repository.BetReceiptBannerExtendedRepository;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Repository;

@Qualifier("betReceiptTablet")
@Repository
public class BetReceiptBannerTabletExtendedRepositoryImpl
    implements BetReceiptBannerExtendedRepository<BetReceiptBannerTablet> {

  private MongoTemplate mongoTemplate;

  @Autowired
  public BetReceiptBannerTabletExtendedRepositoryImpl(MongoTemplate mongoTemplate) {
    this.mongoTemplate = mongoTemplate;
  }

  @Override
  public List<BetReceiptBannerTablet> findBetReceiptBanners(String brand) {
    return mongoTemplate.find(createBetReceiptBannerQuery(brand), BetReceiptBannerTablet.class);
  }
}
