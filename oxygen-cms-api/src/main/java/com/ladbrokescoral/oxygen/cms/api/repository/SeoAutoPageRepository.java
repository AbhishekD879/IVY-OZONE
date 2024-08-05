package com.ladbrokescoral.oxygen.cms.api.repository;

import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoAutoPage;
import java.util.List;

public interface SeoAutoPageRepository extends CustomMongoRepository<SeoAutoPage> {

  @FortifyXSSValidate
  List<SeoAutoPage> findAllByBrand(String brand);
}
