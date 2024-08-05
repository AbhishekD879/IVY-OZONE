package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertFalse;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.*;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.repository.*;
import com.ladbrokescoral.oxygen.cms.api.service.impl.HomeModuleServiceImpl;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;
import org.springframework.boot.test.mock.mockito.MockBean;

@RunWith(MockitoJUnitRunner.class)
public class SegmentPurgeServiceTest {

  @InjectMocks private SegmentPurgeService segmentPurgeService;

  @InjectMocks private SurfaceBetService surfaceBetService;
  @InjectMocks private HighlightCarouselService highlightCarouselService;
  @InjectMocks private HomeModuleServiceImpl homeModuleService;
  @InjectMocks private FooterMenuService footerMenuService;
  @InjectMocks private NavigationPointService navigationPointService;
  @InjectMocks private SportQuickLinkService sportQuickLinkService;
  @InjectMocks private ModuleRibbonTabService moduleRibbonTabService;
  @InjectMocks private SportCategoryService SportCategoryService;
  @InjectMocks private HomeInplaySportService homeInplaySportService;

  @InjectMocks private SurfaceBetTitleService surfaceBetTitleService;

  @Mock private SurfaceBetArchivalRepository surfaceBetArchivalRepository;
  @Mock private HighlightCarouselArchiveRepository highlightCarouselArchiveRepository;
  @Mock private HomeModuleArchivalRepository homeModuleArchivalRepository;
  @Mock private FooterMenuArchivalRepository footerMenuArchivalRepository;
  @Mock private NavigationPointArchivalRepository navigationPointArchivalRepository;
  @Mock private SportQuickLinkArchivalRepository sportQuickLinkArchivalRepository;
  @Mock private ModuleRibbonTabArchiveRepository moduleRibbonTabArchiveRepository;
  @Mock private SportCategoryArchivalRepository sportCategoryArchivalRepository;
  @Mock private SportModuleArchivalRepository sportModuleArchivalRepository;

  @Mock private SurfaceBetRepository surfaceBetRepository;
  @Mock private HighlightCarouselRepository highlightCarouselRepository;
  @Mock private HomeModuleRepository homeModuleRepository;
  @Mock private FooterMenuRepository footerMenuRepository;
  @Mock private NavigationPointRepository navigationPointRepository;
  @Mock private SportQuickLinkRepository sportQuickLinkRepository;
  @Mock private ModuleRibbonTabRepository moduleRibbonTabRepository;
  @Mock private SportCategoryRepository sportCategoryRepository;
  @Mock private HomeInplaySportRepository homeInplaySportRepository;

  @MockBean private SegmentService segmentService;
  @Mock private ModelMapper modelMapper;

  @MockBean SvgImageParser svgImageParser;
  @MockBean ImageService imageService;
  @MockBean SvgEntityService<SurfaceBet> svgEntityService;
  @MockBean SiteServeApiProvider siteServeApiProvider;
  @MockBean CompetitionModuleService competitionModuleService;
  @Mock private SportPagesOrderingService sportPagesOrderingService;

  @Before
  public void setUp() {

    surfaceBetService =
        new SurfaceBetService(
            surfaceBetRepository,
            svgEntityService,
            "/foo/test",
            siteServeApiProvider,
            surfaceBetArchivalRepository,
            segmentService,
            modelMapper,
            competitionModuleService,
            sportPagesOrderingService,
            surfaceBetTitleService);
    segmentPurgeService =
        new SegmentPurgeService(
            surfaceBetService,
            highlightCarouselService,
            homeModuleService,
            footerMenuService,
            navigationPointService,
            sportQuickLinkService,
            moduleRibbonTabService,
            SportCategoryService,
            homeInplaySportService);
  }

