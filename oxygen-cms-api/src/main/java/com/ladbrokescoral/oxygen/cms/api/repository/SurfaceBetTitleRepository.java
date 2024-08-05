package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBetTitle;
import org.springframework.stereotype.Repository;

@Repository
public interface SurfaceBetTitleRepository extends CustomMongoRepository<SurfaceBetTitle> {
  SurfaceBetTitle findByTitle(String title);

  SurfaceBetTitle findByBrandAndId(String brand, String id);

  void deleteByBrandAndId(String brand, String id);
}
