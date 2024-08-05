package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static com.ladbrokescoral.oxygen.cms.api.entity.AbstractSportEntity.SPORT_HOME_PAGE;
import static com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType.*;
import static com.ladbrokescoral.oxygen.cms.api.service.public_api.ModularContentPublicService.FEATURED_DIRECTIVE;
import static java.util.Arrays.asList;
import static java.util.Collections.singletonList;
import static org.assertj.core.api.AssertionsForClassTypes.assertThat;
import static org.assertj.core.api.AssertionsForInterfaceTypes.assertThat;

import com.ladbrokescoral.oxygen.cms.api.controller.private_api.SportModuleTest;
import com.ladbrokescoral.oxygen.cms.api.dto.*;
import com.ladbrokescoral.oxygen.cms.api.entity.*;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.Segment;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.SegmentConstants;
import com.ladbrokescoral.oxygen.cms.api.mapping.RacingModuleMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.RacingModuleType;
import com.ladbrokescoral.oxygen.cms.api.repository.SegmentRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FanzonesService;
import com.ladbrokescoral.oxygen.cms.api.service.SportModuleService;
import com.ladbrokescoral.oxygen.cms.api.service.StructureService;
import com.ladbrokescoral.oxygen.cms.api.service.VirtualNextEventsService;
import com.ladbrokescoral.oxygen.cms.util.Util;
import java.time.Instant;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.UUID;
import java.util.function.Function;
import java.util.stream.Collectors;
import java.util.stream.IntStream;
import org.apache.commons.lang.WordUtils;
import org.apache.commons.lang3.RandomStringUtils;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mapstruct.factory.Mappers;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(MockitoJUnitRunner.class)
public class SportPagePublicServiceTest extends BDDMockito {
  private static final boolean GROUPED = true;
  private static final boolean UNGROUPED = false;

  private static final String BRAND = "bma";
  private static final String FOOTBALL_PAGE_ID = "16";
  private static final String HOKEY_PAGE_ID = "54";
  private static final String BOXING_PAGE_ID = "9";
  private static final String FOOTBALL_CATEGORY_ID = "101";
  private static final String BASKETBALL_CATEGORY_ID = "102";
  private static final String HORSE_RACING_ID = "21";

  private static final String VIRTUALS_ID = "39";
  private static final String FANZONE_PAGE_ID = "160";
  private static final String FOOTBALL_PREMIER_LEAGUE = "Premier League";
  private static final String FOOTBALL_SERIE_A = "Serie A";
  private static final String FOOTBALL_PRIMERA_DIVISION = "Primera Division";
  private static final String BASKETBALL_NBA = "NBA";
  private static final String BASKETBALL_FIBA = "FIBA";
  private static final String SPORT_CUSTOMIZED_HOME_PAGE =
      new SportGroupKey(SPORT_HOME_PAGE, PageType.customized).getGroupKey();

  @Mock private ModularContentPublicService modularContentPublicService;
  @Mock private SportQuickLinkPublicService sportQuickLinkPublicService;
  @Mock private SportModuleService sportModuleService;
  @Mock private HighlightCarouselPublicService highlightCarouselPublicService;
  @Mock private SurfaceBetPublicService surfaceBetPublicService;
  @Mock private StructureService structureService;
  @Mock private SegmentRepository segmentRepository;
  @Mock private BybWidgetPublicService bybWidgetPublicService;
  @Mock private LuckyDipModuleService luckyDipModuleService;
  @Mock private PopularAccaWidgetPublicService popularAccaWidgetPublicService;

  @Mock private VirtualNextEventsService nextEventsService;

  @Mock private FanzonesService fanzonesService;

  @Spy
  private final RacingModuleMapper racingModuleMapper = Mappers.getMapper(RacingModuleMapper.class);

  @InjectMocks private SportPagePublicService sportPagePublicService;

  @Before
  public void setUp() {
    mockIsGroupedFeaturedEnabled(true);
  }

