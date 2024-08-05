package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.dto.BrandMenuItemDto;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;

public class BybMenuUpdate extends AbstractBrandMongoUpdate {

  public void updateBybMenu(MongockTemplate mongockTemplate, String brand) {
    updateBrandMenuItems(mongockTemplate, brand, "/byb", initBybMenuItems());
    removeYcMenu(mongockTemplate, brand);
  }

  public void addAssetManagementMenu(MongockTemplate mongockTemplate, String brand) {
    updateBrandMenuItems(
        mongockTemplate,
        brand,
        "/byb",
        Collections.singletonList(
            createBrandMenuItemBuilder("Asset Management", "/byb/asset-management").build()));
  }

  private void removeYcMenu(MongockTemplate mongockTemplate, String brand) {
    removeBrandMenuItem(mongockTemplate, brand, "/yc");
  }

  private List<BrandMenuItemDto> initBybMenuItems() {
    return Arrays.asList(
        createBrandMenuItemBuilder("Banach Leagues", "/yc/yc-leagues").build(),
        createBrandMenuItemBuilder("BYB Static Blocks", "/yc/yc-static-blocks").build(),
        createBrandMenuItemBuilder("5 A Side", "/byb/5aSide").build());
  }
}
