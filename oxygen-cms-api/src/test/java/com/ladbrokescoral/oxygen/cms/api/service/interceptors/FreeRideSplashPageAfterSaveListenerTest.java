package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;

import com.ladbrokescoral.oxygen.cms.api.dto.FreeRidePublicSplashPageDto;
import com.ladbrokescoral.oxygen.cms.api.entity.freeride.FreeRideSplashPage;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FreeRideSplashPagePublicService;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

@RunWith(Parameterized.class)
public class FreeRideSplashPageAfterSaveListenerTest
    extends AbstractAfterSaveListenerTest<FreeRideSplashPage> {

  @Mock private FreeRideSplashPagePublicService freeRideSplashPagePublicService;

  @Getter @Mock private FreeRideSplashPage entity;

  @Getter @InjectMocks private FreeRideSplashPageAfterSaveListener listener;

  private String COLLECTION_NAME = "freeride-splashpage";

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"ladbrokes", "api/ladbrokes", "freeride-splashpage"},
          {"connect", "api/connect", "freeride-splashpage"}
        });
  }

  @Before
  public void init() {
    given(freeRideSplashPagePublicService.getFreeRideSplashPageByBrand(anyString()))
        .willReturn(this.getCollection());
  }

  @Test
  public void onAfterSaveTest() {
    assertNotNull(listener);
    listener.onAfterSave(new AfterSaveEvent<FreeRideSplashPage>(entity, null, COLLECTION_NAME));
  }

  @Test
  public void onAfterSaveAllImgUrlNullTest() {
    FreeRideSplashPagePublicService service = Mockito.mock(FreeRideSplashPagePublicService.class);
    FreeRideSplashPageAfterSaveListener freerideListener =
        new FreeRideSplashPageAfterSaveListener(service, context);
    List<FreeRidePublicSplashPageDto> splashPageList = new ArrayList<>();
    FreeRidePublicSplashPageDto splashPageDto = new FreeRidePublicSplashPageDto();
    splashPageList.add(splashPageDto);
    assertNull(splashPageDto.getBannerImageUrl());
    assertNull(splashPageDto.getSplashImageUrl());
    assertNull(splashPageDto.getFreeRideLogoUrl());
    doReturn(splashPageList).when(service).getFreeRideSplashPageByBrand(any());
    freerideListener.onAfterSave(
        new AfterSaveEvent<FreeRideSplashPage>(entity, null, COLLECTION_NAME));
  }

  @Test
  public void onAfterSaveSplashPageAndLogoUrlNullTest() {
    FreeRideSplashPagePublicService service = Mockito.mock(FreeRideSplashPagePublicService.class);
    FreeRideSplashPageAfterSaveListener freerideListener =
        new FreeRideSplashPageAfterSaveListener(service, context);
    List<FreeRidePublicSplashPageDto> splashPageList = new ArrayList<>();
    FreeRidePublicSplashPageDto splashPageDto = new FreeRidePublicSplashPageDto();
    splashPageDto.setBannerImageUrl("/banner/test");
    splashPageList.add(splashPageDto);
    assertNull(splashPageDto.getSplashImageUrl());
    assertNull(splashPageDto.getFreeRideLogoUrl());
    doReturn(splashPageList).when(service).getFreeRideSplashPageByBrand(any());
    freerideListener.onAfterSave(
        new AfterSaveEvent<FreeRideSplashPage>(entity, null, COLLECTION_NAME));
  }

  @Test
  public void onAfterSaveFreeRideLogoNullTest() {
    FreeRideSplashPagePublicService service = Mockito.mock(FreeRideSplashPagePublicService.class);
    FreeRideSplashPageAfterSaveListener freerideListener =
        new FreeRideSplashPageAfterSaveListener(service, context);
    List<FreeRidePublicSplashPageDto> splashPageList = new ArrayList<>();
    FreeRidePublicSplashPageDto splashPageDto = new FreeRidePublicSplashPageDto();
    splashPageDto.setBannerImageUrl("/banner/test");
    splashPageDto.setSplashImageUrl("/FRlogo/png");
    splashPageList.add(splashPageDto);
    assertNull(splashPageDto.getFreeRideLogoUrl());
    doReturn(splashPageList).when(service).getFreeRideSplashPageByBrand(any());
    freerideListener.onAfterSave(
        new AfterSaveEvent<FreeRideSplashPage>(entity, null, COLLECTION_NAME));
  }

  @Override
  protected List<FreeRidePublicSplashPageDto> getCollection() {
    List<FreeRidePublicSplashPageDto> splashPageList = new ArrayList<>();
    FreeRidePublicSplashPageDto freeRidePublicSplashPageDto = new FreeRidePublicSplashPageDto();
    freeRidePublicSplashPageDto.setBrand("BMA");
    freeRidePublicSplashPageDto.setSplashImageUrl("/splash/img");
    freeRidePublicSplashPageDto.setBannerImageUrl("/banner/img");
    freeRidePublicSplashPageDto.setFreeRideLogoUrl("/FRlogo/png");
    splashPageList.add(freeRidePublicSplashPageDto);
    return splashPageList;
  }
}