  @Test
  public void testdeleteSegmentsInModules() {
    List<String> segments = Arrays.asList("s1,s2,s3".split(","));

    List<SurfaceBet> surfaceBets = getSurfaceBets();
    when(surfaceBetRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(surfaceBets);

    List<HighlightCarousel> highlightCarousels = gethighlightCarousels();
    when(highlightCarouselRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(highlightCarousels);

    List<HomeModule> homeModules = getHomeModules();
    when(homeModuleRepository.findAllBySegmentNameIninclusiveAndExclusiveAndPulishToChannels(
            "bma", segments))
        .thenReturn(homeModules);

    List<SportQuickLink> sportQuickLinks = getsportQuickLinks();
    when(sportQuickLinkRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(sportQuickLinks);

    List<ModuleRibbonTab> moduleRibbonTabs = getModuleRibbonTab();
    when(moduleRibbonTabRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(moduleRibbonTabs);

    List<NavigationPoint> navigationPoints = getNavigationPoints();
    when(navigationPointRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(navigationPoints);

    List<FooterMenu> footerMenus = getFooterMenus();
    when(footerMenuRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(footerMenus);

    segmentPurgeService.deleteSegmentsInModules(segments, "bma");

    assertFalse(
        surfaceBets.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        highlightCarousels.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        homeModules.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        sportQuickLinks.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        moduleRibbonTabs.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        navigationPoints.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        footerMenus.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
  }

  @Test
  public void testdeleteSegmentsInModulesNullmodules() {
    List<String> segments = Arrays.asList("s1,s2,s3".split(","));

    List<SurfaceBet> surfaceBets = getSurfaceBets();
    when(surfaceBetRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(new ArrayList<>());

    List<HighlightCarousel> highlightCarousels = gethighlightCarousels();
    when(highlightCarouselRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(null);

    List<HomeModule> homeModules = getHomeModules();
    when(homeModuleRepository.findAllBySegmentNameIninclusiveAndExclusiveAndPulishToChannels(
            "bma", segments))
        .thenReturn(new ArrayList<>());

    List<SportQuickLink> sportQuickLinks = getsportQuickLinks();
    when(sportQuickLinkRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(new ArrayList<>());

    List<ModuleRibbonTab> moduleRibbonTabs = getModuleRibbonTab();
    when(moduleRibbonTabRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(new ArrayList<>());

    List<NavigationPoint> navigationPoints = getNavigationPoints();
    when(navigationPointRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(new ArrayList<>());

    List<FooterMenu> footerMenus = getFooterMenus();
    when(footerMenuRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(null);

    segmentPurgeService.deleteSegmentsInModules(segments, "bma");

    assertFalse(
        surfaceBets.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        highlightCarousels.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        homeModules.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        sportQuickLinks.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        moduleRibbonTabs.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        navigationPoints.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        footerMenus.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
  }

  @Test
  public void testdeleteSegmentsInModulesNullwithInclusiveAndExclusiveNull() {
    List<String> segments = Arrays.asList("s1,s2,s3".split(","));

    List<SurfaceBet> surfaceBets = getSurfaceBets();
    surfaceBets.get(0).setInclusionList(null);
    surfaceBets.get(1).setExclusionList(null);
    when(surfaceBetRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(surfaceBets);

    List<HighlightCarousel> highlightCarousels = gethighlightCarousels();
    highlightCarousels.get(0).setInclusionList(null);
    highlightCarousels.get(1).setExclusionList(null);
    when(highlightCarouselRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(highlightCarousels);

    List<HomeModule> homeModules = getHomeModules();
    homeModules.get(0).setInclusionList(null);
    homeModules.get(1).setExclusionList(null);
    when(homeModuleRepository.findAllBySegmentNameIninclusiveAndExclusiveAndPulishToChannels(
            "bma", segments))
        .thenReturn(homeModules);

    List<SportQuickLink> sportQuickLinks = getsportQuickLinks();
    sportQuickLinks.get(0).setInclusionList(null);
    sportQuickLinks.get(1).setExclusionList(null);
    when(sportQuickLinkRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(sportQuickLinks);

    List<ModuleRibbonTab> moduleRibbonTabs = getModuleRibbonTab();
    moduleRibbonTabs.get(0).setInclusionList(null);
    moduleRibbonTabs.get(1).setExclusionList(null);
    when(moduleRibbonTabRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(moduleRibbonTabs);

    List<NavigationPoint> navigationPoints = getNavigationPoints();
    navigationPoints.get(0).setInclusionList(null);
    navigationPoints.get(1).setExclusionList(null);
    when(navigationPointRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(navigationPoints);

    List<FooterMenu> footerMenus = getFooterMenus();
    footerMenus.get(0).setInclusionList(null);
    footerMenus.get(1).setExclusionList(null);
    when(footerMenuRepository.findAllBySegmentNameIninclusiveAndExclusive("bma", segments))
        .thenReturn(footerMenus);

    segmentPurgeService.deleteSegmentsInModules(segments, "bma");

    assertFalse(
        surfaceBets.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        highlightCarousels.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        homeModules.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        sportQuickLinks.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        moduleRibbonTabs.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        navigationPoints.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
    assertFalse(
        footerMenus.stream()
            .anyMatch(
                surfaceBet ->
                    segments.stream()
                        .anyMatch(
                            seg ->
                                surfaceBet.getInclusionList().contains(seg)
                                    && surfaceBet.getExclusionList().contains(seg))));
  }

  private List<NavigationPoint> getNavigationPoints() {
    List<NavigationPoint> navigationPoints = new ArrayList<>();
    navigationPoints.add(
        createNavigationPoint("TITLE", castToList("s1,s4,s6"), castToList("s2,s3,s7,s8"), false));
    navigationPoints.add(
        createNavigationPoint("TITLE1", castToList("s1,s2,s3"), castToList("s4,s6"), true));
    return navigationPoints;
  }

  private NavigationPoint createNavigationPoint(
      String Title, List<String> inclusionList, List<String> exclusionList, boolean isunivesal) {
    NavigationPoint result = new NavigationPoint();
    result.setBrand("bma");
    if (!isunivesal) {
      result.setInclusionList(inclusionList);
    } else {
      result.setExclusionList(exclusionList);
    }
    result.setUniversalSegment(isunivesal);
    return result;
  }

  private List<FooterMenu> getFooterMenus() {
    List<FooterMenu> footerMenus = new ArrayList<>();
    footerMenus.add(
        createFooterMenus("TITLE", castToList("s1,s4,s6"), castToList("s2,s3,s7,s8"), false));
    footerMenus.add(createFooterMenus("TITLE1", castToList("s1,s2,s3"), castToList("s4,s6"), true));
    return footerMenus;
  }

  private FooterMenu createFooterMenus(
      String Title, List<String> inclusionList, List<String> exclusionList, boolean isunivesal) {
    FooterMenu result = new FooterMenu();
    result.setBrand("bma");
    if (!isunivesal) {
      result.setInclusionList(inclusionList);
    } else {
      result.setExclusionList(exclusionList);
    }
    result.setUniversalSegment(isunivesal);

    return result;
  }

  private List<ModuleRibbonTab> getModuleRibbonTab() {
    List<ModuleRibbonTab> moduleRibbonTabs = new ArrayList<>();
    moduleRibbonTabs.add(
        createModuleRibbonTab("TITLE", castToList("s1,s4,s6"), castToList("s2,s3,s7,s8"), false));
    moduleRibbonTabs.add(
        createModuleRibbonTab("TITLE1", castToList("s1,s2,s3"), castToList("s4,s6"), true));
    return moduleRibbonTabs;
  }

  private ModuleRibbonTab createModuleRibbonTab(
      String Title, List<String> inclusionList, List<String> exclusionList, boolean isunivesal) {
    ModuleRibbonTab result = new ModuleRibbonTab();
    result.setBrand("bma");
    result.setTitle(Title);
    if (!isunivesal) {
      result.setInclusionList(inclusionList);
    } else {
      result.setExclusionList(exclusionList);
    }
    result.setUniversalSegment(isunivesal);

    return result;
  }

  private List<SportQuickLink> getsportQuickLinks() {
    List<SportQuickLink> sportQuickLinks = new ArrayList<>();
    sportQuickLinks.add(
        craetesportQuickLink("TITLE", castToList("s1,s4,s6"), castToList("s2,s3,s7,s8"), false));
    sportQuickLinks.add(
        craetesportQuickLink("TITLE1", castToList("s1,s2,s3"), castToList("s4,s6"), true));
    return sportQuickLinks;
  }

  private SportQuickLink craetesportQuickLink(
      String Title, List<String> inclusionList, List<String> exclusionList, boolean isunivesal) {
    SportQuickLink result = new SportQuickLink();
    result.setBrand("bma");
    result.setTitle(Title);
    if (!isunivesal) {
      result.setInclusionList(inclusionList);
    } else {
      result.setExclusionList(exclusionList);
    }
    result.setUniversalSegment(isunivesal);
    return result;
  }

  private List<HomeModule> getHomeModules() {
    List<HomeModule> HomeModules = new ArrayList<>();
    HomeModules.add(
        createHomeModule("TITLE", castToList("s1,s4,s6"), castToList("s2,s3,s7,s8"), false));
    HomeModules.add(createHomeModule("TITLE1", castToList("s1,s2,s3"), castToList("s4,s6"), true));
    return HomeModules;
  }

  private HomeModule createHomeModule(
      String Title, List<String> inclusionList, List<String> exclusionList, boolean isunivesal) {
    HomeModule result = new HomeModule();
    result.setTitle(Title);
    if (!isunivesal) {
      result.setInclusionList(inclusionList);
    } else {
      result.setExclusionList(exclusionList);
    }
    result.setUniversalSegment(isunivesal);
    return result;
  }

  private List<HighlightCarousel> gethighlightCarousels() {
    List<HighlightCarousel> highlightCarousels = new ArrayList<>();
    highlightCarousels.add(
        createHighlightCarousel("TITLE", castToList("s1,s4,s6"), castToList("s2,s3,s7,s8"), false));
    highlightCarousels.add(
        createHighlightCarousel("TITLE1", castToList("s1,s2,s3"), castToList("s4,s6"), true));
    return highlightCarousels;
  }

  private HighlightCarousel createHighlightCarousel(
      String Title, List<String> inclusionList, List<String> exclusionList, boolean isunivesal) {
    HighlightCarousel result = new HighlightCarousel();
    result.setBrand("bma");
    result.setTitle(Title);
    if (!isunivesal) {
      result.setInclusionList(inclusionList);
    } else {
      result.setExclusionList(exclusionList);
    }
    result.setUniversalSegment(isunivesal);
    return result;
  }

  private List<SurfaceBet> getSurfaceBets() {

    List<SurfaceBet> surfaceBets = new ArrayList<>();
    surfaceBets.add(
        createSurfaceBet("TITLE", castToList("s1,s4,s6"), castToList("s2,s3,s7,s8"), false));
    surfaceBets.add(createSurfaceBet("TITLE1", castToList("s1,s2,s3"), castToList("s4,s6"), true));
    return surfaceBets;
  }

  private SurfaceBet createSurfaceBet(
      String Title, List<String> inclusionList, List<String> exclusionList, boolean isunivesal) {
    SurfaceBet result = new SurfaceBet();
    result.setBrand("bma");
    result.setTitle(Title);
    result.setContent("content");
    if (!isunivesal) {
      result.setInclusionList(inclusionList);
    } else {
      result.setExclusionList(exclusionList);
    }
    result.setUniversalSegment(isunivesal);
    return result;
  }

  public List<String> castToList(String segments) {

    return Arrays.asList(segments.split(","));
  }
}
