package com.coral.oxygen.middleware.featured.controller;

import com.coral.oxygen.middleware.common.service.AssetManagementService;
import com.coral.oxygen.middleware.pojos.model.output.AssetManagement;
import java.util.Arrays;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mockito;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
public class AssetManagementControllerTest {

  @MockBean private AssetManagementService assetManagementService;

  @InjectMocks private AssetManagementController assetManagementController;

  @Before
  public void init() {
    assetManagementController = new AssetManagementController(assetManagementService);
    Mockito.when(assetManagementService.findAll()).thenReturn(Arrays.asList(getAssetManagement()));
  }

  @Test
  public void testGetAll() throws Exception {
    Iterable<AssetManagement> assetManagements = assetManagementController.getAll();
    Assert.assertNotNull(assetManagements);
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
