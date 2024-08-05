package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.ModuleRibbonTabDto;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ModuleRibbonTabPublicService;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class ModuleRibbonTabApiTest {

  @Mock ModuleRibbonTabPublicService moduleRibbonTabService;

  private ModuleRibbonTabApi moduleRibbonTabApi;

  @Before
  public void init() throws Exception {
    moduleRibbonTabApi = new ModuleRibbonTabApi(moduleRibbonTabService);

    List<ModuleRibbonTabDto> moduleRibbonTabs =
        TestUtil.deserializeListWithJackson(
            "controller/public_api/moduleRibbonTabMongo.json", ModuleRibbonTabDto.class);
    when(moduleRibbonTabService.findAll()).thenReturn(moduleRibbonTabs);
  }

  @Test
  public void findByBrandTest() throws Exception {
    List<ModuleRibbonTabDto> result = moduleRibbonTabApi.findAll();

    List<ModuleRibbonTabDto> expected =
        TestUtil.deserializeListWithJackson(
            "controller/public_api/moduleRibbonTabDto.json", ModuleRibbonTabDto.class);
    assertEquals(expected, result);
  }
}
