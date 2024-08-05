package com.coral.oxygen.middleware.featured.aem.model;

import static org.junit.Assert.assertEquals;

import com.coral.oxygen.middleware.pojos.model.cms.featured.AemBannersConfig;
import com.coral.oxygen.middleware.pojos.model.cms.featured.AemBannersConfig.SportPageId;
import com.coral.oxygen.middleware.pojos.model.output.featured.FeaturedRawIndex.PageType;
import org.junit.Test;

public class AemBannersRawKeyTest {

  @Test
  public void testFromPageId_sport() {
    SportPageId spi =
        AemBannersConfig.SportPageId.builder()
            .pageType(PageType.sport)
            .id("2")
            .type("AEM_BANNERS")
            .moduleDataId(1)
            .build();
    assertEquals("2", AemBannersRawKey.fromPageId(spi).getPageId());
    assertEquals("carousel1", AemBannersRawKey.fromPageId(spi).getCarouselId());
  }

  @Test
  public void testFromPageId_eventhub() {
    SportPageId spi =
        AemBannersConfig.SportPageId.builder()
            .pageType(PageType.eventhub)
            .id("2")
            .type("AEM_BANNERS")
            .moduleDataId(1)
            .build();
    assertEquals("h2", AemBannersRawKey.fromPageId(spi).getPageId());
    assertEquals("carousel1", AemBannersRawKey.fromPageId(spi).getCarouselId());
  }

  @Test
  public void stripJcrKey() {
    assertEquals("football", AemBannersRawKey.stripJcrKey("coral:allowed-pages/football"));
    assertEquals("carousel2", AemBannersRawKey.stripJcrKey("coral:carousels/carousel2"));
  }
}
