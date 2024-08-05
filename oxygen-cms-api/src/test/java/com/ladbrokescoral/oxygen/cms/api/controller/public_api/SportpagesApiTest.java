package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.service.public_api.SportPagePublicService;
import java.util.ArrayList;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SportpagesApiTest {

  @Mock private SportPagePublicService sportPagePublicService;

  private SportPageApi sportPageApi;

  @Before
  public void init() {

    sportPageApi = new SportPageApi(sportPagePublicService);
  }

  @Test
  public void testFindByBrand() throws Exception {
    when(sportPagePublicService.findAllPagesByBrand("bma", 0)).thenReturn(new ArrayList<>());
    sportPageApi.findAllPagesByBrand("bma", Optional.empty());
    verify(sportPagePublicService, times(1)).findAllPagesByBrand("bma", 0);
  }

  @Test
  public void testFindByBrandWithLastUpdatedTime() throws Exception {
    Optional<Long> lastRun = Optional.of(System.currentTimeMillis());
    when(sportPagePublicService.findAllPagesByBrand("bma", lastRun.get()))
        .thenReturn(new ArrayList<>());
    sportPageApi.findAllPagesByBrand("bma", lastRun);
    verify(sportPagePublicService, times(1)).findAllPagesByBrand("bma", lastRun.get());
  }
}
