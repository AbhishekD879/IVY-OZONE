package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static com.ladbrokescoral.oxygen.cms.api.service.public_api.ModuleRibbonTabPublicService.BUILD_YOUR_BET_TAB;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.FooterMenusTest;
import com.ladbrokescoral.oxygen.cms.api.dto.BaseModularContentDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ModularContentDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ModularIdsContentDto;
import com.ladbrokescoral.oxygen.cms.api.dto.ModularSegmentedContentDto;
import com.ladbrokescoral.oxygen.cms.api.entity.DataSelection;
import com.ladbrokescoral.oxygen.cms.api.entity.DeviceType;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModuleData;
import com.ladbrokescoral.oxygen.cms.api.entity.ModuleRibbonTab;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.Visibility;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.service.BybTabAvailabilityService;
import com.ladbrokescoral.oxygen.cms.api.service.ModuleRibbonTabService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentedModuleSerive;
import com.ladbrokescoral.oxygen.cms.api.service.impl.HomeModuleServiceImpl;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.stream.Collectors;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.util.CollectionUtils;

@RunWith(MockitoJUnitRunner.class)
public class ModularContentPublicServiceTest {

  @Mock private HomeModuleServiceImpl homeModuleService;

  @Mock private ModuleRibbonTabService moduleRibbonTabService;

  @Mock private BybTabAvailabilityService bybTabAvailabilityService;

  private ModularContentPublicService modularContentPublicService;

  @Mock private BuildYourBetPublicService buildYourBetPublicService;
  @Mock private SegmentRepository segmentRepository;
  @Mock private SegmentedModuleSerive segmentedModuleSerive;

  @Mock private SegmentService segmentService;

  @Before
  public void init() {
    List<ModuleRibbonTab> ribbonModules = createModules();
    when(moduleRibbonTabService.findAllByBrandAndVisible("bma")).thenReturn(ribbonModules);
    modularContentPublicService =
        new ModularContentPublicService(
            homeModuleService,
            moduleRibbonTabService,
            bybTabAvailabilityService,
            buildYourBetPublicService,
            segmentRepository,
            segmentedModuleSerive,
            segmentService);
  }

  public List<ModuleRibbonTab> createModules() {
    ModuleRibbonTab featuredTab = new ModuleRibbonTab();
    featuredTab.setDirectiveName("Featured");
    featuredTab.setBrand("bma");

    ModuleRibbonTab inPlayTab = new ModuleRibbonTab();
    inPlayTab.setDirectiveName("InPlay");
    inPlayTab.setBrand("bma");

    ModuleRibbonTab eventHubTab = new ModuleRibbonTab();
    eventHubTab.setDirectiveName("EventHub");
    eventHubTab.setBrand("bma");
    eventHubTab.setHubIndex(1);

    return Arrays.asList(featuredTab, inPlayTab, eventHubTab);
  }

  @Test
  public void testMapModuleContent() {
    List<HomeModule> homeModules =
        Arrays.asList(
            createModules("1", PageType.eventhub, "1", "Football 1"),
            createModules("2", PageType.sport, "2", "Slime Racing"),
            createModules("0", PageType.sport, "3", "Dull Tennis"),
            createModules("1", PageType.eventhub, "4", "Football 2"));
    when(homeModuleService.findByActiveStateAndPublishToChannel(true, "bma"))
        .thenReturn(homeModules);
    when(segmentRepository.findByBrand("bma"))
        .thenReturn(
            Arrays.asList(Segment.builder().segmentName(SegmentConstants.UNIVERSAL).build()));
    List<BaseModularContentDto> list = modularContentPublicService.findByBrand("bma");

    assertEquals(6, list.size());
    assertFalse(CollectionUtils.isEmpty(((ModularContentDto) list.get(0)).getModuleDtos()));

    ModularIdsContentDto modularIds = (ModularIdsContentDto) list.get(3);
    assertFalse(CollectionUtils.isEmpty(modularIds.getMarketIds()));
    assertTrue(Arrays.asList(1, 2, 3, 4).containsAll(modularIds.getMarketIds()));
  }

