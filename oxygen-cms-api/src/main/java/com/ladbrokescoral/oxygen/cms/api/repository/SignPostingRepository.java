package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.SignPosting;
import java.util.List;
import java.util.Optional;

public interface SignPostingRepository extends CustomMongoRepository<SignPosting> {
  Optional<SignPosting> findOneByBrand(String brand);

  List<SignPosting> findAllByBrandOrderBySortOrderAsc(String brand);
}
