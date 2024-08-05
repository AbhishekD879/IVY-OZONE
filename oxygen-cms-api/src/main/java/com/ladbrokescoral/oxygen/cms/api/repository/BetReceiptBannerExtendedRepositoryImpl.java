package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.BetReceiptBanner;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.data.mongodb.core.MongoTemplate;
import org.springframework.stereotype.Repository;

@Qualifier("betReceipt")
@Repository
public class BetReceiptBannerExtendedRepositoryImpl
    implements BetReceiptBannerExtendedRepository<BetReceiptBanner> {

  private MongoTemplate mongoTemplate;

  @Autowired
  public BetReceiptBannerExtendedRepositoryImpl(MongoTemplate mongoTemplate) {
    this.mongoTemplate = mongoTemplate;
  }

  @Override
  public List<BetReceiptBanner> findBetReceiptBanners(String brand) {
    return mongoTemplate.find(createBetReceiptBannerQuery(brand), BetReceiptBanner.class);
  }
}
