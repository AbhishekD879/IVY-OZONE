package com.ladbrokescoral.oxygen.cms.api.dto;

import static org.junit.Assert.assertEquals;

import com.ladbrokescoral.oxygen.cms.api.entity.AemBannersConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import java.time.Instant;
import org.junit.Test;

public class SportPageIdTest {

  private final String title = "Banner #1";
  private final Instant displayFrom = Instant.parse("2019-10-10T10:39:20.640Z");
  private final Instant displayTo = Instant.parse("2019-10-11T10:39:20.640Z");
  private final Integer maxOffers = 7;
  private final Integer timePerSlide = 8;
  private final String sportId = "0";

  @Test
  public void extractModuleDataIdForAemBanner() {
    SportPageId spId = SportPageId.fromSportModule(createSportModule());
    assertEquals(sportId, spId.getId());
    assertEquals(PageType.eventhub, spId.getPageType());
    assertEquals(SportModuleType.AEM_BANNERS, spId.getType());
    assertEquals(new Integer(1), spId.getModuleDataId());
  }

  @Test
  public void extractModuleDataIdForCommonModule() {
    SportModule module = createSportModule();
    module.setTitle("Common Module");
    SportPageId spId = SportPageId.fromSportModule(module);
    assertEquals(sportId, spId.getId());
    assertEquals(PageType.eventhub, spId.getPageType());
    assertEquals(SportModuleType.AEM_BANNERS, spId.getType());
    assertEquals(new Integer(0), spId.getModuleDataId());
  }

  @Test
  public void extractModuleDataIdForBrokenTitle() {
    SportModule module = createSportModule();
    module.setTitle("Common #Module#non");
    SportPageId spId = SportPageId.fromSportModule(module);
    assertEquals(sportId, spId.getId());
    assertEquals(PageType.eventhub, spId.getPageType());
    assertEquals(SportModuleType.AEM_BANNERS, spId.getType());
    assertEquals(new Integer(0), spId.getModuleDataId());
  }

  private SportModule createSportModule() {
    SportModule sportModule = new SportModule();
    sportModule.setSportId(Integer.parseInt(sportId));
    sportModule.setModuleType(SportModuleType.AEM_BANNERS);
    sportModule.setPageType(PageType.eventhub);

    sportModule.setTitle(title);

    sportModule.setModuleConfig(
        AemBannersConfig.builder()
            .displayFrom(displayFrom)
            .displayTo(displayTo)
            .maxOffers(maxOffers)
            .timePerSlide(timePerSlide)
            .build());
    return sportModule;
  }
}
