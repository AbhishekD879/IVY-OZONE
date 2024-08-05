package com.ladbrokescoral.oxygen.cms.api.repository.impl;

import com.ladbrokescoral.oxygen.cms.api.entity.MarketLink;
import com.ladbrokescoral.oxygen.cms.api.repository.CustomMongoRepository;
import java.util.List;

public interface MarketLinkRepository extends CustomMongoRepository<MarketLink> {

  List<MarketLink> findByBrandEqualsAndEnabledTrue(String brand);
}
