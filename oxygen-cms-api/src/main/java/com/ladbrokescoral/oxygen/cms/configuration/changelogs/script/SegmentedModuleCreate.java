package com.ladbrokescoral.oxygen.cms.configuration.changelogs.script;

import com.github.cloudyrock.mongock.driver.mongodb.springdata.v3.decorator.impl.MongockTemplate;
import com.ladbrokescoral.oxygen.cms.api.entity.DeviceType;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.HighlightCarousel;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.ModuleRibbonTab;
import com.ladbrokescoral.oxygen.cms.api.entity.NavigationPoint;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportQuickLink;
import com.ladbrokescoral.oxygen.cms.api.entity.SurfaceBet;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentedModule;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;

@Slf4j
public class SegmentedModuleCreate extends AbstractBrandMongoUpdate {

  private static final String COLLECTION_NAME = "segmentedModules";

  private final Class<?>[] moduleClassArray =
      new Class[] {
        SurfaceBet.class,
        SportQuickLink.class,
        HighlightCarousel.class,
        FooterMenu.class,
        NavigationPoint.class,
        HomeModule.class,
        ModuleRibbonTab.class
      };

  public void addSegmentedModule(MongockTemplate mongockTemplate) {
    // Do nothing as we are going to create the Segments/segmentedModules specific to Brand. Not
    // deleting the Changelog as it is executed in some environments already.
    // Data clean up will taken care while adding the records with respect to brand.
  }

  public void addSegmentedModule(MongockTemplate mongockTemplate, String brand) {

    List<SegmentedModule> listSegment =
        Arrays.stream(moduleClassArray)
            .parallel()
            .map(
                mclass ->
                    SegmentedModule.builder()
                        .moduleName(mclass.getSimpleName())
                        .channel(DeviceType.MOBILE)
                        .pageId("0")
                        .pageType(PageType.sport)
                        .brand(brand)
                        .build())
            .collect(Collectors.toList());

    mongockTemplate.insert(listSegment, COLLECTION_NAME);
  }
}
