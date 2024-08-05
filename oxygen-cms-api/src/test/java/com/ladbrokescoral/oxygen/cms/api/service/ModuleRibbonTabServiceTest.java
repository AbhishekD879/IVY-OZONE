package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.ModuleRibbonTabArchiveRepository;
import com.ladbrokescoral.oxygen.cms.api.controller.private_api.ModuleRibbonTabsTest;
import com.ladbrokescoral.oxygen.cms.api.entity.ModuleRibbonTab;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.repository.ModuleRibbonTabRepository;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Arrays;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;
import org.springframework.context.annotation.Import;
import org.springframework.data.domain.Sort;

@RunWith(MockitoJUnitRunner.class)
@Import(ModelMapperConfig.class)
public class ModuleRibbonTabServiceTest {
  @Mock ModuleRibbonTabRepository repository;
  @Spy private ModelMapper modelMapper;
  ModuleRibbonTabService moduleRibbonTabService;

  ModuleRibbonTabArchiveRepository moduleRibbonTabArchiveRepository;
  @Mock SegmentService segmentService;

  @Before
  public void setUp() throws Exception {
    moduleRibbonTabService =
        new ModuleRibbonTabService(
            repository, moduleRibbonTabArchiveRepository, modelMapper, segmentService);
  }

  @Test
  public void testFindAllUniversalModuleRibbonTabs() {
    when(repository.findAllByUniversalSegment())
        .thenReturn(
            Arrays.asList(ModuleRibbonTabsTest.createModuleRibbonTab("2", false, "universal")));
    List<ModuleRibbonTab> moduleRibbonTabs =
        moduleRibbonTabService.findAllUniversalModuleRibbonTabs();
    Assert.assertNotNull(moduleRibbonTabs);
    Assert.assertSame(1, moduleRibbonTabs.size());
  }

  @Test
  public void testFindAllSegmentedByBrandAndVisible() {
    when(repository.findAllUniversalByBrandAndVisibleOrderBySortOrderAsc(
            "bma", true, Sort.by(Sort.Direction.ASC, "sortOrder")))
        .thenReturn(
            Arrays.asList(
                ModuleRibbonTabsTest.createModuleRibbonTab(
                    "2", false, SegmentConstants.UNIVERSAL)));
    List<ModuleRibbonTab> moduleRibbonTabs =
        moduleRibbonTabService.findAllSegmentedByBrandAndVisible("bma", SegmentConstants.UNIVERSAL);
    Assert.assertNotNull(moduleRibbonTabs);
    Assert.assertSame(1, moduleRibbonTabs.size());
  }

  @Test
  public void testFindAllSegmentedByBrandAndVisibleForSegment() {
    when(repository.findAllByBrandAndSegmentName("bma", true, Arrays.asList("segment1")))
        .thenReturn(
            Arrays.asList(ModuleRibbonTabsTest.createModuleRibbonTab("2", false, "segment1")));
    List<ModuleRibbonTab> moduleRibbonTabs =
        moduleRibbonTabService.findAllSegmentedByBrandAndVisible("bma", "segment1");

    Assert.assertNotNull(moduleRibbonTabs);
    Assert.assertSame(1, moduleRibbonTabs.size());
  }
}
