package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.Widget;
import java.util.Optional;

public interface WidgetRepository extends CustomMongoRepository<Widget>, FindByRepository<Widget> {

  Optional<Widget> findOneByBrandAndType(String brand, String type);
}
