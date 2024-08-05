package com.coral.oxygen.middleware.featured.controller;

import com.coral.oxygen.middleware.featured.service.FeaturedDataService;
import java.util.HashSet;
import java.util.Set;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mockito;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
public class FeaturedDataControllerTest {

  @MockBean private FeaturedDataService featuredDataService;

  @InjectMocks private FeaturedDataController featuredDataController;

  @Before
  public void init() {
    featuredDataController = new FeaturedDataController(featuredDataService);
    Mockito.when(featuredDataService.getModuleByIdAndVersion("1", "1")).thenReturn("1");
  }

  @Test
  public void testModulesByVersion() throws Exception {
    Set<String> moduleIds = new HashSet<String>();
    moduleIds.add("1");
    moduleIds.add("2");
    String sportPages = featuredDataController.modulesByVersion(moduleIds, "1");
    Assert.assertNotNull(sportPages);
  }

  @Test
  public void TestSportPages() {
    Mockito.when(featuredDataService.getSportPages()).thenReturn("1");
    String sportPages = featuredDataController.sportPages();
    Assert.assertNotNull(sportPages);
  }
}
