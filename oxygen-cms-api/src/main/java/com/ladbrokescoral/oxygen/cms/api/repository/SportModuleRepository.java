package com.ladbrokescoral.oxygen.cms.api.repository;

import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import java.util.Collection;
import java.util.EnumSet;
import java.util.List;
import java.util.Optional;

public interface SportModuleRepository
    extends CustomMongoRepository<SportModule>, FindByRepository<SportModule> {

  @Override
  default List<SportModule> findAll() {
    return findAllByModuleTypeIn(EnumSet.allOf(SportModuleType.class));
  }

  @Override
  default List<SportModule> findByBrand(String brand) {
    return findAllByBrandAndModuleTypeIn(brand, EnumSet.allOf(SportModuleType.class));
  }

  List<SportModule> findAllByBrandAndDisabledAndModuleTypeInOrderBySortOrderAsc(
      String brand, Boolean disabled, Collection<SportModuleType> types);

  List<SportModule> findAllByBrandAndModuleTypeOrderBySortOrderAsc(
      String brand, SportModuleType moduleType);

  List<SportModule> findAllByBrandAndModuleTypeAndDisabledFalseOrderBySortOrderAsc(
      String brand, SportModuleType moduleType);

  List<SportModule> findAllByBrandAndPageTypeAndPageIdAndModuleTypeInOrderBySortOrderAsc(
      String brand, PageType pageType, String pageId, Collection<SportModuleType> types);

  Optional<SportModule> findAllByBrandAndPageTypeAndPageIdAndModuleType(
      String brand, PageType pageType, String sportId, SportModuleType moduleType);

  void deleteAllByBrandAndPageTypeAndPageId(String brand, PageType pageType, String pageId);

  List<SportModule> findAllByBrandAndModuleTypeIn(String brand, Collection<SportModuleType> types);

  List<SportModule> findAllByModuleTypeIn(Collection<SportModuleType> types);

  List<SportModule> findAllByBrandAndSportId(String brand, Integer sportId);
}
