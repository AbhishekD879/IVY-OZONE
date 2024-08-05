package com.oxygen.publisher.sportsfeatured.service;

import static org.mockito.BDDMockito.given;

import com.google.common.cache.Cache;
import com.oxygen.publisher.model.PageType;
import com.oxygen.publisher.sportsfeatured.context.SportsMiddlewareContext;
import com.oxygen.publisher.sportsfeatured.model.*;
import com.oxygen.publisher.sportsfeatured.model.module.*;
import com.oxygen.publisher.sportsfeatured.model.module.data.*;
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.SportSegment;
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.TypeSegment;
import com.oxygen.publisher.translator.AbstractWorker;
import com.oxygen.publisher.translator.DiagnosticService;
import java.math.BigDecimal;
import java.util.*;
import javax.validation.constraints.NotNull;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class AbstractSportsChainFactoryTest {

  @Mock private SportsMiddlewareContext context;
  @Mock private SportsCachedData thisCache;
  @Mock private Cache<ModuleRawIndex, AbstractFeaturedModule<?>> thisModulesCache;

  private FeaturedModel thisHomeModel;
  private FeaturedModel thisFanzoneModel;

  private AbstractSportsChainFactory chainFactory;

  @Before
  public void init() {
    thisHomeModel = FeaturedModel.builder().pageId("0").build();
    thisFanzoneModel = FeaturedModel.builder().pageId("160").build();
    chainFactory =
        new AbstractSportsChainFactory() {
          @Override
          protected SportsMiddlewareContext getContext() {
            return context;
          }

          @Override
          public AbstractWorker getScheduledJob() {
            throw new UnsupportedOperationException("Not implemented.");
          }

          @Override
          public DiagnosticService diagnosticService() {
            return new DiagnosticService(10);
          }
        };
  }

  @Test
  public void processEventsModule_replace_scenario_OK() {
    EventsModule newModule = createValidEventModule("New module");
    EventsModule thisModule = createValidEventModule("This module");
    thisHomeModel.addModule(thisModule);

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(PageRawIndex.HOME_PAGE)).willReturn(thisHomeModel);

    chainFactory.processModule(newModule, thisCache);

    Assert.assertTrue(thisHomeModel.getModules().contains(newModule));
    Assert.assertFalse(thisHomeModel.getModules().contains(thisModule));
  }

  @Test
  public void processEventsModule_replace_Fanzone_Scenario_OK() {
    EventsModule newModule = createValidFanzoneEventModule("New module");
    EventsModule thisModule = createValidFanzoneEventModule("This module");
    thisFanzoneModel.addModule(thisModule);

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(new PageRawIndex(PageType.sport, 160)))
        .willReturn(thisFanzoneModel);

    chainFactory.processModule(newModule, thisCache);

    Assert.assertTrue(thisFanzoneModel.getModules().contains(newModule));
    Assert.assertFalse(thisFanzoneModel.getModules().contains(thisModule));
  }

  @Test
  public void processEventsModuleSegmented_replace_scenario_OK() {
    EventsModule newModule = createValidEventModule("New module");
    newModule.setSegmented(true);
    EventsModule thisModule = createValidEventModule("This module");
    thisModule.setSegmented(true);
    thisHomeModel.addModule(thisModule);
    this.thisHomeModel.setSegmented(true);
    this.thisHomeModel.setSegmentWiseModules(
        new HashMap<String, SegmentView>() {
          {
            put("universal", null);
          }
        });
    newModule.setSegments(new ArrayList<>(Arrays.asList("universal")));

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(PageRawIndex.HOME_PAGE)).willReturn(thisHomeModel);

    chainFactory.processModule(newModule, thisCache);

    Assert.assertTrue(thisHomeModel.getModules().contains(newModule));
    Assert.assertFalse(thisHomeModel.getModules().contains(thisModule));
  }

  @Test
  public void processEventsModuleFanzoneSegmented_replace_scenario_OK() {
    EventsModule newModule = createValidFanzoneEventModule("New module");
    newModule.setSegmented(true);
    EventsModule thisModule = createValidFanzoneEventModule("This module");
    thisModule.setSegmented(true);
    thisFanzoneModel.addModule(thisModule);
    this.thisFanzoneModel.setSegmented(true);
    this.thisFanzoneModel.setFanzoneSegmentWiseModules(
        new HashMap<String, FanzoneSegmentView>() {
          {
            put("universal", null);
          }
        });
    newModule.setFanzoneSegments(new ArrayList<>(Arrays.asList("universal")));

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(new PageRawIndex(PageType.sport, 160)))
        .willReturn(thisFanzoneModel);

    chainFactory.processModule(newModule, thisCache);

    Assert.assertTrue(thisFanzoneModel.getModules().contains(newModule));
    Assert.assertFalse(thisFanzoneModel.getModules().contains(thisModule));
  }

  @Test
  public void processEventsModuleSegmentedModule_replace_scenario_OK() {
    EventsModule newModule = createValidEventSegmentedModule("New module");
    newModule.setSegmented(true);
    EventsModule thisModule = createValidEventModule("This module");
    thisModule.setSegmented(true);
    // thisHomeModel.addModule(thisModule);
    this.thisHomeModel.setSegmented(true);
    SegmentOrderdModule segmentOrderdModule =
        SegmentOrderdModule.builder().eventsModule(thisModule).build();
    SegmentView segmentView =
        SegmentView.builder()
            .eventModules(
                new HashMap<String, SegmentOrderdModule>() {
                  {
                    put("universal", segmentOrderdModule);
                  }
                })
            .build();
    this.thisHomeModel.setSegmentWiseModules(
        new HashMap<String, SegmentView>() {
          {
            put("universal", segmentView);
          }
        });
    newModule.setSegments(new ArrayList<>(Arrays.asList("universal")));

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(PageRawIndex.HOME_PAGE)).willReturn(thisHomeModel);

    chainFactory.processModule(newModule, thisCache);

    // Assert.assertTrue(thisHomeModel.getModules().contains(newModule));
    Assert.assertFalse(thisHomeModel.getModules().contains(thisModule));
  }

  @Test
  public void processQuickLinkModuleSegmentedModule_replace_scenario_OK() {
    QuickLinkModule newModule = createValidQuickLinkSegmentedModule("New module");
    newModule.setSegmented(true);
    newModule.setSegments(new ArrayList<>(Arrays.asList("universal")));

    QuickLinkModule thisModule = createValidQuickLinkModule("This module");
    thisModule.setSegmented(true);
    AbstractModuleData eventData = getAbstractModuleData();

    this.thisHomeModel.setSegmented(true);
    SegmentOrderdModuleData segmentOrderdModule =
        SegmentOrderdModuleData.builder().quickLinkData((QuickLinkData) eventData).build();
    SegmentView segmentView =
        SegmentView.builder()
            .quickLinkData(
                new HashMap<String, SegmentOrderdModuleData>() {
                  {
                    put("universal", segmentOrderdModule);
                  }
                })
            .build();
    this.thisHomeModel.setSegmentWiseModules(
        new HashMap<String, SegmentView>() {
          {
            put("universal", segmentView);
          }
        });

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(PageRawIndex.HOME_PAGE)).willReturn(thisHomeModel);

    chainFactory.processModule(newModule, thisCache);

    // Assert.assertTrue(thisHomeModel.getModules().contains(newModule));
    Assert.assertFalse(thisHomeModel.getModules().contains(thisModule));
  }

  @Test
  public void processSurfacebetModuleSegmentedModule_replace_scenario_OK() {
    SurfaceBetModule newModule = createValidSurfacebetSegmentedModule("New module");

    SurfaceBetModuleData eventData = getSurfaceBetModuleData();

    this.thisHomeModel.setSegmented(true);
    SegmentOrderdModuleData segmentOrderdModule =
        SegmentOrderdModuleData.builder().surfaceBetModuleData(eventData).build();
    SegmentView segmentView =
        SegmentView.builder()
            .surfaceBetModuleData(
                new HashMap<String, SegmentOrderdModuleData>() {
                  {
                    put("universal", segmentOrderdModule);
                  }
                })
            .build();
    this.thisHomeModel.setSegmentWiseModules(
        new HashMap<String, SegmentView>() {
          {
            put("universal", segmentView);
          }
        });

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(PageRawIndex.HOME_PAGE)).willReturn(thisHomeModel);

    chainFactory.processModule(newModule, thisCache);

    Assert.assertFalse(thisHomeModel.getModules().contains(newModule));
  }

  @Test
  public void processSurfacebetModuleFanzoneSegmentedModule_replace_scenario_OK() {
    SurfaceBetModule newModule = createValidSurfacebetFanzoneSegmentedModule("New module");

    SurfaceBetModuleData eventData = getSurfaceBetModuleData();

    this.thisFanzoneModel.setSegmented(true);
    FanzoneSegmentView fanzoneSegmentView =
        FanzoneSegmentView.builder()
            .surfaceBetModuleData(
                new HashMap<String, SurfaceBetModuleData>() {
                  {
                    put("universal", eventData);
                  }
                })
            .build();
    this.thisFanzoneModel.setFanzoneSegmentWiseModules(
        new HashMap<String, FanzoneSegmentView>() {
          {
            put("universal", fanzoneSegmentView);
          }
        });

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(new PageRawIndex(PageType.sport, 160)))
        .willReturn(thisFanzoneModel);

    chainFactory.processModule(newModule, thisCache);

    Assert.assertFalse(thisFanzoneModel.getModules().contains(newModule));
  }

  @Test
  public void processQuickLinkModuleFanzoneSegmentedModule_replace_scenario_OK() {
    QuickLinkModule newModule = createQuickLinkFanzoneSegmentedModule("New module");

    QuickLinkData eventData = getQuickLinkData();

    this.thisFanzoneModel.setSegmented(true);
    FanzoneSegmentView fanzoneSegmentView =
        FanzoneSegmentView.builder()
            .quickLinkModuleData(
                new HashMap<String, QuickLinkData>() {
                  {
                    put("universal", eventData);
                  }
                })
            .build();
    this.thisFanzoneModel.setFanzoneSegmentWiseModules(
        new HashMap<String, FanzoneSegmentView>() {
          {
            put("universal", fanzoneSegmentView);
          }
        });

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(new PageRawIndex(PageType.sport, 160)))
        .willReturn(thisFanzoneModel);

    chainFactory.processModule(newModule, thisCache);

    Assert.assertFalse(thisFanzoneModel.getModules().contains(newModule));
  }

  @Test
  public void processFanBetsModuleFanzoneSegmentedModule_replace_scenario_OK() {
    FanBetsModule newModule = createFanBetsModule("New module");

    FanBetsConfig data = createFanBetsModuleData();

    this.thisFanzoneModel.setSegmented(true);
    FanzoneSegmentView fanzoneSegmentView =
        FanzoneSegmentView.builder()
            .fanBetsModuleData(
                new HashMap<String, FanBetsConfig>() {
                  {
                    put("universal", data);
                  }
                })
            .build();
    this.thisFanzoneModel.setFanzoneSegmentWiseModules(
        new HashMap<String, FanzoneSegmentView>() {
          {
            put("universal", fanzoneSegmentView);
          }
        });

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(new PageRawIndex(PageType.sport, 160)))
        .willReturn(thisFanzoneModel);

    chainFactory.processModule(newModule, thisCache);

    Assert.assertFalse(thisFanzoneModel.getModules().contains(newModule));
  }

  @Test
  public void processTeamBetsModuleFanzoneSegmentedModule_replace_scenario_OK() {
    TeamBetsModule newModule = createTeamBetsModule("New module");

    TeamBetsConfig data = createTeamBetsModuleData();

    this.thisFanzoneModel.setSegmented(true);
    FanzoneSegmentView fanzoneSegmentView =
        FanzoneSegmentView.builder()
            .teamBetsModuleData(
                new HashMap<String, TeamBetsConfig>() {
                  {
                    put("universal", data);
                  }
                })
            .build();
    this.thisFanzoneModel.setFanzoneSegmentWiseModules(
        new HashMap<String, FanzoneSegmentView>() {
          {
            put("universal", fanzoneSegmentView);
          }
        });

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(new PageRawIndex(PageType.sport, 160)))
        .willReturn(thisFanzoneModel);

    chainFactory.processModule(newModule, thisCache);

    Assert.assertFalse(thisFanzoneModel.getModules().contains(newModule));
  }

  @Test
  public void processHighlightCarouselSegmentedModule_replace_scenario_OK() {
    HighlightCarouselModule newModule = createValidHighlightCarouselSegmentedModule("New module");
    HighlightCarouselModule thisModule = createValidHighlightCarouselSegmentedModule("This module");
    this.thisHomeModel.setSegmented(true);
    SegmentOrderdModule segmentOrderdModule =
        SegmentOrderdModule.builder().highlightCarouselModule(thisModule).build();
    SegmentView segmentView =
        SegmentView.builder()
            .highlightCarouselModules(
                new HashMap<String, SegmentOrderdModule>() {
                  {
                    put("universal", segmentOrderdModule);
                  }
                })
            .build();
    this.thisHomeModel.setSegmentWiseModules(
        new HashMap<String, SegmentView>() {
          {
            put("universal", segmentView);
          }
        });
    newModule.setSegments(new ArrayList<>(Arrays.asList("universal")));

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(PageRawIndex.HOME_PAGE)).willReturn(thisHomeModel);

    chainFactory.processModule(newModule, thisCache);

    // Assert.assertTrue(thisHomeModel.getModules().contains(newModule));
    Assert.assertFalse(thisHomeModel.getModules().contains(thisModule));
  }

  @Test
  public void processHighlightCarouselFanzoneSegmentedModule_replace_scenario_OK() {
    HighlightCarouselModule newModule =
        createValidHighlightCarouselFanzoneSegmentedModule("New module");
    HighlightCarouselModule thisModule =
        createValidHighlightCarouselFanzoneSegmentedModule("This module");
    this.thisFanzoneModel.setSegmented(true);
    FanzoneSegmentView fanzoneSegmentView =
        FanzoneSegmentView.builder()
            .highlightCarouselModules(
                new HashMap<String, HighlightCarouselModule>() {
                  {
                    put("universal", thisModule);
                  }
                })
            .build();
    this.thisFanzoneModel.setFanzoneSegmentWiseModules(
        new HashMap<String, FanzoneSegmentView>() {
          {
            put("universal", fanzoneSegmentView);
          }
        });
    newModule.setFanzoneSegments(new ArrayList<>(Arrays.asList("universal")));

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(new PageRawIndex(PageType.sport, 160)))
        .willReturn(thisFanzoneModel);

    chainFactory.processModule(newModule, thisCache);

    // Assert.assertTrue(thisHomeModel.getModules().contains(newModule));
    Assert.assertFalse(thisFanzoneModel.getModules().contains(thisModule));
  }

  @Test
  public void processSegmentedModule_with_no_segments() {
    HighlightCarouselModule newModule = createValidHighlightCarouselSegmentedModule("New module");
    HighlightCarouselModule thisModule = createValidHighlightCarouselSegmentedModule("This module");
    this.thisHomeModel.setSegmented(true);
    SegmentOrderdModule segmentOrderdModule =
        SegmentOrderdModule.builder().highlightCarouselModule(thisModule).build();
    SegmentView segmentView =
        SegmentView.builder()
            .highlightCarouselModules(
                new HashMap<String, SegmentOrderdModule>() {
                  {
                    put("universal", segmentOrderdModule);
                  }
                })
            .build();
    this.thisHomeModel.setSegmentWiseModules(
        new HashMap<String, SegmentView>() {
          {
            put("universal", segmentView);
          }
        });
    newModule.setSegments(null);

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(PageRawIndex.HOME_PAGE)).willReturn(thisHomeModel);

    chainFactory.processModule(newModule, thisCache);

    // Assert.assertTrue(thisHomeModel.getModules().contains(newModule));
    Assert.assertFalse(thisHomeModel.getModules().contains(thisModule));
  }

  @Test
  public void processSegmentedModule_with_no_fanzonesegments() {
    HighlightCarouselModule newModule =
        createValidHighlightCarouselFanzoneSegmentedModule("New module");
    HighlightCarouselModule thisModule =
        createValidHighlightCarouselFanzoneSegmentedModule("This module");
    this.thisHomeModel.setSegmented(true);
    FanzoneSegmentView fanzoneSegmentView =
        FanzoneSegmentView.builder()
            .highlightCarouselModules(
                new HashMap<String, HighlightCarouselModule>() {
                  {
                    put("universal", thisModule);
                  }
                })
            .build();
    this.thisFanzoneModel.setFanzoneSegmentWiseModules(
        new HashMap<String, FanzoneSegmentView>() {
          {
            put("universal", fanzoneSegmentView);
          }
        });
    newModule.setFanzoneSegments(null);

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(new PageRawIndex(PageType.sport, 160)))
        .willReturn(thisFanzoneModel);

    chainFactory.processModule(newModule, thisCache);

    // Assert.assertTrue(thisHomeModel.getModules().contains(newModule));
    Assert.assertFalse(thisFanzoneModel.getModules().contains(thisModule));
  }

  @Test
  public void procesNonSegmentedModuleInSegmentWiseModules_replace_scenario_OK() {
    InplayModule newModule = createValidInplaySegmentedModule("title");
    HighlightCarouselModule thisModule = createValidHighlightCarouselSegmentedModule("This module");
    this.thisHomeModel.setSegmented(true);
    SegmentOrderdModule segmentOrderdModule =
        SegmentOrderdModule.builder().highlightCarouselModule(thisModule).build();
    SegmentView segmentView =
        SegmentView.builder()
            .highlightCarouselModules(
                new HashMap<String, SegmentOrderdModule>() {
                  {
                    put("universal", segmentOrderdModule);
                  }
                })
            .build();
    SegmentOrderdModuleData segmentOrderdModuleData =
        SegmentOrderdModuleData.builder()
            .build()
            .builder()
            .segmentOrder(1.0)
            .inplayData(getInplayModuleData())
            .build();
    Map<String, SegmentOrderdModuleData> inplaySegView =
        new HashMap<String, SegmentOrderdModuleData>() {
          {
            put("universal", segmentOrderdModuleData);
          }
        };
    segmentView.setInplayModuleData(inplaySegView);
    this.thisHomeModel.setSegmentWiseModules(
        new HashMap<String, SegmentView>() {
          {
            put("universal", segmentView);
          }
        });

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(PageRawIndex.HOME_PAGE)).willReturn(thisHomeModel);

    chainFactory.processModule(newModule, thisCache);

    // Assert.assertTrue(thisHomeModel.getModules().contains(newModule));
    Assert.assertFalse(thisHomeModel.getModules().contains(thisModule));
  }

  @Test
  public void processRacingEventsModuleSegmented_replace_scenario_OK() {
    RacingEventsModule newModule = createRacingEventsModuleSegmentedTrue("New module");
    RacingEventsModule thisModule = createRacingEventsModuleSegmentedTrue("This module");
    thisHomeModel.addModule(thisModule);
    this.thisHomeModel.setSegmented(true);

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(PageRawIndex.HOME_PAGE)).willReturn(thisHomeModel);

    chainFactory.processModule(newModule, thisCache);

    Assert.assertFalse(thisHomeModel.getModules().contains(newModule));
    Assert.assertTrue(thisHomeModel.getModules().contains(thisModule));
  }

  @Test
  public void procesNonSegmentedModuleInFanzoneSegmentWiseModules_replace_scenario_OK() {
    InplayModule newModule = new InplayModule();
    newModule.setSportId(160);
    HighlightCarouselModule thisModule =
        createValidHighlightCarouselFanzoneSegmentedModule("This module");
    this.thisFanzoneModel.setSegmented(true);
    FanzoneSegmentView fanzoneSegmentView =
        FanzoneSegmentView.builder()
            .highlightCarouselModules(
                new HashMap<String, HighlightCarouselModule>() {
                  {
                    put("universal", thisModule);
                  }
                })
            .build();
    this.thisFanzoneModel.setFanzoneSegmentWiseModules(
        new HashMap<String, FanzoneSegmentView>() {
          {
            put("universal", fanzoneSegmentView);
          }
        });
    newModule.setFanzoneSegments(new ArrayList<>(Arrays.asList("universal")));

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(new PageRawIndex(PageType.sport, 160)))
        .willReturn(thisFanzoneModel);

    chainFactory.processModule(newModule, thisCache);

    // Assert.assertTrue(thisHomeModel.getModules().contains(newModule));
    Assert.assertFalse(thisFanzoneModel.getModules().contains(thisModule));
  }

  @Test
  public void processVirtualEventsModule_replace_scenario_OK() {
    EventsModule newModule = createValidVirtualEventModule("New module");
    EventsModule thisModule = createValidVirtualEventModule("This module");
    thisHomeModel.addModule(thisModule);

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(PageRawIndex.HOME_PAGE)).willReturn(thisHomeModel);

    chainFactory.processModule(newModule, thisCache);

    Assert.assertTrue(thisHomeModel.getModules().contains(newModule));
    Assert.assertFalse(thisHomeModel.getModules().contains(thisModule));
  }

  @Test
  public void processPopularBetEventsModule_replace_scenario_OK() {
    PopularBetModule newModule = createValidPopularBetModule("New module");
    PopularBetModule thisModule = createValidPopularBetModule("This module");
    thisHomeModel.addModule(thisModule);

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(PageRawIndex.HOME_PAGE)).willReturn(thisHomeModel);

    chainFactory.processModule(newModule, thisCache);

    Assert.assertTrue(thisHomeModel.getModules().contains(newModule));
    Assert.assertFalse(thisHomeModel.getModules().contains(thisModule));
  }

  @Test
  public void processLuckyDipModule_replace_scenario_OK() {
    LuckyDipModule newModule = createLuckyDipModule("Lucky Dip Module");
    PopularBetModule thisModule = createValidPopularBetModule("This module");
    thisHomeModel.addModule(thisModule);

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(PageRawIndex.HOME_PAGE)).willReturn(thisHomeModel);

    chainFactory.processModule(newModule, thisCache);

    Assert.assertFalse(thisHomeModel.getModules().contains(newModule));
    Assert.assertTrue(thisHomeModel.getModules().contains(thisModule));
  }

  @NotNull
  private AbstractModuleData getAbstractModuleData() {
    AbstractModuleData eventData = new QuickLinkData();
    eventData.setId("EVENT ID");
    ((QuickLinkData) eventData).setDestination("https://sports.ladbrokes.com/1-2-free");
    ((QuickLinkData) eventData).setSvgId("0ff5c599-a8cd-3497-8991-77e82bdaebde");
    return eventData;
  }

  private SurfaceBetModuleData getSurfaceBetModuleData() {
    SurfaceBetModuleData eventData = new SurfaceBetModuleData();
    eventData.setId("EVENT ID");
    eventData.setTitle("surfaceBetModuleData");
    eventData.setSvgId("0ff5c599-a8cd-3497-8991-77e82bdaebde");
    return eventData;
  }

  private QuickLinkData getQuickLinkData() {
    QuickLinkData eventData = new QuickLinkData();
    eventData.setId("EVENT ID");
    eventData.setTitle("surfaceBetModuleData");
    eventData.setSvgId("0ff5c599-a8cd-3497-8991-77e82bdaebde");
    eventData.setDisplayOrder(1);
    eventData.setFanzoneSegments(Arrays.asList("universal"));
    return eventData;
  }

  private FanBetsConfig createFanBetsModuleData() {
    FanBetsConfig data = new FanBetsConfig();
    data.setId(UUID.randomUUID().toString());
    data.setNoOfMaxSelections(4);
    data.setGuid("tguid");
    data.setFanzoneSegments(Arrays.asList("universal"));
    return data;
  }

  private TeamBetsConfig createTeamBetsModuleData() {
    TeamBetsConfig data = new TeamBetsConfig();
    data.setId(UUID.randomUUID().toString());
    data.setNoOfMaxSelections(4);
    data.setGuid("tguid");
    data.setFanzoneSegments(Arrays.asList("universal"));
    return data;
  }

  private SportSegment getInplayModuleData() {
    SportSegment eventData = new SportSegment();
    eventData.setId("EVENT ID");
    eventData.setCategoryId(16);
    eventData.setSvgId("0ff5c599-a8cd-3497-8991-77e82bdaebde");
    return eventData;
  }

  @Test
  public void processInPlayModule_OK() {
    InplayModule newInplayModule = createInPlayModule("New Inplay Module");
    InplayModule thisInplayModule = createInPlayModule("This Inplay Module");

    thisHomeModel.addModule(thisInplayModule);

    given(context.getFeaturedCachedData()).willReturn(thisCache);
    given(thisCache.getStructure(PageRawIndex.HOME_PAGE)).willReturn(thisHomeModel);

    chainFactory.processModule(newInplayModule, thisCache);

    Assert.assertTrue(thisHomeModel.getModules().contains(newInplayModule));
    Assert.assertFalse(thisHomeModel.getModules().contains(thisInplayModule));
  }

  /** This case is handled by the structure change */
  @Test(expected = NullPointerException.class)
  public void processEventsModule_replace_scenario_NODATA() {
    EventsModule newModule = createValidEventModule("New module");
    newModule.setData(null);
    EventsModule thisModule = createValidEventModule("This module");
    thisModule.setData(null);
    thisHomeModel.addModule(thisModule);

    chainFactory.processModule(newModule, thisCache);
  }

  private EventsModule createValidEventModule(String title) {
    EventsModuleData eventData = new EventsModuleData();
    eventData.setId("EVENT ID");

    List<EventsModuleData> data = new ArrayList<>();
    data.add(eventData);

    EventsModule thisModule = new EventsModule();
    thisModule.setId("TEST ID");
    thisModule.setSportId(0);
    thisModule.setTitle(title);
    thisModule.setData(data);
    return thisModule;
  }

  private VirtualEventModule createValidVirtualEventModule(String title) {
    EventsModuleData eventData = new EventsModuleData();
    eventData.setId("EVENT ID");

    List<EventsModuleData> data = new ArrayList<>();
    data.add(eventData);

    VirtualEventModule thisModule = new VirtualEventModule();
    thisModule.setId("TEST ID");
    thisModule.setSportId(0);
    thisModule.setTitle(title);
    thisModule.setData(data);
    return thisModule;
  }

  private PopularBetModule createValidPopularBetModule(String title) {
    PopularBetModuleData eventData = new PopularBetModuleData();
    eventData.setId("EVENT ID");

    List<EventsModuleData> data = new ArrayList<>();
    data.add(eventData);

    PopularBetModule thisModule = new PopularBetModule();
    thisModule.setId("TEST ID");
    thisModule.setSportId(0);
    thisModule.setTitle(title);
    thisModule.setData(data);
    return thisModule;
  }

  private EventsModule createValidFanzoneEventModule(String title) {
    EventsModuleData eventData = new EventsModuleData();
    eventData.setId("EVENT ID");

    List<EventsModuleData> data = new ArrayList<>();
    data.add(eventData);

    EventsModule thisModule = new EventsModule();
    thisModule.setId("TEST ID");
    thisModule.setSportId(160);
    thisModule.setTitle(title);
    thisModule.setData(data);
    return thisModule;
  }

  private QuickLinkModule createValidQuickLinkModule(String title) {
    AbstractModuleData eventData = new QuickLinkData();
    eventData.setId("EVENT ID");

    List<AbstractModuleData> data = new ArrayList<>();
    data.add(eventData);

    QuickLinkModule thisModule = new QuickLinkModule();
    thisModule.setId("TEST ID");
    thisModule.setSportId(0);
    thisModule.setTitle(title);
    thisModule.setData(data);
    return thisModule;
  }

  private EventsModule createValidEventSegmentedModule(String title) {
    EventsModuleData eventData = new EventsModuleData();
    eventData.setId("EVENT ID");

    List<EventsModuleData> data = new ArrayList<>();
    data.add(eventData);

    EventsModule thisModule = new EventsModule();
    thisModule.setId("TEST ID");
    thisModule.setSportId(0);
    thisModule.setTitle(title);
    thisModule.setData(data);
    SegmentOrderdModule segmentOrderdModule =
        SegmentOrderdModule.builder().eventsModule(thisModule).build();

    thisModule.setModuleSegmentView(
        new HashMap<String, SegmentView>() {
          {
            put("universal", getSegmentView(segmentOrderdModule));
          }
        });
    return thisModule;
  }

  private SegmentView getSegmentView(SegmentOrderdModule segmentOrderdModule) {
    return SegmentView.builder()
        .eventModules(
            new HashMap<String, SegmentOrderdModule>() {
              {
                put("TEST ID", segmentOrderdModule);
              }
            })
        .build();
  }

  private QuickLinkModule createValidQuickLinkSegmentedModule(String title) {
    AbstractModuleData eventData = getAbstractModuleData();

    List<AbstractModuleData> data = new ArrayList<>();
    data.add(eventData);

    QuickLinkModule thisModule = new QuickLinkModule();
    thisModule.setId("TEST ID");
    thisModule.setId("0");
    thisModule.setTitle(title);
    thisModule.setSegmentOrder(0.1);
    thisModule.setSegments(new ArrayList<>(Arrays.asList("universal")));
    thisModule.setSegmented(true);

    thisModule.setData(data);

    SegmentOrderdModuleData segmentOrderdModule =
        SegmentOrderdModuleData.builder()
            .build()
            .builder()
            .segmentOrder(1.0)
            .quickLinkData((QuickLinkData) eventData)
            .build();

    thisModule.setModuleSegmentView(
        new HashMap<String, SegmentView>() {
          {
            put(
                "universal",
                SegmentView.builder()
                    .quickLinkData(
                        new HashMap<String, SegmentOrderdModuleData>() {
                          {
                            put("universal", segmentOrderdModule);
                          }
                        })
                    .build());
          }
        });

    return thisModule;
  }

  private SurfaceBetModule createValidSurfacebetSegmentedModule(String title) {
    SurfaceBetModuleData eventData = getSurfaceBetModuleData();

    SurfaceBetModule thisModule = new SurfaceBetModule();
    thisModule.setId("TEST ID");
    thisModule.setId("0");
    thisModule.setTitle(title);
    thisModule.setSegmentOrder(0.1);
    thisModule.setSegments(new ArrayList<>(Arrays.asList("universal")));
    thisModule.setSegmented(true);

    SegmentOrderdModuleData segmentOrderdModule =
        SegmentOrderdModuleData.builder()
            .build()
            .builder()
            .segmentOrder(1.0)
            .surfaceBetModuleData(eventData)
            .build();

    thisModule.setModuleSegmentView(
        new HashMap<String, SegmentView>() {
          {
            put(
                "universal",
                SegmentView.builder()
                    .surfaceBetModuleData(
                        new HashMap<String, SegmentOrderdModuleData>() {
                          {
                            put("universal", segmentOrderdModule);
                          }
                        })
                    .build());
          }
        });

    return thisModule;
  }

  private SurfaceBetModule createValidSurfacebetFanzoneSegmentedModule(String title) {
    SurfaceBetModuleData eventData = getSurfaceBetModuleData();

    SurfaceBetModule thisModule = new SurfaceBetModule();
    thisModule.setId("TEST ID");
    thisModule.setSportId(160);
    thisModule.setTitle(title);
    thisModule.setSegmentOrder(0.1);
    thisModule.setFanzoneSegments(new ArrayList<>(Arrays.asList("universal")));
    thisModule.setSegmented(true);

    thisModule.setFanzoneModuleSegmentView(
        new HashMap<String, FanzoneSegmentView>() {
          {
            put(
                "universal",
                FanzoneSegmentView.builder()
                    .surfaceBetModuleData(
                        new HashMap<String, SurfaceBetModuleData>() {
                          {
                            put("universal", eventData);
                          }
                        })
                    .build());
          }
        });

    return thisModule;
  }

  private QuickLinkModule createQuickLinkFanzoneSegmentedModule(String title) {
    QuickLinkData eventData = getQuickLinkData();

    QuickLinkModule thisModule = new QuickLinkModule();
    thisModule.setId("TEST ID");
    thisModule.setSportId(160);
    thisModule.setTitle(title);
    thisModule.setSegmentOrder(0.1);
    thisModule.setFanzoneSegments(new ArrayList<>(Arrays.asList("universal")));
    thisModule.setSegmented(true);

    thisModule.setFanzoneModuleSegmentView(
        new HashMap<String, FanzoneSegmentView>() {
          {
            put(
                "universal",
                FanzoneSegmentView.builder()
                    .quickLinkModuleData(
                        new HashMap<String, QuickLinkData>() {
                          {
                            put("universal", eventData);
                          }
                        })
                    .build());
          }
        });

    return thisModule;
  }

  private FanBetsModule createFanBetsModule(String title) {
    FanBetsModule module = new FanBetsModule();

    module.setSegmented(true);
    module.setPageType(PageType.sport);
    module.setId("fan bets id");
    module.setSportId(160);
    module.setTitle(title);
    module.setSegmentOrder(0.1);
    module.setDisplayOrder(new BigDecimal(1));
    module.setFanzoneSegments(new ArrayList<>(Arrays.asList("universal")));

    module.setData(Arrays.asList(createFanBetsModuleData()));

    module.setFanzoneModuleSegmentView(
        new HashMap<>() {
          {
            put(
                "universal",
                FanzoneSegmentView.builder()
                    .fanBetsModuleData(
                        new HashMap<>() {
                          {
                            put("universal", createFanBetsModuleData());
                          }
                        })
                    .build());
          }
        });
    return module;
  }

  private TeamBetsModule createTeamBetsModule(String title) {
    TeamBetsModule module = new TeamBetsModule();

    module.setSegmented(true);
    module.setPageType(PageType.sport);
    module.setId("team bets id");
    module.setSportId(160);
    module.setTitle(title);
    module.setSegmentOrder(0.1);
    module.setDisplayOrder(new BigDecimal(1));
    module.setFanzoneSegments(new ArrayList<>(Arrays.asList("universal")));

    module.setData(Arrays.asList(createTeamBetsModuleData()));

    module.setFanzoneModuleSegmentView(
        new HashMap<>() {
          {
            put(
                "universal",
                FanzoneSegmentView.builder()
                    .teamBetsModuleData(
                        new HashMap<>() {
                          {
                            put("universal", createTeamBetsModuleData());
                          }
                        })
                    .build());
          }
        });
    return module;
  }

  private HighlightCarouselModule createValidHighlightCarouselSegmentedModule(String title) {
    EventsModuleData eventData = new EventsModuleData();
    eventData.setId("EVENT ID");

    List<EventsModuleData> data = new ArrayList<>();
    data.add(eventData);

    HighlightCarouselModule thisModule = new HighlightCarouselModule();
    thisModule.setId("TEST ID");
    thisModule.setId("0");
    thisModule.setTitle(title);
    thisModule.setSegmentOrder(0.1);
    thisModule.setSegments(new ArrayList<>(Arrays.asList("universal")));
    thisModule.setSegmented(true);
    thisModule.setData(data);

    SegmentOrderdModule segmentOrderdModule =
        SegmentOrderdModule.builder().highlightCarouselModule(thisModule).build();

    thisModule.setModuleSegmentView(
        new HashMap<String, SegmentView>() {
          {
            put(
                "universal",
                SegmentView.builder()
                    .highlightCarouselModules(
                        new HashMap<String, SegmentOrderdModule>() {
                          {
                            put("TEST ID", segmentOrderdModule);
                          }
                        })
                    .build());
          }
        });
    return thisModule;
  }

  private HighlightCarouselModule createValidHighlightCarouselFanzoneSegmentedModule(String title) {
    EventsModuleData eventData = new EventsModuleData();
    eventData.setId("EVENT ID");

    List<EventsModuleData> data = new ArrayList<>();
    data.add(eventData);

    HighlightCarouselModule thisModule = new HighlightCarouselModule();
    thisModule.setId("TEST ID");
    thisModule.setSportId(160);
    thisModule.setTitle(title);
    thisModule.setSegmentOrder(0.1);
    thisModule.setFanzoneSegments(new ArrayList<>(Arrays.asList("universal")));
    thisModule.setSegmented(true);
    thisModule.setData(data);

    thisModule.setFanzoneModuleSegmentView(
        new HashMap<String, FanzoneSegmentView>() {
          {
            put(
                "universal",
                FanzoneSegmentView.builder()
                    .highlightCarouselModules(
                        new HashMap<String, HighlightCarouselModule>() {
                          {
                            put("TEST ID", thisModule);
                          }
                        })
                    .build());
          }
        });
    return thisModule;
  }

  private InplayModule createInPlayModule(String title) {
    InplayModule inplayModule = new InplayModule();
    List<SportSegment> data = new ArrayList<>();
    SportSegment segment = new SportSegment();
    List<TypeSegment> typeSegments = new ArrayList<>();
    TypeSegment typeSegment = new TypeSegment();
    List<EventsModuleData> events = new ArrayList<>();
    EventsModuleData event = new EventsModuleData();
    event.setId("9454374");
    event.setCategoryId("16");
    events.add(event);
    typeSegment.setEvents(events);
    typeSegments.add(typeSegment);
    segment.setEventsByTypeName(typeSegments);
    data.add(segment);
    inplayModule.setData(data);

    inplayModule.setTitle(title);
    inplayModule.setSportId(0);
    inplayModule.setId("INPLAY_ID");

    return inplayModule;
  }

  private InplayModule createValidInplaySegmentedModule(String title) {
    SportSegment eventData = getInplayModuleData();

    List<SportSegment> data = new ArrayList<>();
    data.add(eventData);

    InplayModule thisModule = new InplayModule();
    thisModule.setId("TEST ID");
    thisModule.setId("0");
    thisModule.setTitle(title);
    thisModule.setSegmentOrder(0.1);
    thisModule.setSegments(new ArrayList<>(Arrays.asList("universal")));
    thisModule.setSegmented(true);

    thisModule.setData(data);

    SegmentOrderdModuleData segmentOrderdModule =
        SegmentOrderdModuleData.builder()
            .build()
            .builder()
            .segmentOrder(1.0)
            .inplayData((SportSegment) eventData)
            .build();

    thisModule.setModuleSegmentView(
        new HashMap<String, SegmentView>() {
          {
            put(
                "universal",
                SegmentView.builder()
                    .inplayModuleData(
                        new HashMap<String, SegmentOrderdModuleData>() {
                          {
                            put("universal", segmentOrderdModule);
                          }
                        })
                    .build());
          }
        });

    return thisModule;
  }

  private RacingEventsModule createRacingEventsModuleSegmentedTrue(String title) {
    RacingEventsModuleData racingEventsModuleData = new RacingEventsModuleData();
    racingEventsModuleData.setId("EVENT ID");

    List<RacingEventsModuleData> data = new ArrayList<>();
    data.add(racingEventsModuleData);

    RacingEventsModule racingEventsModule = new RacingEventsModule();
    racingEventsModule.setId("TEST ID");
    racingEventsModule.setSportId(0);
    racingEventsModule.setTitle(title);
    racingEventsModule.setData(data);
    racingEventsModule.setSegmentOrder(0.1);
    racingEventsModule.setSegments(new ArrayList<>(Arrays.asList("universal")));
    racingEventsModule.setSegmented(true);

    return racingEventsModule;
  }

  private LuckyDipModule createLuckyDipModule(String title) {
    LuckyDipModule luckyDipModule = new LuckyDipModule();
    luckyDipModule.setTitle(title);
    luckyDipModule.setType("LuckyDipModule");
    return luckyDipModule;
  }
}
