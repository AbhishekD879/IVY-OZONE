package com.coral.oxygen.middleware.common.service;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.middleware.common.scheduler.AssetManagementScheduler;
import com.coral.oxygen.middleware.pojos.model.output.AssetManagement;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mockito;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
public class AssetManagementScheduleTest {

  @MockBean private AssetManagementService assetManagementService;
  @MockBean private CmsService cmsService;

  @InjectMocks private AssetManagementScheduler assetManagementScheduler;

  @Before
  public void init() {
    assetManagementScheduler = new AssetManagementScheduler(cmsService, assetManagementService);
  }

  @Test
  public void tstDoJob() {
    AssetManagement asset1 = getAssetManagement();
    asset1.setHighlightCarouselToggle(true);
    Assertions.assertDoesNotThrow(() -> assetManagementScheduler.doJob());
  }

  @Test
  public void tstDoJobForException() {
    AssetManagement asset1 = getAssetManagement();
    asset1.setHighlightCarouselToggle(true);
    Mockito.when(cmsService.getAssetManagementInfoByBrand()).thenThrow(new RuntimeException());
    Assertions.assertDoesNotThrow(() -> assetManagementScheduler.doJob());
  }

  private AssetManagement getAssetManagement() {
    AssetManagement assetManagement = new AssetManagement();
    assetManagement.setSportId(16);
    assetManagement.setId("1");
    assetManagement.setPrimaryColour("#454454");
    assetManagement.setTeamName("Liverpool");
    assetManagement.setSecondaryNames(List.of("Liverpool1"));

    return assetManagement;
  }
}
