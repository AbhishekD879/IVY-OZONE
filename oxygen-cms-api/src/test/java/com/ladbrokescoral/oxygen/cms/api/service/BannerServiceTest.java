package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.*;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.Banner;
import com.ladbrokescoral.oxygen.cms.api.repository.BannerRepository;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class BannerServiceTest {

  @Mock private BannerRepository repository;
  @Mock private SportCategoryService sportCategoryService;
  BannerService service;
  Banner banner;

  @Before
  public void init() throws Exception {
    service = new BannerService(repository, sportCategoryService);

    banner = TestUtil.deserializeWithJackson("test/banner.json", Banner.class);
    doReturn(Optional.of(banner)).when(repository).findById("bannerId");
    doReturn(banner).when(repository).save(banner);
  }

  @Test
  public void saveTest() {
    service.save(banner);
    verify(repository, times(1)).save(banner);
  }

  @Test
  public void findOneTest() {
    Optional<Banner> bannerOpt = service.findOne("bannerId");
    verify(repository, times(1)).findById("bannerId");
    assertEquals(banner, bannerOpt.get());
  }

  @Test
  public void findAllTest() {
    doReturn(Collections.singletonList(banner)).when(repository).findAll();
    List<Banner> banners = service.findAll();
    verify(repository, times(1)).findAll();
    assertTrue(banners.contains(banner));
  }

  @Test
  public void findByBrandTest() {
    String brand = "testBrand";
    doReturn(Collections.singletonList(banner))
        .when(repository)
        .findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC);
    List<Banner> banners = service.findByBrand(brand);
    verify(repository, times(1)).findByBrand(brand, SortableService.SORT_BY_SORT_ORDER_ASC);
    assertTrue(banners.contains(banner));
  }

  @Test
  public void prepareModelBeforeSaveTest() {
    assertNull(banner.getVipLevels());
    assertNull(banner.getImageTitleBrand());
    Banner updatedBanner = service.prepareModelBeforeSave(banner);
    assertNull(updatedBanner.getVipLevels());
    assertNotNull(updatedBanner.getImageTitleBrand());
  }

  @Test
  public void updateTest() {
    Banner updated = service.update(new Banner(), banner);
    assertEquals(banner, updated);
  }
}
