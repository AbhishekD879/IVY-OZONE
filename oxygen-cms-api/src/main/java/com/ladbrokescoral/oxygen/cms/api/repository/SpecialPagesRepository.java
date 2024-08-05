package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.SpecialPage;
import java.util.Optional;

public interface SpecialPagesRepository<T> extends CustomMongoRepository<SpecialPage> {
  Optional<SpecialPage> findByPageName(String pageName);

  void deleteByPageName(String pageName);
}
