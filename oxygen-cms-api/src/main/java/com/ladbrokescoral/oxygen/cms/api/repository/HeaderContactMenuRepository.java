package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.HeaderContactMenu;
import java.util.List;
import org.springframework.data.domain.Sort;
import org.springframework.data.mongodb.repository.Query;

public interface HeaderContactMenuRepository
    extends CustomMongoRepository<HeaderContactMenu>, FindByRepository<HeaderContactMenu> {

  @Query("{\"brand\":?0, \"disabled\": false}")
  List<HeaderContactMenu> findAllByBrand(String brand, Sort sorting);
}
