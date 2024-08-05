package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.junit.Assert.assertEquals;
import static org.junit.jupiter.api.Assertions.assertNotNull;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.entity.BetPackBanner;
import com.ladbrokescoral.oxygen.cms.api.repository.BetPackEnablerBannerRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.CustomMongoRepository;
import com.ladbrokescoral.oxygen.cms.api.service.*;
import java.util.Collections;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class BetPackMarketPlacePublicBannerServiceTest {

  @Mock private CustomMongoRepository<BetPackBanner> mongoRepository;
  @Mock private BetPackEnablerBannerRepository betPackEnablerBannerRepository;

  private BetPackMarketPlacePublicBannerService service;
  @Mock private ImageService imageService;
  @Spy BetPackBanner banner;

  @Before
  public void init() {
    BetPackMarketPlaceBannerService betPackMarketPlaceBannerService =
        new BetPackMarketPlaceBannerService(
            betPackEnablerBannerRepository, imageService, "image/path/betPackBanner");
    service = new BetPackMarketPlacePublicBannerService(betPackMarketPlaceBannerService);
  }

  @Test
  public void testFindByBrand() {
    // arrange
    String brand = "bma";

    when(betPackEnablerBannerRepository.findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC))
        .thenReturn(Collections.singletonList(banner));

    // act
    List<BetPackBanner> list = service.getBetPackBannerByBrand(brand);

    // arrange
    assertEquals(1, list.size());
    BetPackBanner banner = list.iterator().next();
    assertEquals(banner.getBrand(), banner.getBrand());
    assertNotNull(banner);
  }
}
