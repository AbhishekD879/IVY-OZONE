package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.dto.BrandMenuItemDto;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.UUID;

public class SportPagesMenuUpdate extends AbstractBrandMongoUpdate {

  public void initSportPagesMenu(MongockTemplate mongockTemplate, String brand) {
    updateBrandMenu(
        mongockTemplate,
        brand,
        BrandMenuItemDto.builder()
            .path("sports-pages")
            .active(true)
            .id(UUID.randomUUID().toString())
            .label("Sports Pages")
            .icon("directions_run")
            .displayOrder(3)
            .subMenu(initSportPagesMenuItems())
            .build());
  }

  public void addSportPagesSubMenus(MongockTemplate mongockTemplate, String brand) {
    updateBrandMenuItems(mongockTemplate, brand, "sports-pages", initSportPagesMenuItems());
  }

  private List<BrandMenuItemDto> initSportPagesMenuItems() {
    return Arrays.asList(
        createBrandMenuItemBuilder("Homepage", "/sports-pages/homepage")
            .subMenu(
                Collections.singletonList(
                    BrandMenuItemDto.builder()
                        .path("/sports-quick-link")
                        .label("Sports quick link")
                        .active(true)
                        .id(UUID.randomUUID().toString())
                        .build()))
            .build(),
        createBrandMenuItemBuilder("Sport Categories", "/sports-pages/sport-categories").build(),
        createBrandMenuItemBuilder("Super Button", "/quick-links/navigation-points").build(),
        createBrandMenuItemBuilder("Event Hub", "/sports-pages/event-hub").displayOrder(0).build(),
        createBrandMenuItemBuilder("Big Competitions", "/sports-pages/big-competition").build(),
        createBrandMenuItemBuilder("Olympic Sports", "/sports-pages/olympics-pages").build());
  }
}
