package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.dto.BrandMenuItemDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BrandMenuStructure;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.Set;
import java.util.UUID;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.mongodb.core.query.Criteria;
import org.springframework.data.mongodb.core.query.Query;
import org.springframework.data.mongodb.core.query.Update;

@Slf4j
public abstract class AbstractBrandMongoUpdate {

  private static final String BRAND_MENU_COLLECTION_NAME = "brandMenu";

  protected void updateBrandMenu(
      MongockTemplate mongockTemplate, String brand, BrandMenuItemDto menuItem) {
    log.info("Update of {} has started", menuItem.getLabel());
    Optional<BrandMenuStructure> brandMenu =
        findByBrand(mongockTemplate, brand, BRAND_MENU_COLLECTION_NAME, BrandMenuStructure.class);
    brandMenu.ifPresent(
        menu -> {
          Optional<BrandMenuItemDto> any =
              menu.getMenu().stream()
                  .filter(item -> menuItem.getPath().equalsIgnoreCase(item.getPath()))
                  .findFirst();
          if (!any.isPresent()) {
            menu.getMenu().add(menuItem);

            updateBrandMenu(mongockTemplate, brand, menu);
          }
        });
  }

  protected void updateBrandMenuItems(
      MongockTemplate mongockTemplate,
      String brand,
      String menuPath,
      List<BrandMenuItemDto> brandMenuItems) {
    Optional<BrandMenuStructure> brandMenu =
        findByBrand(mongockTemplate, brand, BRAND_MENU_COLLECTION_NAME, BrandMenuStructure.class);
    brandMenu.ifPresent(
        menu -> {
          Optional<BrandMenuItemDto> any =
              menu.getMenu().stream()
                  .filter(item -> menuPath.equalsIgnoreCase(item.getPath()))
                  .findFirst();
          if (any.isPresent()) {
            List<BrandMenuItemDto> subMenus = any.get().getSubMenu();
            Set<String> existingMenus =
                subMenus.stream().map(BrandMenuItemDto::getPath).collect(Collectors.toSet());

            for (BrandMenuItemDto newItem : brandMenuItems) {
              if (!existingMenus.contains(newItem.getPath())) {
                subMenus.add(newItem);
              }
            }

            updateBrandMenu(mongockTemplate, brand, menu);
          }
        });
  }

  protected void removeBrandMenuItem(
      MongockTemplate mongockTemplate, String brand, String menuPath) {
    Optional<BrandMenuStructure> brandMenu =
        findByBrand(mongockTemplate, brand, BRAND_MENU_COLLECTION_NAME, BrandMenuStructure.class);
    brandMenu.ifPresent(
        menu -> {
          Optional<BrandMenuItemDto> any =
              menu.getMenu().stream()
                  .filter(item -> menuPath.equalsIgnoreCase(item.getPath()))
                  .findFirst();
          any.ifPresent(brandMenuItemDto -> menu.getMenu().remove(brandMenuItemDto));
          updateBrandMenu(mongockTemplate, brand, menu);
        });
  }

  protected BrandMenuItemDto.BrandMenuItemDtoBuilder createBrandMenuItemBuilder(
      String label, String path) {
    return BrandMenuItemDto.builder()
        .label(label)
        .path(path)
        .active(true)
        .id(UUID.randomUUID().toString())
        .subMenu(Collections.emptyList());
  }

  private void updateBrandMenu(
      MongockTemplate mongockTemplate, String brand, BrandMenuStructure menu) {
    Query query = getFindByBrandQuery(brand);
    Update update = new Update();
    update.set("menu", menu.getMenu());

    mongockTemplate.updateFirst(query, update, BRAND_MENU_COLLECTION_NAME);
  }

  protected <T extends HasBrand> Optional<T> findByBrand(
      MongockTemplate mongockTemplate, String brand, String collectionName, Class<T> entityClass) {
    return findAllByBrand(mongockTemplate, brand, collectionName, entityClass).stream().findFirst();
  }

  protected <T extends HasBrand> List<T> findAllByBrand(
      MongockTemplate mongockTemplate, String brand, String collectionName, Class<T> entityClass) {
    Query query = getFindByBrandQuery(brand);
    return mongockTemplate.find(query, entityClass, collectionName);
  }

  protected <T extends HasBrand> List<T> findAllByBrand(
      MongockTemplate mongockTemplate, String brand, Class<T> entityClass) {
    Query query = getFindByBrandQuery(brand);
    return mongockTemplate.find(query, entityClass);
  }

  protected Query getFindByBrandQuery(String brand) {
    return getFindByCriteriaQuery("brand", brand);
  }

  private Query getFindByCriteriaQuery(String parameter, String value) {
    Query query = new Query();
    query.addCriteria(Criteria.where(parameter).is(value));
    return query;
  }

  protected <T extends HasBrand> List<T> findByBrandAndTabName(
      MongockTemplate mongockTemplate,
      String brand,
      String tabName,
      String collectionName,
      Class<T> entityClass) {
    Query query = getFindByBrandQuery(brand);
    query.addCriteria(Criteria.where("name").is(tabName));
    return mongockTemplate.find(query, entityClass, collectionName);
  }
}
