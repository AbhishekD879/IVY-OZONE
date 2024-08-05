package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.BottomMenu;
import java.util.List;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.repository.Query;

public interface BottomMenuRepository
    extends CustomMongoRepository<BottomMenu>, FindByRepository<BottomMenu> {

  @Query("{\"brand\":?0, \"disabled\": false, \"section\" : {\"$ne\" : \"quickLinks\"}}")
  List<BottomMenu> findAllByBrand(String brand, Sort sorting);
}
