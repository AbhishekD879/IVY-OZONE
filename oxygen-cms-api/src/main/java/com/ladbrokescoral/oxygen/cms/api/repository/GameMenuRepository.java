package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.GameMenu;
import java.util.List;

public interface GameMenuRepository extends CustomMongoRepository<GameMenu> {

  List<GameMenu> findAllByUrl(String url);

  List<GameMenu> findAllByUrlAndBrand(String url, String brand);
}
