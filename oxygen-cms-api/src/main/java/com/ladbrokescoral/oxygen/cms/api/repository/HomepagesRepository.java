package com.ladbrokescoral.oxygen.cms.api.repository;

import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.entity.Homepage;
import java.util.List;

public interface HomepagesRepository extends CustomMongoRepository<Homepage> {

  @FortifyXSSValidate("return")
  List<Homepage> findAllByOrderBySortOrderAsc();
}
