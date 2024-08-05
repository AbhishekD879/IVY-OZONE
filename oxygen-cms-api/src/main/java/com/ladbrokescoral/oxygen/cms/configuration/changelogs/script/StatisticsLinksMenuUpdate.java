package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.dto.BrandMenuItemDto;
import java.util.Arrays;
import java.util.List;
import java.util.UUID;

public class StatisticsLinksMenuUpdate extends AbstractBrandMongoUpdate {

  private static final int DISPLAY_ORDER = 10;

  public void init(MongockTemplate mongockTemplate, String brand) {
    updateBrandMenu(
        mongockTemplate,
        brand,
        BrandMenuItemDto.builder()
            .path("statistics-links")
            .active(true)
            .id(UUID.randomUUID().toString())
            .label("Scoreboard Statistics Links")
            .icon("show_chart")
            .displayOrder(DISPLAY_ORDER)
            .subMenu(initStatisticsLinksSubMenus())
            .build());
  }

  private List<BrandMenuItemDto> initStatisticsLinksSubMenus() {
    return Arrays.asList(
        createBrandMenuItemBuilder("League Links", "/statistics-links/league-links").build(),
        createBrandMenuItemBuilder("Market Links", "/statistics-links/market-links").build());
  }
}
