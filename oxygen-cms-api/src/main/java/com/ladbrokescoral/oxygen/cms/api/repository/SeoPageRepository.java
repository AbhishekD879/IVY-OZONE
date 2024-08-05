package com.ladbrokescoral.oxygen.cms.api.repository;

import com.fortify.annotations.FortifyDatabaseSource;
import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoPage;
import java.util.List;
import java.util.Optional;

public interface SeoPageRepository extends CustomMongoRepository<SeoPage> {

  @FortifyDatabaseSource
  @FortifyXSSValidate
  Optional<SeoPage> findOneByIdAndAndBrand(String id, String brand);

  @FortifyXSSValidate
  List<SeoPage> findAllByBrandAndDisabled(String brand, Boolean disabled);
}
