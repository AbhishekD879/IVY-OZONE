package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.ModuleRibbonTabDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ModuleRibbonTab;
import com.ladbrokescoral.oxygen.cms.api.service.BybTabAvailabilityService;
import com.ladbrokescoral.oxygen.cms.api.service.ModuleRibbonTabService;
import java.io.IOException;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class ModuleRibbonTabPublicServiceTest {

  @Mock private ModuleRibbonTabService moduleRibbonTabService;

  @Mock private BybTabAvailabilityService bybTabAvailabilityService;

  @InjectMocks private ModuleRibbonTabPublicService moduleRibbonTabPublicService;

  @Before
  public void init() throws IOException {
    List<ModuleRibbonTab> moduleRibbonTabs =
        TestUtil.deserializeListWithJackson(
            "controller/public_api/moduleRibbonTabMongo.json", ModuleRibbonTab.class);

    Mockito.when(moduleRibbonTabService.findAllUniversalModuleRibbonTabs())
        .thenReturn(moduleRibbonTabs);
  }

  @Test
  public void testFindAll() {
    List<ModuleRibbonTabDto> moduleRibbonTabDtos = moduleRibbonTabPublicService.findAll();
    Assert.assertNotNull(moduleRibbonTabDtos);
    Assert.assertSame(2, moduleRibbonTabDtos.size());
  }
}