  @Test
  public void findAllPagesByBrandHappyPathWithLastUpdatedDate() {
    // given
    List<SportModule> featuredModules =
        asList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, FEATURED), 0),
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, FEATURED), 0),
            sportModuleOf(new SportPageId(FANZONE_PAGE_ID, PageType.sport, FEATURED), 1));
    List<SportModule> quickLinkModules =
        asList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, QUICK_LINK), 1),
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, QUICK_LINK), 1),
            sportModuleOf(new SportPageId(FANZONE_PAGE_ID, PageType.sport, QUICK_LINK), 1));
    List<SportModule> rpgModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, RECENTLY_PLAYED_GAMES), -10));
    List<SportModule> virtualHorseRacingModules =
        Arrays.asList(
            createVirtualHorseRacingModule(RacingModuleType.UK_AND_IRISH_RACES, 99.0),
            createVirtualHorseRacingModule(RacingModuleType.INTERNATIONAL_RACES, 100.0),
            createVirtualHorseRacingModule(RacingModuleType.CORAL_LEGENDS, 97.0));

    List<SportModule> virtualNextEventsModules = singletonList(createVirtualNextEventsModule(10.0));

    when(segmentRepository.findByBrand(BRAND))
        .thenReturn(
            Arrays.asList(
                Segment.builder().segmentName(SegmentConstants.UNIVERSAL).build(),
                Segment.builder().segmentName("segment1").build()));
    List<SportModule> inPlayModules = SportModuleTest.createINplayModules();
    when(sportModuleService.findAll(BRAND, SportModuleType.INPLAY)).thenReturn(inPlayModules);
    List<SportModule> unfeaturedModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, UNGROUPED_FEATURED), 42));

    List<SportModule> bybModules =
        Arrays.asList(
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, BYB_WIDGET), 42),
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, BYB_WIDGET), 42));

    List<SportModule> aemBannerModule = Arrays.asList(createAemBannerModule());

    when(sportModuleService.findByBrand(BRAND))
        .thenReturn(
            Util.mergeLists(
                featuredModules,
                quickLinkModules,
                rpgModules,
                virtualHorseRacingModules,
                unfeaturedModules,
                virtualNextEventsModules,
                bybModules,
                aemBannerModule));

    ReflectionTestUtils.setField(sportPagePublicService, "produceAemBanners", true);
    when(sportModuleService.findAllActive(BRAND, AEM_BANNERS)).thenReturn(aemBannerModule);
    when(sportModuleService.findAllActive(BRAND, RECENTLY_PLAYED_GAMES)).thenReturn(rpgModules);
    when(sportModuleService.findAll(BRAND, SportModuleType.RACING_MODULE))
        .thenReturn(virtualHorseRacingModules);

    List<BaseModularContentDto> homeFeaturedData = createHomeFeaturedData(3);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    List<SportQuickLinkDto> homeQuickLinks =
        asList(
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE));
    List<SportQuickLinkDto> footballQuickLinks =
        asList(createQuickLink(FOOTBALL_PAGE_ID), createQuickLink(FOOTBALL_PAGE_ID));
    List<SportQuickLinkDto> fanzoneQuickLinks =
        asList(createQuickLink(FANZONE_PAGE_ID), createQuickLink(FANZONE_PAGE_ID));
    List<SportQuickLinkDto> hokeyQuickLinks = singletonList(createQuickLink(HOKEY_PAGE_ID));
    List<SportQuickLinkDto> boxingQuickLinks =
        asList(createQuickLink(BOXING_PAGE_ID), createQuickLink(BOXING_PAGE_ID));
    when(sportQuickLinkPublicService.findAll(BRAND))
        .thenReturn(
            Util.mergeLists(
                homeQuickLinks,
                footballQuickLinks,
                hokeyQuickLinks,
                boxingQuickLinks,
                fanzoneQuickLinks));

    List<HighlightCarouselDto> highlightCarouselDtos =
        Arrays.asList(
            createHighlightCarousel(SPORT_HOME_PAGE),
            createHighlightCarousel(SPORT_HOME_PAGE),
            createHighlightCarousel(FANZONE_PAGE_ID));
    when(highlightCarouselPublicService.findActiveByBrand(BRAND)).thenReturn(highlightCarouselDtos);

    List<VirtualNextEventDto> virtualNextEventDtos =
        Arrays.asList(
            createVirtualNextEventDto("football", "223"),
            createVirtualNextEventDto("horseracing", "445"));
    when(nextEventsService.readByBrandAndActive(BRAND)).thenReturn(virtualNextEventDtos);
    mockIsGroupedFeaturedEnabled(false);

    // when
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, System.currentTimeMillis()).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));

    List<RecentlyPlayedGameDto> rpgData = singletonList(new RecentlyPlayedGameDto().setSportId(0));

    assertThat(resultPages).hasSize(7);

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .hasSize(3)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(RECENTLY_PLAYED_GAMES, FEATURED, QUICK_LINK);
    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(Util.mergeLists(rpgData, homeFeaturedData, homeQuickLinks));

    assertThat(resultPages.get(FOOTBALL_PAGE_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(FOOTBALL_PAGE_ID).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(footballQuickLinks);

    assertThat(resultPages.get(HOKEY_PAGE_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(HOKEY_PAGE_ID).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(hokeyQuickLinks);

    assertThat(resultPages.get(BOXING_PAGE_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(SportModuleType.QUICK_LINK);
    assertThat(resultPages.get(BOXING_PAGE_ID).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(boxingQuickLinks);

    assertThat(resultPages.get(HORSE_RACING_ID).getSportPageModules())
        .hasSize(3)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(
            SportModuleType.RACING_MODULE,
            SportModuleType.RACING_MODULE,
            SportModuleType.RACING_MODULE);
    assertThat(resultPages.get(VIRTUALS_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(VIRTUAL_NEXT_EVENTS);

    assertThat(resultPages.get(HORSE_RACING_ID).getSportPageModules())
        .extracting(
            sportPageModule ->
                ((RacingModuleDto) sportPageModule.getPageData().get(0))
                    .getRacingConfig()
                    .getAbbreviation())
        .containsExactly("LVR", "UIR", "IR");
  }

  @Test
  public void findAllPagesByBrandHappyPath() {
    // given
    List<SportModule> featuredModules =
        asList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, FEATURED), 0),
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, FEATURED), 0));
    List<SportModule> quickLinkModules =
        asList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, QUICK_LINK), 1),
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, QUICK_LINK), 1));
    List<SportModule> rpgModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, RECENTLY_PLAYED_GAMES), -10));
    List<SportModule> virtualHorseRacingModules =
        Arrays.asList(
            createVirtualHorseRacingModule(RacingModuleType.UK_AND_IRISH_RACES, 99.0),
            createVirtualHorseRacingModule(RacingModuleType.INTERNATIONAL_RACES, 100.0),
            createVirtualHorseRacingModule(RacingModuleType.CORAL_LEGENDS, 97.0));
    List<SportModule> unfeaturedModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, UNGROUPED_FEATURED), 42));

    List<SportModule> virtualNextEventsModules =
        Collections.singletonList(createVirtualNextEventsModule(11.0));

    List<SportModule> fzYourTeamModules =
        singletonList(
            sportModuleOf(
                new SportPageId(FANZONE_PAGE_ID, PageType.sport, BETS_BASED_ON_YOUR_TEAM), 0));
    List<SportModule> fzOtherTeamModules =
        singletonList(
            sportModuleOf(
                new SportPageId(FANZONE_PAGE_ID, PageType.sport, BETS_BASED_ON_OTHER_FANS), 1));
    when(segmentRepository.findByBrand(BRAND))
        .thenReturn(Arrays.asList(Segment.builder().segmentName("uni").build()));
    List<SportModule> inPlayModules = SportModuleTest.createINplayModules();
    when(sportModuleService.findAll(BRAND, SportModuleType.INPLAY)).thenReturn(inPlayModules);
    when(sportModuleService.findAll(BRAND, BETS_BASED_ON_YOUR_TEAM)).thenReturn(fzYourTeamModules);
    when(sportModuleService.findAll(BRAND, BETS_BASED_ON_OTHER_FANS))
        .thenReturn(fzOtherTeamModules);
    when(fanzonesService.findAllFanzonesByBrand(BRAND))
        .thenReturn(Optional.of(Arrays.asList(getFanzone())));
    when(sportModuleService.findByBrand(BRAND))
        .thenReturn(
            Util.mergeLists(
                featuredModules,
                quickLinkModules,
                rpgModules,
                virtualHorseRacingModules,
                unfeaturedModules,
                virtualNextEventsModules));
    ReflectionTestUtils.setField(sportPagePublicService, "produceAemBanners", false);
    when(sportModuleService.findAllActive(BRAND, RECENTLY_PLAYED_GAMES)).thenReturn(rpgModules);
    when(sportModuleService.findAll(BRAND, SportModuleType.RACING_MODULE))
        .thenReturn(virtualHorseRacingModules);

    List<BaseModularContentDto> homeFeaturedData = createHomeFeaturedData(3);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    List<SportQuickLinkDto> homeQuickLinks =
        asList(
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE));
    List<SportQuickLinkDto> footballQuickLinks =
        asList(createQuickLink(FOOTBALL_PAGE_ID), createQuickLink(FOOTBALL_PAGE_ID));
    List<SportQuickLinkDto> hokeyQuickLinks = singletonList(createQuickLink(HOKEY_PAGE_ID));
    List<SportQuickLinkDto> boxingQuickLinks =
        asList(createQuickLink(BOXING_PAGE_ID), createQuickLink(BOXING_PAGE_ID));
    when(sportQuickLinkPublicService.findAll(BRAND))
        .thenReturn(
            Util.mergeLists(homeQuickLinks, footballQuickLinks, hokeyQuickLinks, boxingQuickLinks));

    List<HighlightCarouselDto> highlightCarouselDtos =
        Arrays.asList(
            createHighlightCarousel(SPORT_HOME_PAGE), createHighlightCarousel(SPORT_HOME_PAGE));
    when(highlightCarouselPublicService.findActiveByBrand(BRAND)).thenReturn(highlightCarouselDtos);

    List<VirtualNextEventDto> virtualNextEventDtos =
        Arrays.asList(
            createVirtualNextEventDto("football", "112"),
            createVirtualNextEventDto("horseracing", "334"));
    when(nextEventsService.readByBrandAndActive(BRAND)).thenReturn(virtualNextEventDtos);

    mockIsGroupedFeaturedEnabled(false);

    // when
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, 0).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));

    List<RecentlyPlayedGameDto> rpgData = singletonList(new RecentlyPlayedGameDto().setSportId(0));

    assertThat(resultPages).hasSize(6);

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .hasSize(3)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(RECENTLY_PLAYED_GAMES, FEATURED, QUICK_LINK);
    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(Util.mergeLists(rpgData, homeFeaturedData, homeQuickLinks));

    assertThat(resultPages.get(FOOTBALL_PAGE_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(FOOTBALL_PAGE_ID).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(footballQuickLinks);

    assertThat(resultPages.get(HOKEY_PAGE_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(HOKEY_PAGE_ID).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(hokeyQuickLinks);

    assertThat(resultPages.get(BOXING_PAGE_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(SportModuleType.QUICK_LINK);
    assertThat(resultPages.get(BOXING_PAGE_ID).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(boxingQuickLinks);

    assertThat(resultPages.get(HORSE_RACING_ID).getSportPageModules())
        .hasSize(3)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(
            SportModuleType.RACING_MODULE,
            SportModuleType.RACING_MODULE,
            SportModuleType.RACING_MODULE);
    assertThat(resultPages.get(VIRTUALS_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(VIRTUAL_NEXT_EVENTS);

    assertThat(resultPages.get(HORSE_RACING_ID).getSportPageModules())
        .extracting(
            sportPageModule ->
                ((RacingModuleDto) sportPageModule.getPageData().get(0))
                    .getRacingConfig()
                    .getAbbreviation())
        .containsExactly("LVR", "UIR", "IR");
  }

  @Test
  public void findAllPagesByBrandHappyPathHighlightCorousel() {
    // given
    List<SportModule> featuredModules =
        asList(
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, FEATURED), 0));
    List<SportModule> quickLinkModules =
        asList(
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, QUICK_LINK), 1));
    List<SportModule> rpgModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, RECENTLY_PLAYED_GAMES), -10));
    List<SportModule> virtualHorseRacingModules =
        Arrays.asList(
            createVirtualHorseRacingModule(RacingModuleType.UK_AND_IRISH_RACES, 99.0),
            createVirtualHorseRacingModule(RacingModuleType.INTERNATIONAL_RACES, 100.0),
            createVirtualHorseRacingModule(RacingModuleType.CORAL_LEGENDS, 97.0));
    List<SportModule> unfeaturedModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, UNGROUPED_FEATURED), 42));
    List<SportModule> highlightCorousel =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, HIGHLIGHTS_CAROUSEL), -11));

    List<HighlightCarouselDto> highlightCarouselDtos =
        Arrays.asList(
            createHighlightCarousel(SPORT_HOME_PAGE), createHighlightCarousel(SPORT_HOME_PAGE));
    when(highlightCarouselPublicService.findActiveByBrand(BRAND)).thenReturn(highlightCarouselDtos);

    when(sportModuleService.findByBrand(BRAND))
        .thenReturn(
            Util.mergeLists(
                featuredModules,
                quickLinkModules,
                rpgModules,
                virtualHorseRacingModules,
                unfeaturedModules,
                highlightCorousel));
    when(sportModuleService.findAllActive(BRAND, RECENTLY_PLAYED_GAMES)).thenReturn(rpgModules);
    when(sportModuleService.findAll(BRAND, SportModuleType.RACING_MODULE))
        .thenReturn(virtualHorseRacingModules);

    List<BaseModularContentDto> homeFeaturedData = createHomeFeaturedData(3);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    mockIsGroupedFeaturedEnabled(false);

    // when
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, 0).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));

    List<RecentlyPlayedGameDto> rpgData = singletonList(new RecentlyPlayedGameDto().setSportId(0));

    assertThat(resultPages).hasSize(2);

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .hasSize(2)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(HIGHLIGHTS_CAROUSEL, RECENTLY_PLAYED_GAMES);
    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(Util.mergeLists(rpgData, highlightCarouselDtos));

    assertThat(resultPages.get(HORSE_RACING_ID).getSportPageModules())
        .hasSize(3)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(
            SportModuleType.RACING_MODULE,
            SportModuleType.RACING_MODULE,
            SportModuleType.RACING_MODULE);

    assertThat(resultPages.get(HORSE_RACING_ID).getSportPageModules())
        .extracting(
            sportPageModule ->
                ((RacingModuleDto) sportPageModule.getPageData().get(0))
                    .getRacingConfig()
                    .getAbbreviation())
        .containsExactly("LVR", "UIR", "IR");
  }

  @Test
  public void findAllPagesByBrandHappyPathHighlightCorouselWithLastRun() {
    // given
    List<SportModule> featuredModules =
        asList(
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, FEATURED), 0));
    List<SportModule> quickLinkModules =
        asList(
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, QUICK_LINK), 1));
    List<SportModule> rpgModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, RECENTLY_PLAYED_GAMES), -10));
    List<SportModule> virtualHorseRacingModules =
        Arrays.asList(
            createVirtualHorseRacingModule(RacingModuleType.UK_AND_IRISH_RACES, 99.0),
            createVirtualHorseRacingModule(RacingModuleType.INTERNATIONAL_RACES, 100.0),
            createVirtualHorseRacingModule(RacingModuleType.CORAL_LEGENDS, 97.0));
    List<SportModule> unfeaturedModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, UNGROUPED_FEATURED), 42));
    List<SportModule> highlightCorousel =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, HIGHLIGHTS_CAROUSEL), -11));

    List<HighlightCarouselDto> highlightCarouselDtos =
        Arrays.asList(
            createHighlightCarousel(SPORT_HOME_PAGE), createHighlightCarousel(SPORT_HOME_PAGE));
    when(highlightCarouselPublicService.findActiveByBrand(BRAND)).thenReturn(highlightCarouselDtos);

    when(sportModuleService.findByBrand(BRAND))
        .thenReturn(
            Util.mergeLists(
                featuredModules,
                quickLinkModules,
                rpgModules,
                virtualHorseRacingModules,
                unfeaturedModules,
                highlightCorousel));
    when(sportModuleService.findAllActive(BRAND, RECENTLY_PLAYED_GAMES)).thenReturn(rpgModules);
    when(sportModuleService.findAll(BRAND, SportModuleType.RACING_MODULE))
        .thenReturn(virtualHorseRacingModules);

    List<BaseModularContentDto> homeFeaturedData = createHomeFeaturedData(3);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    mockIsGroupedFeaturedEnabled(false);

    // when
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, System.currentTimeMillis()).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));

    List<RecentlyPlayedGameDto> rpgData = singletonList(new RecentlyPlayedGameDto().setSportId(0));

    assertThat(resultPages).hasSize(2);

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .hasSize(2)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(HIGHLIGHTS_CAROUSEL, RECENTLY_PLAYED_GAMES);
    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(Util.mergeLists(rpgData, highlightCarouselDtos));

    assertThat(resultPages.get(HORSE_RACING_ID).getSportPageModules())
        .hasSize(3)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(
            SportModuleType.RACING_MODULE,
            SportModuleType.RACING_MODULE,
            SportModuleType.RACING_MODULE);

    assertThat(resultPages.get(HORSE_RACING_ID).getSportPageModules())
        .extracting(
            sportPageModule ->
                ((RacingModuleDto) sportPageModule.getPageData().get(0))
                    .getRacingConfig()
                    .getAbbreviation())
        .containsExactly("LVR", "UIR", "IR");
  }

  @Test
  public void findAllPagesByBrandHappyPathForNone() {
    // given
    List<SportModule> featuredModules =
        asList(
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, FEATURED), 0));
    List<SportModule> quickLinkModules =
        asList(
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, QUICK_LINK), 1));
    List<SportModule> rpgModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, RECENTLY_PLAYED_GAMES), -10));
    List<SportModule> virtualHorseRacingModules =
        Arrays.asList(
            createVirtualHorseRacingModule(RacingModuleType.UK_AND_IRISH_RACES, 99.0),
            createVirtualHorseRacingModule(RacingModuleType.INTERNATIONAL_RACES, 100.0),
            createVirtualHorseRacingModule(RacingModuleType.CORAL_LEGENDS, 97.0));
    List<SportModule> unfeaturedModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, UNGROUPED_FEATURED), 42));

    when(sportModuleService.findByBrand(BRAND))
        .thenReturn(
            Util.mergeLists(
                featuredModules,
                quickLinkModules,
                rpgModules,
                virtualHorseRacingModules,
                unfeaturedModules));
    when(sportModuleService.findAllActive(BRAND, RECENTLY_PLAYED_GAMES)).thenReturn(rpgModules);
    when(sportModuleService.findAll(BRAND, SportModuleType.RACING_MODULE))
        .thenReturn(virtualHorseRacingModules);

    List<BaseModularContentDto> homeFeaturedData = createHomeFeaturedData(3);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    mockIsGroupedFeaturedEnabled(false);

    // when
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, 0).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));

    List<RecentlyPlayedGameDto> rpgData = singletonList(new RecentlyPlayedGameDto().setSportId(0));

    assertThat(resultPages).hasSize(2);

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(RECENTLY_PLAYED_GAMES);
    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(Util.mergeLists(rpgData));

    assertThat(resultPages.get(HORSE_RACING_ID).getSportPageModules())
        .hasSize(3)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(
            SportModuleType.RACING_MODULE,
            SportModuleType.RACING_MODULE,
            SportModuleType.RACING_MODULE);

    assertThat(resultPages.get(HORSE_RACING_ID).getSportPageModules())
        .extracting(
            sportPageModule ->
                ((RacingModuleDto) sportPageModule.getPageData().get(0))
                    .getRacingConfig()
                    .getAbbreviation())
        .containsExactly("LVR", "UIR", "IR");
  }

  @Test
  public void findAllPagesByBrandHappyPathForNonewithLastRun() {
    // given
    List<SportModule> featuredModules =
        asList(
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, FEATURED), 0));
    List<SportModule> quickLinkModules =
        asList(
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, QUICK_LINK), 1));
    List<SportModule> rpgModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, RECENTLY_PLAYED_GAMES), -10));
    List<SportModule> virtualHorseRacingModules =
        Arrays.asList(
            createVirtualHorseRacingModule(RacingModuleType.UK_AND_IRISH_RACES, 99.0),
            createVirtualHorseRacingModule(RacingModuleType.INTERNATIONAL_RACES, 100.0),
            createVirtualHorseRacingModule(RacingModuleType.CORAL_LEGENDS, 97.0));
    List<SportModule> unfeaturedModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, UNGROUPED_FEATURED), 42));

    when(sportModuleService.findByBrand(BRAND))
        .thenReturn(
            Util.mergeLists(
                featuredModules,
                quickLinkModules,
                rpgModules,
                virtualHorseRacingModules,
                unfeaturedModules));
    when(sportModuleService.findAllActive(BRAND, RECENTLY_PLAYED_GAMES)).thenReturn(rpgModules);
    when(sportModuleService.findAll(BRAND, SportModuleType.RACING_MODULE))
        .thenReturn(virtualHorseRacingModules);

    List<BaseModularContentDto> homeFeaturedData = createHomeFeaturedData(3);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    mockIsGroupedFeaturedEnabled(false);

    // when
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, System.currentTimeMillis()).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));

    List<RecentlyPlayedGameDto> rpgData = singletonList(new RecentlyPlayedGameDto().setSportId(0));

    assertThat(resultPages).hasSize(2);

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(RECENTLY_PLAYED_GAMES);
    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(Util.mergeLists(rpgData));

    assertThat(resultPages.get(HORSE_RACING_ID).getSportPageModules())
        .hasSize(3)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(
            SportModuleType.RACING_MODULE,
            SportModuleType.RACING_MODULE,
            SportModuleType.RACING_MODULE);

    assertThat(resultPages.get(HORSE_RACING_ID).getSportPageModules())
        .extracting(
            sportPageModule ->
                ((RacingModuleDto) sportPageModule.getPageData().get(0))
                    .getRacingConfig()
                    .getAbbreviation())
        .containsExactly("LVR", "UIR", "IR");
  }

  public List<BaseModularContentDto> createHomeFeaturedData(int len) {
    return IntStream.range(0, len)
        .mapToObj(
            i -> {
              ModularContentDto dto = new ModularContentDto();
              dto.setId(UUID.randomUUID().toString());
              dto.setModuleDtos(Arrays.asList(ModuleDto.builder().title("text").build()));
              dto.setModuleDtos(Arrays.asList(createModuleDto("hi")));
              return dto;
            })
        .collect(Collectors.toList());
  }

  public List<BaseModularContentDto> createRandomFeaturedData(int len) {
    return IntStream.range(0, len)
        .mapToObj(
            i -> {
              ModularContentDto dto = new ModularContentDto();
              dto.setId(UUID.randomUUID().toString());
              dto.setDirectiveName("Featured");
              dto.setModuleDtos(Arrays.asList(createModuleDto("hello")));
              return dto;
            })
        .collect(Collectors.toList());
  }

  public List<BaseModularContentDto> createRandomFeaturedDataWithUngroupedFeatured(
      int len, boolean groupedBySport) {
    return createRandomFeaturedData(len).stream()
        .filter(ModularContentDto.class::isInstance)
        .map(ModularContentDto.class::cast)
        .map(modularContentDto -> createUngroupedModulesDto(modularContentDto, groupedBySport))
        .collect(Collectors.toList());
  }

  private ModularContentDto createUngroupedModulesDto(
      ModularContentDto modularContentDto, boolean groupedBySport) {
    ModuleDto moduleDto = ModuleDto.builder().groupedBySport(groupedBySport).build();
    modularContentDto.setModuleDtos(singletonList(moduleDto));
    return modularContentDto;
  }

  @Test
  public void findHomePagesByBrandWithUngroupedEvents() {
    List<SportModule> featuredModules =
        singletonList(sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, FEATURED), 0));
    List<SportModule> quickLinkModules =
        singletonList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, QUICK_LINK), 1));
    List<SportModule> rpgModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, RECENTLY_PLAYED_GAMES), -10));
    List<SportModule> ungroupedModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, UNGROUPED_FEATURED), 42));
    when(sportModuleService.findByBrand(BRAND))
        .thenReturn(
            Util.mergeLists(featuredModules, quickLinkModules, rpgModules, ungroupedModules));
    when(sportModuleService.findAllActive(BRAND, RECENTLY_PLAYED_GAMES)).thenReturn(rpgModules);

    List<BaseModularContentDto> homeFeaturedData =
        createRandomFeaturedDataWithUngroupedFeatured(3, UNGROUPED);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    List<SportQuickLinkDto> homeQuickLinks =
        asList(
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE));

    when(sportQuickLinkPublicService.findAll(BRAND)).thenReturn(Util.mergeLists(homeQuickLinks));

    // when
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, 0).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));

    // then
    List<RecentlyPlayedGameDto> rpgData = singletonList(new RecentlyPlayedGameDto().setSportId(0));

    assertThat(resultPages).hasSize(2);

    SportPage sportPage = resultPages.get(SPORT_CUSTOMIZED_HOME_PAGE);
    List<SportPageModule> modules = sportPage.getSportPageModules();
    assertThat(modules)
        .hasSize(4)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(RECENTLY_PLAYED_GAMES, FEATURED, QUICK_LINK, UNGROUPED_FEATURED);

    List<SportPageModuleDataItem> pageData = modules.get(2).getPageData();
    assertThat(pageData).hasSize(3);
    SportQuickLinkDto dto = (SportQuickLinkDto) pageData.get(0);
    String customPrefix = PageType.customized.getPrefix() + "0";
    Assert.assertTrue("Must start id with " + customPrefix, dto.getId().startsWith(customPrefix));
    Assert.assertEquals(PageType.customized, dto.getPageType());

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(Util.mergeLists(rpgData, homeFeaturedData, homeQuickLinks));
  }

  @Test
  public void findHomePagesByBrandWithUngroupedEventsWithLastRun() {
    List<SportModule> featuredModules =
        singletonList(sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, FEATURED), 0));
    List<SportModule> quickLinkModules =
        singletonList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, QUICK_LINK), 1));
    List<SportModule> rpgModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, RECENTLY_PLAYED_GAMES), -10));
    List<SportModule> ungroupedModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, UNGROUPED_FEATURED), 42));
    when(sportModuleService.findByBrand(BRAND))
        .thenReturn(
            Util.mergeLists(featuredModules, quickLinkModules, rpgModules, ungroupedModules));
    when(sportModuleService.findAllActive(BRAND, RECENTLY_PLAYED_GAMES)).thenReturn(rpgModules);

    List<BaseModularContentDto> homeFeaturedData =
        createRandomFeaturedDataWithUngroupedFeatured(3, UNGROUPED);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    List<SportQuickLinkDto> homeQuickLinks =
        asList(
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE));

    when(sportQuickLinkPublicService.findAll(BRAND)).thenReturn(Util.mergeLists(homeQuickLinks));

    // when
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, System.currentTimeMillis()).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));

    // then
    List<RecentlyPlayedGameDto> rpgData = singletonList(new RecentlyPlayedGameDto().setSportId(0));

    assertThat(resultPages).hasSize(2);

    SportPage sportPage = resultPages.get(SPORT_CUSTOMIZED_HOME_PAGE);
    List<SportPageModule> modules = sportPage.getSportPageModules();
    assertThat(modules)
        .hasSize(4)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(RECENTLY_PLAYED_GAMES, FEATURED, QUICK_LINK, UNGROUPED_FEATURED);

    List<SportPageModuleDataItem> pageData = modules.get(2).getPageData();
    assertThat(pageData).hasSize(3);
    SportQuickLinkDto dto = (SportQuickLinkDto) pageData.get(0);
    String customPrefix = PageType.customized.getPrefix() + "0";
    Assert.assertTrue("Must start id with " + customPrefix, dto.getId().startsWith(customPrefix));
    Assert.assertEquals(PageType.customized, dto.getPageType());

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(Util.mergeLists(rpgData, homeFeaturedData, homeQuickLinks));
  }

  @Test
  public void findHomePagesByBrandWithUngroupedEventsPresentButNotSupported() {
    List<SportModule> featuredModules =
        singletonList(sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, FEATURED), 0));
    List<SportModule> quickLinkModules =
        singletonList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, QUICK_LINK), 1));
    List<SportModule> rpgModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, RECENTLY_PLAYED_GAMES), -10));
    when(sportModuleService.findByBrand(BRAND))
        .thenReturn(Util.mergeLists(featuredModules, quickLinkModules, rpgModules));
    when(sportModuleService.findAllActive(BRAND, RECENTLY_PLAYED_GAMES)).thenReturn(rpgModules);

    List<BaseModularContentDto> homeFeaturedData =
        createRandomFeaturedDataWithUngroupedFeatured(3, false);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    List<SportQuickLinkDto> homeQuickLinks =
        asList(
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE));
    mockIsGroupedFeaturedEnabled(false);

    // when
    when(sportQuickLinkPublicService.findAll(BRAND)).thenReturn(Util.mergeLists(homeQuickLinks));
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, 0).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));

    // then
    List<RecentlyPlayedGameDto> rpgData = singletonList(new RecentlyPlayedGameDto().setSportId(0));

    assertThat(resultPages).hasSize(1);

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .hasSize(3)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(RECENTLY_PLAYED_GAMES, FEATURED, QUICK_LINK);
    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(Util.mergeLists(rpgData, homeFeaturedData, homeQuickLinks));
  }

  @Test
  public void findHomePagesByBrandWithUngroupedEventsPresentButNotSupportedwithLastRun() {
    List<SportModule> featuredModules =
        singletonList(sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, FEATURED), 0));
    List<SportModule> quickLinkModules =
        singletonList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, QUICK_LINK), 1));
    List<SportModule> rpgModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, RECENTLY_PLAYED_GAMES), -10));
    when(sportModuleService.findByBrand(BRAND))
        .thenReturn(Util.mergeLists(featuredModules, quickLinkModules, rpgModules));
    when(sportModuleService.findAllActive(BRAND, RECENTLY_PLAYED_GAMES)).thenReturn(rpgModules);

    List<BaseModularContentDto> homeFeaturedData =
        createRandomFeaturedDataWithUngroupedFeatured(3, false);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    List<SportQuickLinkDto> homeQuickLinks =
        asList(
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE));
    mockIsGroupedFeaturedEnabled(false);

    // when
    when(sportQuickLinkPublicService.findAll(BRAND)).thenReturn(Util.mergeLists(homeQuickLinks));
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, System.currentTimeMillis()).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));

    // then
    List<RecentlyPlayedGameDto> rpgData = singletonList(new RecentlyPlayedGameDto().setSportId(0));

    assertThat(resultPages).hasSize(1);

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .hasSize(3)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(RECENTLY_PLAYED_GAMES, FEATURED, QUICK_LINK);
    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(Util.mergeLists(rpgData, homeFeaturedData, homeQuickLinks));
  }

  @Test
  public void findHomePagesByBrandWithUngroupedEventsNotPresentButSupported() {
    List<SportModule> featuredModules =
        asList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, FEATURED), 0),
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, UNGROUPED_FEATURED), 0));
    List<SportModule> quickLinkModules =
        singletonList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, QUICK_LINK), 1));
    List<SportModule> rpgModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, RECENTLY_PLAYED_GAMES), -10));
    when(sportModuleService.findByBrand(BRAND))
        .thenReturn(Util.mergeLists(featuredModules, quickLinkModules, rpgModules));
    when(sportModuleService.findAllActive(BRAND, RECENTLY_PLAYED_GAMES)).thenReturn(rpgModules);

    List<BaseModularContentDto> homeFeaturedData =
        createRandomFeaturedDataWithUngroupedFeatured(3, GROUPED);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    List<SportQuickLinkDto> homeQuickLinks =
        asList(
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE));

    when(sportQuickLinkPublicService.findAll(BRAND)).thenReturn(Util.mergeLists(homeQuickLinks));

    // when
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, 0).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));

    // then
    List<RecentlyPlayedGameDto> rpgData = singletonList(new RecentlyPlayedGameDto().setSportId(0));

    assertThat(resultPages).hasSize(2);

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .hasSize(3)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(RECENTLY_PLAYED_GAMES, FEATURED, QUICK_LINK);
    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(Util.mergeLists(rpgData, homeFeaturedData, homeQuickLinks));
  }

  @Test
  public void findHomePagesByBrandWithUngroupedEventsNotPresentButSupportedwithLastRun() {
    List<SportModule> featuredModules =
        asList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, FEATURED), 0),
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, UNGROUPED_FEATURED), 0));
    List<SportModule> quickLinkModules =
        singletonList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, QUICK_LINK), 1));
    List<SportModule> rpgModules =
        singletonList(
            sportModuleOf(
                new SportPageId(SPORT_HOME_PAGE, PageType.sport, RECENTLY_PLAYED_GAMES), -10));
    when(sportModuleService.findByBrand(BRAND))
        .thenReturn(Util.mergeLists(featuredModules, quickLinkModules, rpgModules));
    when(sportModuleService.findAllActive(BRAND, RECENTLY_PLAYED_GAMES)).thenReturn(rpgModules);

    List<BaseModularContentDto> homeFeaturedData =
        createRandomFeaturedDataWithUngroupedFeatured(3, GROUPED);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    List<SportQuickLinkDto> homeQuickLinks =
        asList(
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE));

    when(sportQuickLinkPublicService.findAll(BRAND)).thenReturn(Util.mergeLists(homeQuickLinks));

    // when
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, System.currentTimeMillis()).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));

    // then
    List<RecentlyPlayedGameDto> rpgData = singletonList(new RecentlyPlayedGameDto().setSportId(0));

    assertThat(resultPages).hasSize(2);

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .hasSize(3)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(RECENTLY_PLAYED_GAMES, FEATURED, QUICK_LINK);
    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(Util.mergeLists(rpgData, homeFeaturedData, homeQuickLinks));
  }

  @Test
  public void findAllPagesByBrandNoSportModules() {

    List<BaseModularContentDto> homeFeaturedData = createRandomFeaturedData(3);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    List<SportQuickLinkDto> homeQuickLinks =
        asList(
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE));
    List<SportQuickLinkDto> footballQuickLinks =
        asList(createQuickLink(FOOTBALL_PAGE_ID), createQuickLink(FOOTBALL_PAGE_ID));
    List<SportQuickLinkDto> hokeyQuickLinks = singletonList(createQuickLink(HOKEY_PAGE_ID));
    List<SportQuickLinkDto> boxingQuickLinks =
        asList(createQuickLink(BOXING_PAGE_ID), createQuickLink(BOXING_PAGE_ID));
    when(sportQuickLinkPublicService.findAll(BRAND))
        .thenReturn(
            Util.mergeLists(homeQuickLinks, footballQuickLinks, hokeyQuickLinks, boxingQuickLinks));

    assertThat(sportPagePublicService.findAllPagesByBrand(BRAND, 0)).isEmpty();
  }

  @Test
  public void findAllPagesByBrandNoSportModuleswithLastRun() {

    List<BaseModularContentDto> homeFeaturedData = createRandomFeaturedData(3);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    List<SportQuickLinkDto> homeQuickLinks =
        asList(
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE));
    List<SportQuickLinkDto> footballQuickLinks =
        asList(createQuickLink(FOOTBALL_PAGE_ID), createQuickLink(FOOTBALL_PAGE_ID));
    List<SportQuickLinkDto> hokeyQuickLinks = singletonList(createQuickLink(HOKEY_PAGE_ID));
    List<SportQuickLinkDto> boxingQuickLinks =
        asList(createQuickLink(BOXING_PAGE_ID), createQuickLink(BOXING_PAGE_ID));
    when(sportQuickLinkPublicService.findAll(BRAND))
        .thenReturn(
            Util.mergeLists(homeQuickLinks, footballQuickLinks, hokeyQuickLinks, boxingQuickLinks));

    assertThat(sportPagePublicService.findAllPagesByBrand(BRAND, System.currentTimeMillis()))
        .isEmpty();
  }

  @Test
  public void findAllPagesByBrandNoSportModulesNoModulesData() {
    when(sportQuickLinkPublicService.findAll(BRAND)).thenReturn(Collections.emptyList());

    assertThat(sportPagePublicService.findAllPagesByBrand(BRAND, System.currentTimeMillis()))
        .isEmpty();
  }

  @Test
  public void findAllPagesByBrandNoFeaturedData() {
    List<SportModule> featuredModules =
        asList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, FEATURED), 0),
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, FEATURED), 0),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.eventhub, FEATURED), 0));
    List<SportModule> quickLinkModules =
        asList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, QUICK_LINK), 1),
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, QUICK_LINK), 1));
    when(sportModuleService.findByBrand(BRAND))
        .thenReturn(Util.mergeLists(featuredModules, quickLinkModules));

    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(Collections.emptyList());

    List<SportQuickLinkDto> homeQuickLinks =
        asList(
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE));
    List<SportQuickLinkDto> footballQuickLinks =
        asList(createQuickLink(FOOTBALL_PAGE_ID), createQuickLink(FOOTBALL_PAGE_ID));
    List<SportQuickLinkDto> hokeyQuickLinks = singletonList(createQuickLink(HOKEY_PAGE_ID));
    List<SportQuickLinkDto> boxingQuickLinks =
        asList(createQuickLink(BOXING_PAGE_ID), createQuickLink(BOXING_PAGE_ID));
    when(sportQuickLinkPublicService.findAll(BRAND))
        .thenReturn(
            Util.mergeLists(homeQuickLinks, footballQuickLinks, hokeyQuickLinks, boxingQuickLinks));

    mockIsGroupedFeaturedEnabled(false);
    // when
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, System.currentTimeMillis()).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));

    // then
    assertThat(resultPages).hasSize(4);

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(homeQuickLinks);

    assertThat(resultPages.get(FOOTBALL_PAGE_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(FOOTBALL_PAGE_ID).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(footballQuickLinks);

    assertThat(resultPages.get(HOKEY_PAGE_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(HOKEY_PAGE_ID).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(hokeyQuickLinks);

    assertThat(resultPages.get(BOXING_PAGE_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(BOXING_PAGE_ID).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(boxingQuickLinks);
  }

  @Test
  public void findAllPagesByBrandNoQuickLinksData() {
    List<SportModule> featuredModules =
        asList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, FEATURED), 0),
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, FEATURED), 0));
    List<SportModule> quickLinkModules =
        asList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, QUICK_LINK), 1),
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, QUICK_LINK), 1));
    when(sportModuleService.findByBrand(BRAND))
        .thenReturn(Util.mergeLists(featuredModules, quickLinkModules));

    List<BaseModularContentDto> homeFeaturedData = createRandomFeaturedData(3);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);
    when(sportQuickLinkPublicService.findAll(BRAND)).thenReturn(Collections.emptyList());

    mockIsGroupedFeaturedEnabled(false);
    // when
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, System.currentTimeMillis()).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));
    // then
    assertThat(resultPages).hasSize(1);

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(FEATURED);
  }

  @Test
  public void findAllPagesByBrandNoQuickLinkModules() {
    List<SportModule> featuredModules =
        asList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, FEATURED), 0),
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, FEATURED), 1),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, FEATURED), 0));
    when(sportModuleService.findByBrand(BRAND)).thenReturn(featuredModules);

    List<BaseModularContentDto> homeFeaturedData = createRandomFeaturedData(3);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    List<SportQuickLinkDto> homeQuickLinks =
        asList(
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE),
            createQuickLink(SPORT_HOME_PAGE));
    List<SportQuickLinkDto> footballQuickLinks =
        asList(createQuickLink(FOOTBALL_PAGE_ID), createQuickLink(FOOTBALL_PAGE_ID));
    List<SportQuickLinkDto> hokeyQuickLinks = singletonList(createQuickLink(HOKEY_PAGE_ID));
    List<SportQuickLinkDto> boxingQuickLinks =
        asList(createQuickLink(BOXING_PAGE_ID), createQuickLink(BOXING_PAGE_ID));
    when(sportQuickLinkPublicService.findAll(BRAND))
        .thenReturn(
            Util.mergeLists(homeQuickLinks, footballQuickLinks, hokeyQuickLinks, boxingQuickLinks));
    mockIsGroupedFeaturedEnabled(false);
    // when
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, System.currentTimeMillis()).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));
    // then
    assertThat(resultPages).hasSize(1);

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(FEATURED);
  }

  @Test
  public void findAllPagesByBrandNoFeaturedModulesWithLasUpdateValue() {
    List<SportModule> quickLinkModules =
        asList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, QUICK_LINK), 1),
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, QUICK_LINK), 1));
    when(sportModuleService.findByBrand(BRAND)).thenReturn(quickLinkModules);

    List<BaseModularContentDto> homeFeaturedData = createRandomFeaturedData(3);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    SportQuickLinkDto quickLink1 = createQuickLink(SPORT_HOME_PAGE);
    SportQuickLinkDto quickLink2 = createQuickLink(SPORT_HOME_PAGE);
    SportQuickLinkDto quickLink3 = createQuickLink(SPORT_HOME_PAGE);
    List<SportQuickLinkDto> homeQuickLinks = asList(quickLink1, quickLink2, quickLink3);
    List<SportQuickLinkDto> customQuickLinks =
        asList(
            quickLink1.copy(PageType.customized, "c0"),
            quickLink2.copy(PageType.customized, "c0"),
            quickLink3.copy(PageType.customized, "c0"));
    List<SportQuickLinkDto> footballQuickLinks =
        asList(createQuickLink(FOOTBALL_PAGE_ID), createQuickLink(FOOTBALL_PAGE_ID));
    List<SportQuickLinkDto> hokeyQuickLinks = singletonList(createQuickLink(HOKEY_PAGE_ID));
    List<SportQuickLinkDto> boxingQuickLinks =
        asList(createQuickLink(BOXING_PAGE_ID), createQuickLink(BOXING_PAGE_ID));
    when(sportQuickLinkPublicService.findAll(BRAND))
        .thenReturn(
            Util.mergeLists(homeQuickLinks, footballQuickLinks, hokeyQuickLinks, boxingQuickLinks));

    // when
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, System.currentTimeMillis()).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));

    // then
    assertThat(resultPages).hasSize(5);

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(homeQuickLinks);

    assertThat(resultPages.get(SPORT_CUSTOMIZED_HOME_PAGE).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(SPORT_CUSTOMIZED_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(customQuickLinks);

    assertThat(resultPages.get(FOOTBALL_PAGE_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(FOOTBALL_PAGE_ID).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(footballQuickLinks);

    assertThat(resultPages.get(HOKEY_PAGE_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(HOKEY_PAGE_ID).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(hokeyQuickLinks);

    assertThat(resultPages.get(BOXING_PAGE_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(BOXING_PAGE_ID).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(boxingQuickLinks);
  }

  @Test
  public void findAllPagesByBrandNoFeaturedModules() {
    List<SportModule> quickLinkModules =
        asList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, QUICK_LINK), 1),
            sportModuleOf(new SportPageId(FOOTBALL_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(HOKEY_PAGE_ID, PageType.sport, QUICK_LINK), 0),
            sportModuleOf(new SportPageId(BOXING_PAGE_ID, PageType.sport, QUICK_LINK), 1));
    when(sportModuleService.findByBrand(BRAND)).thenReturn(quickLinkModules);

    List<BaseModularContentDto> homeFeaturedData = createRandomFeaturedData(3);
    when(modularContentPublicService.findByBrand(BRAND)).thenReturn(homeFeaturedData);

    SportQuickLinkDto quickLink1 = createQuickLink(SPORT_HOME_PAGE);
    SportQuickLinkDto quickLink2 = createQuickLink(SPORT_HOME_PAGE);
    SportQuickLinkDto quickLink3 = createQuickLink(SPORT_HOME_PAGE);
    List<SportQuickLinkDto> homeQuickLinks = asList(quickLink1, quickLink2, quickLink3);
    List<SportQuickLinkDto> customQuickLinks =
        asList(
            quickLink1.copy(PageType.customized, "c0"),
            quickLink2.copy(PageType.customized, "c0"),
            quickLink3.copy(PageType.customized, "c0"));
    List<SportQuickLinkDto> footballQuickLinks =
        asList(createQuickLink(FOOTBALL_PAGE_ID), createQuickLink(FOOTBALL_PAGE_ID));
    List<SportQuickLinkDto> hokeyQuickLinks = singletonList(createQuickLink(HOKEY_PAGE_ID));
    List<SportQuickLinkDto> boxingQuickLinks =
        asList(createQuickLink(BOXING_PAGE_ID), createQuickLink(BOXING_PAGE_ID));
    when(sportQuickLinkPublicService.findAll(BRAND))
        .thenReturn(
            Util.mergeLists(homeQuickLinks, footballQuickLinks, hokeyQuickLinks, boxingQuickLinks));

    // when
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, 0).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));

    // then
    assertThat(resultPages).hasSize(5);

    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(SPORT_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(homeQuickLinks);

    assertThat(resultPages.get(SPORT_CUSTOMIZED_HOME_PAGE).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(SPORT_CUSTOMIZED_HOME_PAGE).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(customQuickLinks);

    assertThat(resultPages.get(FOOTBALL_PAGE_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(FOOTBALL_PAGE_ID).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(footballQuickLinks);

    assertThat(resultPages.get(HOKEY_PAGE_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(HOKEY_PAGE_ID).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(hokeyQuickLinks);

    assertThat(resultPages.get(BOXING_PAGE_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(QUICK_LINK);
    assertThat(resultPages.get(BOXING_PAGE_ID).getSportPageModules())
        .flatExtracting(SportPageModule::getPageData)
        .containsOnlyOnceElementsOf(boxingQuickLinks);
  }

  @Test
  public void findAllPagesGroupedForHomePageBySport() {
    List<SportModule> featuredModules =
        asList(
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, FEATURED), 0),
            sportModuleOf(new SportPageId(SPORT_HOME_PAGE, PageType.sport, UNGROUPED_FEATURED), 0));
    when(sportModuleService.findByBrand(BRAND)).thenReturn(featuredModules);
    when(modularContentPublicService.findByBrand(BRAND))
        .thenReturn(
            singletonList(
                createFeaturedData(
                    moduleDto(FOOTBALL_CATEGORY_ID, FOOTBALL_PREMIER_LEAGUE, GROUPED),
                    moduleDto(BASKETBALL_CATEGORY_ID, BASKETBALL_NBA, GROUPED),
                    moduleDto(FOOTBALL_CATEGORY_ID, FOOTBALL_SERIE_A, GROUPED),
                    moduleDto(BASKETBALL_CATEGORY_ID, BASKETBALL_FIBA, GROUPED),
                    moduleDto(FOOTBALL_CATEGORY_ID, FOOTBALL_PRIMERA_DIVISION, GROUPED))));
    // when
    Map<String, SportPage> resultPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, System.currentTimeMillis()).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));
    // then
    assertThat(resultPages).hasSize(2);

    String[] homePageOrder =
        new String[] {
          FOOTBALL_PREMIER_LEAGUE,
          BASKETBALL_NBA,
          FOOTBALL_SERIE_A,
          BASKETBALL_FIBA,
          FOOTBALL_PRIMERA_DIVISION
        };
    String[] nativeHomePageOrder =
        new String[] {
          FOOTBALL_PREMIER_LEAGUE,
          FOOTBALL_SERIE_A,
          FOOTBALL_PRIMERA_DIVISION,
          BASKETBALL_NBA,
          BASKETBALL_FIBA
        };

    assertOrder(resultPages.get(SPORT_HOME_PAGE), homePageOrder);
    assertOrder(resultPages.get(SPORT_CUSTOMIZED_HOME_PAGE), nativeHomePageOrder);
  }

  @Test
  public void testVirtualNextEventsModuleWithBrand() {

    List<SportModule> virtualNextEventsModules =
        Collections.singletonList(createVirtualNextEventsModule(12.0));
    when(sportModuleService.findByBrand(BRAND)).thenReturn(virtualNextEventsModules);
    List<VirtualNextEventDto> virtualNextEventDtos =
        Arrays.asList(
            createVirtualNextEventDto("cricket", "223"), createVirtualNextEventDto("Hocky", "44"));
    when(nextEventsService.readByBrandAndActive(BRAND)).thenReturn(virtualNextEventDtos);
    Map<String, SportPage> sportPages =
        sportPagePublicService.findAllPagesByBrand(BRAND, System.currentTimeMillis()).stream()
            .collect(Collectors.toMap(SportPage::getSportId, Function.identity()));
    assertThat(sportPages).hasSize(1);
    assertThat(sportPages.get(VIRTUALS_ID).getSportPageModules())
        .hasSize(1)
        .extracting(sportPageModule -> sportPageModule.getSportModule().getModuleType())
        .containsExactly(VIRTUAL_NEXT_EVENTS);
  }

  private void mockIsGroupedFeaturedEnabled(boolean value) {
    when(structureService.findValueByProperty(
            BRAND, "NativeConfig", "isGroupedFeaturedOnHomePageEnabled"))
        .thenReturn(Optional.of(value));
  }

  private void assertOrder(SportPage sportPage, String[] expectedLeagues) {
    List<SportPageModuleDataItem> sportPageModuleDataItems =
        sportPage.getSportPageModules().stream()
            .filter(module -> FEATURED.equals(module.getSportModule().getModuleType()))
            .findFirst()
            .get()
            .getPageData();

    ModularContentDto modularContentDto =
        sportPageModuleDataItems.stream()
            .filter(item -> item instanceof ModularContentDto)
            .map(item -> (ModularContentDto) item)
            .filter(item -> FEATURED_DIRECTIVE.equals(item.getDirectiveName()))
            .findFirst()
            .get();

    String[] actualLeagues =
        modularContentDto.getModuleDtos().stream().map(ModuleDto::getTitle).toArray(String[]::new);

    assertThat(actualLeagues).isEqualTo(expectedLeagues);
  }

  public SportQuickLinkDto createQuickLink(String sportId) {
    SportQuickLinkDto sportQuickLinkDto = new SportQuickLinkDto();
    sportQuickLinkDto.setId(UUID.randomUUID().toString()).setPageId(sportId);
    return sportQuickLinkDto;
  }

  public HighlightCarouselDto createHighlightCarousel(String sportId) {
    HighlightCarouselDto dto = new HighlightCarouselDto();
    dto.setId(UUID.randomUUID().toString());
    dto.setPageId(sportId);
    dto.setSportId(Integer.parseInt(sportId));
    dto.setSegmentReferences(getSegmentReference("segment1"));
    return dto;
  }

  private SportModule sportModuleOf(SportPageId sportPageId, double order) {
    SportModule sportModule = new SportModule();

    sportModule.setId(UUID.randomUUID().toString());
    sportModule.setSortOrder(order);
    sportModule.setModuleType(sportPageId.getType());
    sportModule.setPageId(sportModule.getPageId());
    sportModule.setPageType(sportPageId.getPageType());
    sportModule.setSportId(Integer.valueOf(sportPageId.getId()));
    sportModule.setBrand(BRAND);
    sportModule.setDisabled(Boolean.FALSE);
    sportModule.setTitle(RandomStringUtils.randomAlphabetic(5));

    return sportModule;
  }

  private SportModule createVirtualHorseRacingModule(RacingModuleType type, double order) {
    SportModule sportModule = new SportModule();

    sportModule.setId(UUID.randomUUID().toString());
    sportModule.setSortOrder(order);
    sportModule.setModuleType(SportModuleType.RACING_MODULE);
    sportModule.setPageId(sportModule.getPageId());
    sportModule.setPageType(PageType.sport);
    sportModule.setSportId(Integer.valueOf(HORSE_RACING_ID));
    sportModule.setBrand(BRAND);
    sportModule.setDisabled(Boolean.FALSE);
    sportModule.setTitle(type.getTitle());

    RacingModuleConfig racingConfig = new RacingModuleConfig();
    racingConfig.setType(type);
    sportModule.setRacingConfig(racingConfig);
    return sportModule;
  }

  public BaseModularContentDto createFeaturedData(ModuleDto... moduleDtos) {
    ModularContentDto modularContentDto = new ModularContentDto();
    modularContentDto.setDirectiveName(FEATURED_DIRECTIVE);
    modularContentDto.setId(UUID.randomUUID().toString());
    modularContentDto.setModuleDtos(asList(moduleDtos));

    return modularContentDto;
  }

  private static ModuleDto moduleDto(String categoryId, String league, boolean groupedBySport) {
    ModuleDataDto moduleDataDto = new ModuleDataDto();
    moduleDataDto.setCategoryId(categoryId);

    List<ModuleDataDto> moduleDataDtos = new ArrayList<>();
    moduleDataDtos.add(moduleDataDto);

    return ModuleDto.builder()
        .title(league)
        .data(moduleDataDtos)
        .groupedBySport(groupedBySport)
        .displayOrder(0.0)
        .build();
  }

  private ModuleDto createModuleDto(String title) {
    ModuleDto dto = ModuleDto.builder().title(title).build();
    dto.setSegmentReferences(getSegmentReference("segment1"));
    return dto;
  }

  public static List<SegmentReferenceDto> getSegmentReference(String segmentName) {
    List<SegmentReferenceDto> segmentReferences = new ArrayList<>();
    segmentReferences.add(getSegmentReference(segmentName, "10", 1 + Math.random(), 0));
    segmentReferences.add(getSegmentReference(segmentName, "10", 2 + Math.random(), 15));
    return segmentReferences;
  }

  private static SegmentReferenceDto getSegmentReference(
      String segmentName, String pageRefId, double sortOrder, int sec) {
    SegmentReferenceDto dto = new SegmentReferenceDto();
    dto.setSegment(segmentName);
    dto.setDisplayOrder(sortOrder);
    dto.setPageRefId(pageRefId);
    dto.setUpdatedAt(Instant.now().plusSeconds(sec));
    return dto;
  }

  private static SportModule createVirtualNextEventsModule(double sortOrder) {
    SportModule sportModule = new SportModule();

    sportModule.setId(UUID.randomUUID().toString());
    sportModule.setSortOrder(sortOrder);
    sportModule.setModuleType(VIRTUAL_NEXT_EVENTS);
    sportModule.setPageId("39");
    sportModule.setPageType(PageType.sport);
    sportModule.setSportId(Integer.valueOf(VIRTUALS_ID));
    sportModule.setBrand(BRAND);
    sportModule.setDisabled(Boolean.FALSE);
    sportModule.setTitle(
        WordUtils.capitalizeFully(VIRTUAL_NEXT_EVENTS.name().replace("_", " ")) + " Module");
    return sportModule;
  }

  private static VirtualNextEventDto createVirtualNextEventDto(String title, String typeId) {
    VirtualNextEventDto virtualNextEventDto = new VirtualNextEventDto();
    virtualNextEventDto.setTitle(title);
    virtualNextEventDto.setTypeIds(typeId);
    virtualNextEventDto.setSportId(39);
    return virtualNextEventDto;
  }

  private Fanzone getFanzone() {
    Fanzone fanzone = new Fanzone();
    fanzone.setName("Arsenal");
    fanzone.setTeamId("3dsj344kj2h43j32h4");
    fanzone.setActive(true);
    FanzoneConfiguration configuration = new FanzoneConfiguration();
    configuration.setShowBetsBasedOnYourTeam(true);
    configuration.setShowBetsBasedOnOtherFans(true);
    fanzone.setFanzoneConfiguration(configuration);
    return fanzone;
  }

  private SportModule createAemBannerModule() {
    Instant displayFrom = Instant.parse("2019-10-10T10:39:20.640Z");
    Instant displayTo = Instant.parse("2019-10-11T10:39:20.640Z");
    SportModule sportModule = new SportModule();
    sportModule.setSportId(0);
    sportModule.setModuleType(SportModuleType.AEM_BANNERS);
    sportModule.setPageType(PageType.eventhub);

    sportModule.setTitle("Banner #1");

    sportModule.setModuleConfig(
        AemBannersConfig.builder()
            .displayFrom(displayFrom)
            .displayTo(displayTo)
            .maxOffers(7)
            .timePerSlide(8)
            .build());
    return sportModule;
  }
}
