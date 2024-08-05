package com.ladbrokescoral.oxygen.cms.api.mapping;

import static org.junit.Assert.assertEquals;

import com.ladbrokescoral.oxygen.cms.api.dto.AemBannersDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SportPageId;
import com.ladbrokescoral.oxygen.cms.api.entity.AemBannersConfig;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import java.time.Instant;
import org.junit.Test;

public class AemBannerDataMapperTest {

  final String title = "Banner #1";
  final Instant displayFrom = Instant.parse("2019-10-10T10:39:20.640Z");
  final Instant displayTo = Instant.parse("2019-10-11T10:39:20.640Z");
  final Integer maxOffers = 7;
  final Integer timePerSlide = 8;

  @Test
  public void toDtoTest_OK() {
    SportModule sportModule = createSportModule();

    AemBannersDto dto = AemBannerDataMapper.INSTANCE.toDto(sportModule);
    assertEquals(
        new SportPageId("0", PageType.eventhub, SportModuleType.AEM_BANNERS, 1), dto.sportPageId());
    assertEquals(title, dto.getTitle());
    assertEquals(maxOffers, dto.getMaxOffers());
    assertEquals(timePerSlide, dto.getTimePerSlide());
    assertEquals(displayFrom, dto.getDisplayFrom());
    assertEquals(displayTo, dto.getDisplayTo());
  }

  private SportModule createSportModule() {
    SportModule sportModule = new SportModule();
    sportModule.setSportId(0);
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
