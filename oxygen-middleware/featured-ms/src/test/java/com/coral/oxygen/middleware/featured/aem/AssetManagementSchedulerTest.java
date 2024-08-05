package com.coral.oxygen.middleware.featured.aem;

import com.coral.oxygen.cms.api.CmsService;
import com.coral.oxygen.middleware.common.scheduler.AssetManagementScheduler;
import com.coral.oxygen.middleware.common.service.AssetManagementService;
import com.coral.oxygen.middleware.pojos.model.output.AssetManagement;
import java.util.Arrays;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mockito;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
public class AssetManagementSchedulerTest {

  @MockBean private CmsService cmsService;

  @MockBean private AssetManagementService assetManagementService;

  @InjectMocks private AssetManagementScheduler assetManagementScheduler;

  @Before
  public void init() {
    assetManagementScheduler = new AssetManagementScheduler(cmsService, assetManagementService);
    Mockito.when(assetManagementService.saveAll(Arrays.asList(getAssetManagement())))
        .thenReturn(Arrays.asList(getAssetManagement()));
    Mockito.when(cmsService.getAssetManagementInfoByBrand())
        .thenReturn(Arrays.asList(getAssetManagement()));
  }

  @Test
  public void testSaveAll() {
    assetManagementScheduler.doJob();
    Mockito.verify(cmsService, Mockito.times(1)).getAssetManagementInfoByBrand();
    Mockito.verify(assetManagementService, Mockito.times(1)).saveAll(Mockito.anyList());
  }

  @Test
  public void testSaveAllForException() {
    Mockito.when(assetManagementService.saveAll(Mockito.anyList()))
        .thenThrow(new RuntimeException());
    assetManagementScheduler.doJob();
    Mockito.verify(cmsService, Mockito.times(1)).getAssetManagementInfoByBrand();
    Mockito.verify(assetManagementService, Mockito.times(1)).saveAll(Mockito.anyList());
  }

  private AssetManagement getAssetManagement() {
    AssetManagement assetManagement = new AssetManagement();
    assetManagement.setSportId(16);
    assetManagement.setId("1");
    assetManagement.setPrimaryColour("#454454");
    assetManagement.setTeamName("Liverpool");
    assetManagement.setSecondaryNames(Arrays.asList("Liverpool1"));
    return assetManagement;
  }
}