  @Test
  public void testMapModuleContentWithoutFeaturedModules() {
    List<HomeModule> homeModules =
        Arrays.asList(
            createModules("1", PageType.eventhub, "1", "Football 1"),
            createModules("2", PageType.sport, "2", "Slime Racing"),
            createModules("0", PageType.sport, "3", "Dull Tennis"),
            createModules("1", PageType.eventhub, "4", "Football 2"));
    when(homeModuleService.findByActiveStateAndPublishToChannel(true, "bma"))
        .thenReturn(homeModules);

    List<BaseModularContentDto> list =
        modularContentPublicService.findInitialDataModularContent("bma", false);

    assertEquals(6, list.size());
    assertTrue(CollectionUtils.isEmpty(((ModularContentDto) list.get(0)).getModuleDtos()));

    ModularIdsContentDto modularIds = (ModularIdsContentDto) list.get(3);
    assertFalse(CollectionUtils.isEmpty(modularIds.getMarketIds()));
    assertTrue(Arrays.asList(1, 2, 3, 4).containsAll(modularIds.getMarketIds()));
  }

  @Test
  public void testPrepareInitialDataModularContent() {
    List<HomeModule> homeModules =
        Arrays.asList(
            createModules("1", PageType.eventhub, "1", "Football 1"),
            createModules("2", PageType.sport, "2", "Slime Racing"),
            createModules("0", PageType.sport, "3", "Dull Tennis"),
            createModules("1", PageType.eventhub, "4", "Football 2"));
    when(homeModuleService.findByActiveStateAndPublishToChannel(true, "bma"))
        .thenReturn(homeModules);

    List<BaseModularContentDto> list =
        modularContentPublicService.prepareInitialDataModularContent("bma");

    assertEquals(6, list.size());
    assertTrue(CollectionUtils.isEmpty(((ModularContentDto) list.get(0)).getModuleDtos()));

    ModularIdsContentDto modularIds = (ModularIdsContentDto) list.get(3);
    assertFalse(CollectionUtils.isEmpty(modularIds.getMarketIds()));
    assertTrue(Arrays.asList(1, 2, 3, 4).containsAll(modularIds.getMarketIds()));
  }

  @Test
  public void testPrepareInitialDataModularContentForPersonalisedHomeModule() {
    List<HomeModule> homeModules =
        Arrays.asList(
            createModules("1", PageType.eventhub, "1", "Football 1"),
            createModules("2", PageType.sport, "2", "Slime Racing"),
            createModules("0", PageType.sport, "3", "Dull Tennis"),
            getPersonalisedHomeModule("1", PageType.eventhub, "4", "Football 2"));
    when(homeModuleService.findByActiveStateAndPublishToChannel(true, "bma"))
        .thenReturn(homeModules);
    when(bybTabAvailabilityService.isBuildYourBetConfigurationEnabled("bma", false))
        .thenReturn(true);
    when(buildYourBetPublicService.isAtLeastOneBanachEventAvailable("bma")).thenReturn(true);

    List<BaseModularContentDto> list =
        modularContentPublicService.prepareInitialDataModularContent("bma");

    assertEquals(6, list.size());
    assertTrue(CollectionUtils.isEmpty(((ModularContentDto) list.get(0)).getModuleDtos()));

    ModularIdsContentDto modularIds = (ModularIdsContentDto) list.get(3);
    assertFalse(CollectionUtils.isEmpty(modularIds.getMarketIds()));
    assertTrue(Arrays.asList(1, 2, 3, 4).containsAll(modularIds.getMarketIds()));
  }

  @Test
  public void testPrepareSegmentedInitialDataModularContent() {
    when(bybTabAvailabilityService.isBuildYourBetConfigurationEnabled("bma", false))
        .thenReturn(true);
    when(buildYourBetPublicService.isAtLeastOneBanachEventAvailable("bma")).thenReturn(true);

    List<BaseModularContentDto> list =
        modularContentPublicService.prepareSegmentedInitialDataModularContent(
            "bma", "universal", DeviceType.MOBILE);

    assertEquals(1, list.size());
  }

