package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.SvgImage;
import java.util.List;

public interface SvgImageRepository extends CustomMongoRepository<SvgImage> {

  List<SvgImage> findAllByBrandAndSprite(String brand, String sprite);
}