  @Test
  public void testPrepareSegmentedInitialDataModularContentForUniversal() {
    HomeModule module = createModules("0", PageType.sport, "3", "Dull Tennis");
    module.setUniversalSegment(true);

    HomeModule module1 = createModules("2", PageType.sport, "2", "Slime Racing");
    module1.setUniversalSegment(false);
    module1.setSegmentReferences(FooterMenusTest.getSegmentReference("segment1"));

    module.setExclusionList(Arrays.asList("segment1"));
    List<HomeModule> homeModules =
        Arrays.asList(
            createModules("1", PageType.eventhub, "1", "Football 1"),
            module1,
            module,
            getPersonalisedHomeModule("1", PageType.eventhub, "4", "Football 2"));
    when(homeModuleService.findByActiveStateAndPublishToChannelBySegmantName(
            true, "bma", SegmentConstants.UNIVERSAL))
        .thenReturn(homeModules);
    when(bybTabAvailabilityService.isBuildYourBetConfigurationEnabled("bma", false))
        .thenReturn(true);
    when(buildYourBetPublicService.isAtLeastOneBanachEventAvailable("bma")).thenReturn(false);
    when(segmentRepository.findByBrand("bma"))
        .thenReturn(
            Arrays.asList(
                Segment.builder().segmentName("segment1").build(),
                Segment.builder().segmentName("segment2").build()));

    when(moduleRibbonTabService.findAllSegmentedByBrandAndVisible(
            "bma", SegmentConstants.UNIVERSAL))
        .thenReturn(createModules());

    List<BaseModularContentDto> list =
        modularContentPublicService.prepareSegmentedInitialDataModularContent(
            "bma", SegmentConstants.UNIVERSAL, DeviceType.MOBILE);

    assertEquals(6, list.size());
  }

  @Test
  public void testPrepareSegmentedInitialDataModularContentForNonUniversal() {
    List<HomeModule> homeModules =
        Arrays.asList(
            createModules("1", PageType.eventhub, "1", "Football 1"),
            createModules("2", PageType.sport, "2", "Slime Racing"),
            createModules("0", PageType.sport, "3", "Dull Tennis"),
            getPersonalisedHomeModule("1", PageType.eventhub, "4", "Football 2"));
    when(homeModuleService.findByActiveStateAndPublishToChannelBySegmantName(
            true, "bma", "segment1"))
        .thenReturn(homeModules);
    when(bybTabAvailabilityService.isBuildYourBetConfigurationEnabled("bma", false))
        .thenReturn(true);
    when(segmentedModuleSerive.isSegmentedModule(
            ModuleRibbonTab.class.getSimpleName(), DeviceType.MOBILE, "bma"))
        .thenReturn(true);

    when(buildYourBetPublicService.isAtLeastOneBanachEventAvailable("bma")).thenReturn(false);

    List<ModuleRibbonTab> moduleRibbonTabs = new ArrayList<>(createModules());
    moduleRibbonTabs.get(0).setInternalId(BUILD_YOUR_BET_TAB);
    when(moduleRibbonTabService.findAllSegmentedByBrandAndVisible("bma", "segment1"))
        .thenReturn(moduleRibbonTabs);

    List<BaseModularContentDto> list =
        modularContentPublicService.prepareSegmentedInitialDataModularContent(
            "bma", "segment1", DeviceType.MOBILE);

    assertEquals(5, list.size());
  }

  @Test
  public void testFindUniversalByBrand() {

    List<BaseModularContentDto> list = modularContentPublicService.findUniversalByBrand("bma");

    assertEquals(1, list.size());
  }

  @Test
  public void testPreparesModularContentCollection() {
    List<HomeModule> homeModules =
        Arrays.asList(
            createModules("1", PageType.eventhub, "1", "Football 1"),
            createModules("2", PageType.sport, "2", "Slime Racing"),
            createModules("0", PageType.sport, "3", "Dull Tennis"),
            getPersonalisedHomeModule("1", PageType.eventhub, "4", "Football 2"));
    when(homeModuleService.findByActiveStateAndPublishToChannel(true, "bma"))
        .thenReturn(homeModules);
    when(bybTabAvailabilityService.isBuildYourBetConfigurationEnabled("bma", false))
        .thenReturn(true);
    when(segmentService.getSegmentsForSegmentedViews("bma")).thenReturn(Arrays.asList("segment1"));

    when(buildYourBetPublicService.isAtLeastOneBanachEventAvailable("bma")).thenReturn(false);

    List<ModuleRibbonTab> moduleRibbonTabs = new ArrayList<>(createModules());
    moduleRibbonTabs.get(0).setInternalId(BUILD_YOUR_BET_TAB);

    ModularSegmentedContentDto modularSegmentedContentDto =
        modularContentPublicService.preparesModularContentCollection("bma");

    assertEquals(3, modularSegmentedContentDto.getModuleRibbonTabCollection().size());
    assertEquals(4, modularSegmentedContentDto.getHomeModuleCollection().size());
  }

  @Test
  public void testInPlayModuleAvailable() {
    when(homeModuleService.findByActiveStateAndPublishToChannel(true, "bma"))
        .thenReturn(new ArrayList<>());

    List<BaseModularContentDto> list = modularContentPublicService.findByBrand("bma");

    assertEquals(4, list.size());
    List<String> directiveNames =
        list.stream()
            .limit(2)
            .map(ModularContentDto.class::cast)
            .map(ModularContentDto::getDirectiveName)
            .collect(Collectors.toList());
    assertTrue(Arrays.asList("Featured", "InPlay", "EventHub").containsAll(directiveNames));
  }

  @Test
  public void testEventHubModuleAvailable() {
    List<HomeModule> homeModules =
        Arrays.asList(
            createModules("1", PageType.eventhub, "1", "Football 1"),
            createModules("2", PageType.sport, "2", "Slime Racing"),
            createModules("0", PageType.sport, "3", "Dull Tennis"),
            createModules("1", PageType.eventhub, "4", "Football 2"));
    createModules("1", PageType.sport, "3", "Dull Tennis");

    when(homeModuleService.findByActiveStateAndPublishToChannel(true, "bma"))
        .thenReturn(homeModules);

    List<BaseModularContentDto> list = modularContentPublicService.findByBrand("bma");
    assertEquals(6, list.size());

    ModularContentDto eventHubModularContent = (ModularContentDto) list.get(2);
    assertEquals("EventHub", eventHubModularContent.getDirectiveName());
    assertEquals(2, eventHubModularContent.getModuleDtos().size());
  }

  @Test
  public void testMapModuleContentPersonalised() {
    List<HomeModule> homeModules =
        Arrays.asList(
            getPersonalisedHomeModule("1", PageType.eventhub, "1", "Football 1"),
            getPersonalisedHomeModule("2", PageType.sport, "2", "Slime Racing"),
            getPersonalisedHomeModule("0", PageType.sport, "3", "Dull Tennis"),
            getPersonalisedHomeModule("1", PageType.eventhub, "4", "Football 2"));
    when(homeModuleService.findByActiveStateAndPublishToChannelAndApplyUniversalSegments(
            true, "bma"))
        .thenReturn(homeModules);

    List<HomeModule> list = modularContentPublicService.findPersonalised("bma");

    assertEquals(4, list.size());
    assertFalse(CollectionUtils.isEmpty(list.get(0).getData()));
  }

  public HomeModule getPersonalisedHomeModule(
      String pageId, PageType pageType, String selectionId, String title) {
    HomeModule homeModule = createModules(pageId, pageType, selectionId, title);
    homeModule.setPersonalised(true);
    return homeModule;
  }

  public HomeModule createModules(
      String pageId, PageType pageType, String selectionId, String title) {
    HomeModule homeModule = new HomeModule();
    homeModule.setTitle(title);
    homeModule.setPageId(pageId);
    homeModule.setPageType(pageType);
    homeModule.setNavItem("Featured");
    HomeModuleData homeModuleData = new HomeModuleData();
    DataSelection dataSelection = new DataSelection();
    dataSelection.setSelectionId(selectionId);
    dataSelection.setSelectionType("Market");
    homeModule.setDataSelection(dataSelection);
    homeModule.setData(Arrays.asList(homeModuleData));
    Visibility visibility = new Visibility();
    visibility.setEnabled(true);
    homeModule.setVisibility(visibility);
    return homeModule;
  }
}
