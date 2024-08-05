package com.oxygen.publisher.sportsfeatured.service;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNotNull;
import static org.mockito.ArgumentMatchers.*;
import static org.mockito.Mockito.*;

import com.corundumstudio.socketio.BroadcastOperations;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.oxygen.publisher.configuration.JsonSupportConfig;
import com.oxygen.publisher.model.PageType;
import com.oxygen.publisher.sportsfeatured.SportsServiceRegistry;
import com.oxygen.publisher.sportsfeatured.context.SportsMiddlewareContext;
import com.oxygen.publisher.sportsfeatured.context.SportsSessionContext;
import com.oxygen.publisher.sportsfeatured.model.*;
import com.oxygen.publisher.sportsfeatured.model.module.*;
import com.oxygen.publisher.sportsfeatured.model.module.data.*;
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.SportSegment;
import com.oxygen.publisher.sportsfeatured.model.module.data.inplay.TypeSegment;
import com.oxygen.publisher.sportsfeatured.visitor.SocketIoRoomSubscriber;
import com.oxygen.publisher.translator.AbstractWorker;
import com.oxygen.publisher.translator.DiagnosticService;
import java.io.IOException;
import java.math.BigDecimal;
import java.util.*;
import java.util.concurrent.atomic.AtomicReference;
import java.util.function.Consumer;
import java.util.function.Supplier;
import java.util.stream.Collectors;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Answers;
import org.mockito.InOrder;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.internal.stubbing.answers.AnswersWithDelay;
import org.mockito.invocation.InvocationOnMock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class SportsChainFactoryTest {
  private String genIds =
      "{\"value\":[{\"type\":\"sport\",\"pageId\":\"0\",\"version\":33544},{\"type\":\"eventhub\",\"pageId\":\"h16\",\"version\":33544},{\"type\":\"sport\",\"pageId\":\"160\",\"version\":33544}]}";

  @Mock(answer = Answers.RETURNS_DEEP_STUBS)
  private SportsMiddlewareContext sportsMiddlewareContext;

  @Mock private ObjectMapper objectMapper;

  @Mock private DiagnosticService diagnosticService;

  @InjectMocks private SportsChainFactory sportsChainFactory;

  @Mock SportsSessionContext sportsSessionContext;

  @Test
  public void addSportPageTest() {

    String generationId = "sport::16::1234";

    PageRawIndex pageRawIndex = PageRawIndex.fromPageId("16");
    doNothing().when(sportsMiddlewareContext).registerNewPageId(pageRawIndex);
    AbstractWorker<PageRawIndex, FeaturedModel> structureChangedWorker =
        sportsChainFactory.addSportPage(generationId);
    structureChangedWorker.start(pageRawIndex);

    verify(sportsMiddlewareContext).registerNewPageId(pageRawIndex);
  }

  @Test
  @Ignore("will be fixed upcoming stories")
  public void deleteSportPageTest() {
    SocketIOServer socketIOServer = mock(SocketIOServer.class);
    SportsCachedData sportsCachedData = mock(SportsCachedData.class);
    SportsServiceRegistry sportsServiceRegistry = mock(SportsServiceRegistry.class);
    when(sportsServiceRegistry.getSportsPageIdRegistration())
        .thenReturn(mock(SportsPageIdRegistration.class));

    PageRawIndex pageRawIndex = PageRawIndex.fromPageId("s10");
    when(sportsCachedData.getStructure(eq(pageRawIndex)))
        .thenReturn(FeaturedModel.builder().pageId("s10").build());
    FeaturedService featuredService = mock(FeaturedService.class);
    when(sportsMiddlewareContext.featuredService()).thenReturn(featuredService);
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketIOServer);
    BroadcastOperations broadcastOperations = mock(BroadcastOperations.class);
    when(socketIOServer.getRoomOperations(anyString())).thenReturn(broadcastOperations);

    SportsMiddlewareContext sportsMiddlewareContextReal =
        new SportsMiddlewareContext(sportsServiceRegistry, sportsCachedData);
    SportsChainFactory sportsChainFactoryInstance =
        new SportsChainFactory(
            sportsMiddlewareContextReal, objectMapper, diagnosticService, sportsSessionContext);

    AbstractWorker<PageRawIndex, FeaturedModel> deleteSportWorker =
        sportsChainFactoryInstance.deleteSportPage("sport::10::123");

    deleteSportWorker.start(pageRawIndex);

    verify(sportsServiceRegistry, atLeastOnce()).getSocketIOServer();
  }

  @Test
  public void collapsedModuleTest() {
    String generationId =
        "eventhub::h1::100"; // generation must be 100 b/c it mocked it FeaturedService#getModule
    String moduleId = "123456";

    FeaturedService featuredService = mock(FeaturedService.class);
    FeaturedModel featuredModel = new FeaturedModel();

    List<AbstractFeaturedModule<?>> modules =
        Arrays.asList(createModule(PageType.eventhub, moduleId, 1));
    modules.forEach(featuredModel::addModule);

    when(sportsMiddlewareContext.featuredService()).thenReturn(featuredService);
    doAnswer(invocation -> acceptFeaturedModel(invocation, featuredModel))
        .when(featuredService)
        .getFeaturedPagesStructure(eq(generationId), any());
    mockFeaturedModuleLoading(featuredService, moduleId, PageType.eventhub, 1);

    PageCacheUpdate thisPageDataSpy =
        spy(new PageCacheUpdate(PageRawIndex.GenerationKey.fromString(generationId)));
    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorker =
        sportsChainFactory.structureChanged(thisPageDataSpy);
    structureChangedWorker.start(generationId);
    InOrder inOrder = inOrder(featuredService, sportsMiddlewareContext);
    inOrder.verify(featuredService).getFeaturedPagesStructure(any(), any());
    inOrder.verify(sportsMiddlewareContext).applyWorkingCache(thisPageDataSpy);
    inOrder.verify(sportsMiddlewareContext).socketIOServer();
  }

  @Test
  public void latestversion() {
    FeaturedService featuredService = mock(FeaturedService.class);
    PageRawIndex.GenerationKey generationKey = new PageRawIndex.GenerationKey();
    PageType pageType = PageType.sport;
    generationKey.setType(pageType);
    generationKey.setPageId("12");
    generationKey.setVersion(12);
    Set<PageRawIndex.GenerationKey> generationKeySet = new HashSet<>();
    generationKeySet.add(generationKey);
    when(sportsMiddlewareContext.featuredService()).thenReturn(featuredService);
    doAnswer(invocation -> acceptPageRawIndex(invocation, generationKeySet))
        .when(featuredService)
        .getLastGeneration(any());
    AbstractWorker<Void, PageRawIndex.GenerationKey> workerVersion =
        sportsChainFactory.workerVersion();
    workerVersion.start(null);
    InOrder inOrder = inOrder(featuredService, sportsMiddlewareContext);
    inOrder.verify(featuredService).getLastGeneration(any());
  }

  @Test
  public void structureWithoutModulesUpdateTest() {
    String generationId =
        "eventhub::h1::100"; // generation must be 100 b/c it mocked it FeaturedService#getModule
    String moduleId = "123456";

    FeaturedService featuredService = mock(FeaturedService.class);
    FeaturedModel featuredModel = new FeaturedModel();

    when(sportsMiddlewareContext.featuredService()).thenReturn(featuredService);
    doAnswer(invocation -> acceptFeaturedModel(invocation, featuredModel))
        .when(featuredService)
        .getFeaturedPagesStructure(eq(generationId), any());
    mockFeaturedEmptyModuleLoading(featuredService, moduleId, PageType.eventhub, 1);

    PageCacheUpdate thisPageDataSpy =
        spy(new PageCacheUpdate(PageRawIndex.GenerationKey.fromString(generationId)));
    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorker =
        sportsChainFactory.structureChanged(thisPageDataSpy);
    structureChangedWorker.start(generationId);
    InOrder inOrder = inOrder(featuredService, sportsMiddlewareContext);
    inOrder.verify(featuredService).getFeaturedPagesStructure(any(), any());
    inOrder.verify(sportsMiddlewareContext).applyWorkingCache(thisPageDataSpy);
    inOrder.verify(sportsMiddlewareContext).socketIOServer();
  }

  @Test
  public void structureChangeWithstructureNullInCache() {
    String generationId = "sport::0::777";
    FeaturedService featuredService = mock(FeaturedService.class);

    FeaturedModel featuredModel = new FeaturedModel();

    doAnswer(invocation -> acceptFeaturedModel(invocation, featuredModel))
        .when(featuredService)
        .getFeaturedPagesStructure(eq(generationId), any());

    when(sportsMiddlewareContext.getFeaturedCachedData().getPrimaryMarketCache())
        .thenReturn(Collections.emptyMap());
    when(sportsMiddlewareContext.getFeaturedCachedData().getStructure(any())).thenReturn(null);
    when(sportsMiddlewareContext.featuredService()).thenReturn(featuredService);
    SocketIOServer socketServer = mock(SocketIOServer.class);
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketServer);
    BroadcastOperations broadcastOperations = mock(BroadcastOperations.class);
    when(socketServer.getRoomOperations(any())).thenReturn(broadcastOperations);

    PageCacheUpdate thisPageDataSpy =
        spy(new PageCacheUpdate(PageRawIndex.GenerationKey.fromString(generationId)));
    AtomicReference<AbstractWorker<PageRawIndex.GenerationKey, AbstractFeaturedModule<?>>>
        populateModulesWorkerSpy = new AtomicReference<>();

    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorker =
        sportsChainFactory.structureChanged(thisPageDataSpy);

    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorkerSpy =
        spy(structureChangedWorker);

    doAnswer(
            invocation ->
                spyOnWorkerPassedToAccept(
                    structureChangedWorker, populateModulesWorkerSpy, invocation))
        .when(structureChangedWorkerSpy)
        .accept(eq(PageRawIndex.GenerationKey.fromString(generationId)), any());

    structureChangedWorkerSpy.start(generationId);

    InOrder inOrder = inOrder(sportsMiddlewareContext);
    inOrder.verify(sportsMiddlewareContext).applyWorkingCache(thisPageDataSpy);
  }

  @Test
  public void mapperTest() throws IOException {
    ObjectMapper mapper = new JsonSupportConfig().objectMapper();
    SportsVersionResponse generations = mapper.readValue(genIds, SportsVersionResponse.class);
    assertNotNull(generations.getValue());
    assertEquals(3, generations.getValue().size());
  }

  @Test
  public void structureChangeWithDifferentModuleTypes() {
    String generationId = "sport::0::777";
    FeaturedService featuredService = mock(FeaturedService.class);

    FeaturedModel featuredModel = new FeaturedModel("0");
    List<AbstractFeaturedModule<?>> expectedEmptyModules =
        Arrays.asList(
            new EventsModule(),
            new RecentlyPlayedGameModule(),
            new HighlightCarouselModule(),
            new QuickLinkModule());
    EventsModule expectedNonEmptyEventsModule = new EventsModule();
    expectedNonEmptyEventsModule.setData(Arrays.asList(eventData(), eventData(), eventData()));

    HighlightCarouselModule expectedNonEmptyHighlightCarouselModule = new HighlightCarouselModule();
    expectedNonEmptyHighlightCarouselModule.setData(Arrays.asList(eventData(), eventData()));

    QuickLinkModule expectedNonEmptyQuickLinkModule = new QuickLinkModule();
    expectedNonEmptyQuickLinkModule.setData(Arrays.asList(quickLinkData(), quickLinkData()));

    RecentlyPlayedGameModule expectedNonEmptyRPGModule = new RecentlyPlayedGameModule();
    expectedNonEmptyRPGModule.setData(Arrays.asList(RpgData()));

    expectedEmptyModules.forEach(featuredModel::addModule);
    featuredModel.addModule(expectedNonEmptyEventsModule);
    featuredModel.addModule(expectedNonEmptyHighlightCarouselModule);
    featuredModel.addModule(expectedNonEmptyQuickLinkModule);
    featuredModel.addModule(expectedNonEmptyRPGModule);

    doAnswer(invocation -> acceptFeaturedModel(invocation, featuredModel))
        .when(featuredService)
        .getFeaturedPagesStructure(eq(generationId), any());

    when(sportsMiddlewareContext.getFeaturedCachedData().getPrimaryMarketCache())
        .thenReturn(Collections.emptyMap());
    when(sportsMiddlewareContext.featuredService()).thenReturn(featuredService);

    PageCacheUpdate thisPageDataSpy =
        spy(new PageCacheUpdate(PageRawIndex.GenerationKey.fromString(generationId)));
    AtomicReference<AbstractWorker<PageRawIndex.GenerationKey, AbstractFeaturedModule<?>>>
        populateModulesWorkerSpy = new AtomicReference<>();

    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorker =
        sportsChainFactory.structureChanged(thisPageDataSpy);

    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorkerSpy =
        spy(structureChangedWorker);

    doAnswer(
            invocation ->
                spyOnWorkerPassedToAccept(
                    structureChangedWorker, populateModulesWorkerSpy, invocation))
        .when(structureChangedWorkerSpy)
        .accept(eq(PageRawIndex.GenerationKey.fromString(generationId)), any());

    structureChangedWorkerSpy.start(generationId);

    expectedEmptyModules.forEach(
        module -> verify(populateModulesWorkerSpy.get()).accept(eq(module), any()));
    verify(thisPageDataSpy).addModule(expectedNonEmptyEventsModule);
    verify(thisPageDataSpy).addModule(expectedNonEmptyHighlightCarouselModule);
    verify(thisPageDataSpy).addModule(expectedNonEmptyQuickLinkModule);

    InOrder inOrder = inOrder(sportsMiddlewareContext);
    inOrder.verify(sportsMiddlewareContext).applyWorkingCache(thisPageDataSpy);
    inOrder.verify(sportsMiddlewareContext).socketIOServer();
  }

  @Test
  public void structureChangeWithSegmentwiseModules() {
    String generationId = "sport::0::777";
    FeaturedService featuredService = mock(FeaturedService.class);

    FeaturedModel featuredModel = new FeaturedModel("0");
    featuredModel.setSegmented(true);
    List<AbstractFeaturedModule<?>> expectedEmptyModules =
        Arrays.asList(new EventsModule(), new HighlightCarouselModule(), new QuickLinkModule());
    EventsModule expectedNonEmptyEventsModule = new EventsModule();
    expectedNonEmptyEventsModule.setData(Arrays.asList(eventData(), eventData(), eventData()));

    HighlightCarouselModule expectedNonEmptyHighlightCarouselModule = new HighlightCarouselModule();
    expectedNonEmptyHighlightCarouselModule.setData(Arrays.asList(eventData(), eventData()));

    QuickLinkModule expectedNonEmptyQuickLinkModule = new QuickLinkModule();
    expectedNonEmptyQuickLinkModule.setDisplayOrder(new BigDecimal(2));
    expectedNonEmptyQuickLinkModule.setData(Arrays.asList(quickLinkData(), quickLinkData()));

    SurfaceBetModule surfaceBetModule = new SurfaceBetModule();
    surfaceBetModule.setDisplayOrder(new BigDecimal(1));
    surfaceBetModule.setData(Arrays.asList(surfaceBetModuleData()));

    RecentlyPlayedGameModule expectedNonEmptyRPGModule = new RecentlyPlayedGameModule();
    expectedNonEmptyRPGModule.setDisplayOrder(new BigDecimal(2));
    expectedNonEmptyRPGModule.setData(Arrays.asList(RpgData()));

    BybWidgetModule bybWidgetModule = new BybWidgetModule();
    bybWidgetModule.setDisplayOrder(new BigDecimal(4));
    bybWidgetModule.setId(UUID.randomUUID().toString());
    bybWidgetModule.setData(Arrays.asList(bybWidgetModuleData()));

    SuperButtonModule superButtonModule = new SuperButtonModule();
    superButtonModule.setDisplayOrder(new BigDecimal(2));
    superButtonModule.setData(Arrays.asList(superButtonData()));

    PopularAccaModule popularAccaModule = new PopularAccaModule();
    popularAccaModule.setDisplayOrder(new BigDecimal(4));
    popularAccaModule.setId(UUID.randomUUID().toString());
    popularAccaModule.setData(Arrays.asList(popularAccaModuleData()));

    expectedEmptyModules.forEach(featuredModel::addModule);
    featuredModel.addModule(expectedNonEmptyEventsModule);
    featuredModel.addModule(expectedNonEmptyHighlightCarouselModule);
    featuredModel.addModule(expectedNonEmptyQuickLinkModule);
    featuredModel.addModule(expectedNonEmptyRPGModule);
    featuredModel.addModule(bybWidgetModule);
    featuredModel.addModule(superButtonModule);
    featuredModel.addModule(popularAccaModule);
    featuredModel.setSurfaceBetModule(surfaceBetModule);
    featuredModel.setQuickLinkModule(expectedNonEmptyQuickLinkModule);
    featuredModel.setInplayModule(createInplayModule("InplayModule"));
    featuredModel.setSegmentWiseModules(segmentWiseModules());

    doAnswer(invocation -> acceptFeaturedModel(invocation, featuredModel))
        .when(featuredService)
        .getFeaturedPagesStructure(eq(generationId), any());

    when(sportsMiddlewareContext.getFeaturedCachedData().getPrimaryMarketCache())
        .thenReturn(Collections.emptyMap());
    when(sportsMiddlewareContext.getFeaturedCachedData().getStructure(any()))
        .thenReturn(featuredModel);
    when(sportsMiddlewareContext.featuredService()).thenReturn(featuredService);
    SocketIOServer socketServer = mock(SocketIOServer.class);
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketServer);
    BroadcastOperations broadcastOperations = mock(BroadcastOperations.class);
    when(socketServer.getRoomOperations(any())).thenReturn(broadcastOperations);
    SocketIOClient socketIOClient = mock(SocketIOClient.class);
    when(broadcastOperations.getClients()).thenReturn(Collections.singletonList(socketIOClient));

    PageCacheUpdate thisPageDataSpy =
        spy(new PageCacheUpdate(PageRawIndex.GenerationKey.fromString(generationId)));
    AtomicReference<AbstractWorker<PageRawIndex.GenerationKey, AbstractFeaturedModule<?>>>
        populateModulesWorkerSpy = new AtomicReference<>();

    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorker =
        sportsChainFactory.structureChanged(thisPageDataSpy);

    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorkerSpy =
        spy(structureChangedWorker);

    doAnswer(
            invocation ->
                spyOnWorkerPassedToAccept(
                    structureChangedWorker, populateModulesWorkerSpy, invocation))
        .when(structureChangedWorkerSpy)
        .accept(eq(PageRawIndex.GenerationKey.fromString(generationId)), any());

    structureChangedWorkerSpy.start(generationId);

    expectedEmptyModules.forEach(
        module -> verify(populateModulesWorkerSpy.get()).accept(eq(module), any()));
    verify(thisPageDataSpy).addModule(expectedNonEmptyEventsModule);
    verify(thisPageDataSpy).addModule(expectedNonEmptyHighlightCarouselModule);
    verify(thisPageDataSpy).addModule(expectedNonEmptyQuickLinkModule);

    InOrder inOrder = inOrder(sportsMiddlewareContext);
    inOrder.verify(sportsMiddlewareContext).applyWorkingCache(thisPageDataSpy);
  }

  @Test
  public void structureChangeWithFanzoneSegmentwiseModules() {
    String generationId = "sport::160::777";
    FeaturedService featuredService = mock(FeaturedService.class);

    FeaturedModel featuredModel = new FeaturedModel("160");
    featuredModel.setSegmented(true);
    List<AbstractFeaturedModule<?>> expectedEmptyModules =
        Arrays.asList(new HighlightCarouselModule());

    HighlightCarouselModule expectedNonEmptyHighlightCarouselModule = new HighlightCarouselModule();
    expectedNonEmptyHighlightCarouselModule.setData(Arrays.asList(eventData(), eventData()));

    SurfaceBetModule surfaceBetModule = new SurfaceBetModule();
    surfaceBetModule.setDisplayOrder(new BigDecimal(1));
    surfaceBetModule.setData(Arrays.asList(surfaceBetModuleData()));

    QuickLinkModule quickLinkModule = new QuickLinkModule();
    quickLinkModule.setDisplayOrder(new BigDecimal(1));
    quickLinkModule.setData(Arrays.asList(quickLinkData()));

    TeamBetsModule teamBetsModule = createTeamBetsModule(PageType.sport, "tid", 160, "segment");
    FanBetsModule fanBetsModule = createFanBetsModule(PageType.sport, "tid", 160, "segment");

    expectedEmptyModules.forEach(featuredModel::addModule);
    featuredModel.addModule(expectedNonEmptyHighlightCarouselModule);
    featuredModel.setSurfaceBetModule(surfaceBetModule);
    featuredModel.setQuickLinkModule(quickLinkModule);
    featuredModel.setTeamBetsModule(teamBetsModule);
    featuredModel.setFanBetsModule(fanBetsModule);
    featuredModel.setSegmentWiseModules(null);
    featuredModel.setFanzoneSegmentWiseModules(fanzoneSegmentWiseModules());

    doAnswer(invocation -> acceptFeaturedModel(invocation, featuredModel))
        .when(featuredService)
        .getFeaturedPagesStructure(eq(generationId), any());

    when(sportsMiddlewareContext.getFeaturedCachedData().getPrimaryMarketCache())
        .thenReturn(Collections.emptyMap());
    when(sportsMiddlewareContext.getFeaturedCachedData().getStructure(any()))
        .thenReturn(featuredModel);
    when(sportsMiddlewareContext.featuredService()).thenReturn(featuredService);
    SocketIOServer socketServer = mock(SocketIOServer.class);
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketServer);
    BroadcastOperations broadcastOperations = mock(BroadcastOperations.class);
    when(socketServer.getRoomOperations(any())).thenReturn(broadcastOperations);
    SocketIOClient socketIOClient = mock(SocketIOClient.class);
    when(broadcastOperations.getClients()).thenReturn(Collections.singletonList(socketIOClient));

    PageCacheUpdate thisPageDataSpy =
        spy(new PageCacheUpdate(PageRawIndex.GenerationKey.fromString(generationId)));
    AtomicReference<AbstractWorker<PageRawIndex.GenerationKey, AbstractFeaturedModule<?>>>
        populateModulesWorkerSpy = new AtomicReference<>();

    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorker =
        sportsChainFactory.structureChanged(thisPageDataSpy);

    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorkerSpy =
        spy(structureChangedWorker);

    doAnswer(
            invocation ->
                spyOnWorkerPassedToAccept(
                    structureChangedWorker, populateModulesWorkerSpy, invocation))
        .when(structureChangedWorkerSpy)
        .accept(eq(PageRawIndex.GenerationKey.fromString(generationId)), any());

    structureChangedWorkerSpy.start(generationId);

    expectedEmptyModules.forEach(
        module -> verify(populateModulesWorkerSpy.get()).accept(eq(module), any()));
    verify(thisPageDataSpy).addModule(expectedNonEmptyHighlightCarouselModule);

    InOrder inOrder = inOrder(sportsMiddlewareContext);
    inOrder.verify(sportsMiddlewareContext).applyWorkingCache(thisPageDataSpy);
  }

  @Test
  public void structureChangeWithFanzoneSegmentwiseModulesWith21stTeamId() {
    String generationId = "sport::160::777";
    FeaturedService featuredService = mock(FeaturedService.class);
    FeaturedModel featuredModel = new FeaturedModel("160");
    featuredModel.setSegmented(true);
    List<AbstractFeaturedModule<?>> expectedEmptyModules =
        Arrays.asList(new HighlightCarouselModule());
    HighlightCarouselModule expectedNonEmptyHighlightCarouselModule = new HighlightCarouselModule();
    expectedNonEmptyHighlightCarouselModule.setData(Arrays.asList(highlightCarouselData()));
    SurfaceBetModule surfaceBetModule = new SurfaceBetModule();
    surfaceBetModule.setDisplayOrder(new BigDecimal(1));
    surfaceBetModule.setData(Arrays.asList(surfaceBetModuleData()));
    QuickLinkModule quickLinkModule = new QuickLinkModule();
    quickLinkModule.setDisplayOrder(new BigDecimal(1));
    quickLinkModule.setData(Arrays.asList(quickLinkData()));
    expectedEmptyModules.forEach(featuredModel::addModule);
    featuredModel.addModule(expectedNonEmptyHighlightCarouselModule);
    featuredModel.setSurfaceBetModule(surfaceBetModule);
    featuredModel.setQuickLinkModule(quickLinkModule);
    featuredModel.setSegmentWiseModules(null);
    Map<String, FanzoneSegmentView> fanzoneSegmentViewMap = fanzoneSegmentWiseModules();
    fanzoneSegmentViewMap =
        fanzoneSegmentViewMap.entrySet().stream()
            .collect(
                Collectors.toMap(
                    entry -> entry.getKey().contains("Universal") ? "FZ001" : entry.getKey(),
                    Map.Entry::getValue));
    featuredModel.setFanzoneSegmentWiseModules(fanzoneSegmentViewMap);
    doAnswer(invocation -> acceptFeaturedModel(invocation, featuredModel))
        .when(featuredService)
        .getFeaturedPagesStructure(eq(generationId), any());
    when(sportsMiddlewareContext.getFeaturedCachedData().getPrimaryMarketCache())
        .thenReturn(Collections.emptyMap());
    when(sportsMiddlewareContext.getFeaturedCachedData().getStructure(any()))
        .thenReturn(featuredModel);
    when(sportsMiddlewareContext.featuredService()).thenReturn(featuredService);
    SocketIOServer socketServer = mock(SocketIOServer.class);
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketServer);
    BroadcastOperations broadcastOperations = mock(BroadcastOperations.class);
    when(socketServer.getRoomOperations(any())).thenReturn(broadcastOperations);
    SocketIOClient socketIOClient = mock(SocketIOClient.class);
    when(broadcastOperations.getClients()).thenReturn(Collections.singletonList(socketIOClient));
    PageCacheUpdate thisPageDataSpy =
        spy(new PageCacheUpdate(PageRawIndex.GenerationKey.fromString(generationId)));
    AtomicReference<AbstractWorker<PageRawIndex.GenerationKey, AbstractFeaturedModule<?>>>
        populateModulesWorkerSpy = new AtomicReference<>();
    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorker =
        sportsChainFactory.structureChanged(thisPageDataSpy);
    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorkerSpy =
        spy(structureChangedWorker);
    doAnswer(
            invocation ->
                spyOnWorkerPassedToAccept(
                    structureChangedWorker, populateModulesWorkerSpy, invocation))
        .when(structureChangedWorkerSpy)
        .accept(eq(PageRawIndex.GenerationKey.fromString(generationId)), any());
    structureChangedWorkerSpy.start(generationId);
    expectedEmptyModules.forEach(
        module -> verify(populateModulesWorkerSpy.get()).accept(eq(module), any()));
    verify(thisPageDataSpy).addModule(expectedNonEmptyHighlightCarouselModule);
    InOrder inOrder = inOrder(sportsMiddlewareContext);
    inOrder.verify(sportsMiddlewareContext).applyWorkingCache(thisPageDataSpy);
  }

  @Test
  public void structureChangeWithoutSegmentwiseModules() {
    String generationId = "sport::0::777";
    FeaturedService featuredService = mock(FeaturedService.class);

    FeaturedModel featuredModel = new FeaturedModel("0");
    featuredModel.setSegmented(true);
    List<AbstractFeaturedModule<?>> expectedEmptyModules =
        Arrays.asList(new EventsModule(), new HighlightCarouselModule(), new QuickLinkModule());
    EventsModule expectedNonEmptyEventsModule = new EventsModule();
    expectedNonEmptyEventsModule.setData(Arrays.asList(eventData(), eventData(), eventData()));

    HighlightCarouselModule expectedNonEmptyHighlightCarouselModule = new HighlightCarouselModule();
    expectedNonEmptyHighlightCarouselModule.setData(Arrays.asList(eventData(), eventData()));

    QuickLinkModule expectedNonEmptyQuickLinkModule = new QuickLinkModule();
    expectedNonEmptyQuickLinkModule.setDisplayOrder(new BigDecimal(2));
    expectedNonEmptyQuickLinkModule.setData(Arrays.asList(quickLinkData(), quickLinkData()));

    SurfaceBetModule surfaceBetModule = new SurfaceBetModule();
    surfaceBetModule.setDisplayOrder(new BigDecimal(1));
    surfaceBetModule.setData(Arrays.asList(surfaceBetModuleData()));

    RecentlyPlayedGameModule expectedNonEmptyRPGModule = new RecentlyPlayedGameModule();
    expectedNonEmptyRPGModule.setDisplayOrder(new BigDecimal(2));
    expectedNonEmptyRPGModule.setData(Arrays.asList(RpgData()));

    expectedEmptyModules.forEach(featuredModel::addModule);
    featuredModel.addModule(expectedNonEmptyEventsModule);
    featuredModel.addModule(expectedNonEmptyHighlightCarouselModule);
    featuredModel.addModule(expectedNonEmptyQuickLinkModule);
    featuredModel.addModule(expectedNonEmptyRPGModule);
    featuredModel.setSurfaceBetModule(surfaceBetModule);
    featuredModel.setQuickLinkModule(expectedNonEmptyQuickLinkModule);
    featuredModel.setSegmentWiseModules(null);

    doAnswer(invocation -> acceptFeaturedModel(invocation, featuredModel))
        .when(featuredService)
        .getFeaturedPagesStructure(eq(generationId), any());

    when(sportsMiddlewareContext.getFeaturedCachedData().getPrimaryMarketCache())
        .thenReturn(Collections.emptyMap());
    when(sportsMiddlewareContext.getFeaturedCachedData().getStructure(any()))
        .thenReturn(featuredModel);
    when(sportsMiddlewareContext.featuredService()).thenReturn(featuredService);
    SocketIOServer socketServer = mock(SocketIOServer.class);
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketServer);
    BroadcastOperations broadcastOperations = mock(BroadcastOperations.class);
    when(socketServer.getRoomOperations(any())).thenReturn(broadcastOperations);

    PageCacheUpdate thisPageDataSpy =
        spy(new PageCacheUpdate(PageRawIndex.GenerationKey.fromString(generationId)));
    AtomicReference<AbstractWorker<PageRawIndex.GenerationKey, AbstractFeaturedModule<?>>>
        populateModulesWorkerSpy = new AtomicReference<>();

    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorker =
        sportsChainFactory.structureChanged(thisPageDataSpy);

    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorkerSpy =
        spy(structureChangedWorker);

    doAnswer(
            invocation ->
                spyOnWorkerPassedToAccept(
                    structureChangedWorker, populateModulesWorkerSpy, invocation))
        .when(structureChangedWorkerSpy)
        .accept(eq(PageRawIndex.GenerationKey.fromString(generationId)), any());

    structureChangedWorkerSpy.start(generationId);

    expectedEmptyModules.forEach(
        module -> verify(populateModulesWorkerSpy.get()).accept(eq(module), any()));
    verify(thisPageDataSpy).addModule(expectedNonEmptyEventsModule);
    verify(thisPageDataSpy).addModule(expectedNonEmptyHighlightCarouselModule);
    verify(thisPageDataSpy).addModule(expectedNonEmptyQuickLinkModule);

    InOrder inOrder = inOrder(sportsMiddlewareContext);
    inOrder.verify(sportsMiddlewareContext).applyWorkingCache(thisPageDataSpy);
  }

  @Test
  public void structureChangeWithoutFanzoneSegmentwiseModules() {
    String generationId = "sport::160::777";
    FeaturedService featuredService = mock(FeaturedService.class);

    FeaturedModel featuredModel = new FeaturedModel("160");
    featuredModel.setSegmented(true);
    List<AbstractFeaturedModule<?>> expectedEmptyModules =
        Arrays.asList(new HighlightCarouselModule());
    HighlightCarouselModule expectedNonEmptyHighlightCarouselModule = new HighlightCarouselModule();
    expectedNonEmptyHighlightCarouselModule.setData(Arrays.asList(eventData(), eventData()));

    SurfaceBetModule surfaceBetModule = new SurfaceBetModule();
    surfaceBetModule.setDisplayOrder(new BigDecimal(1));
    surfaceBetModule.setData(Arrays.asList(surfaceBetModuleData()));

    QuickLinkModule quickLinkModule = new QuickLinkModule();
    quickLinkModule.setDisplayOrder(new BigDecimal(1));
    quickLinkModule.setData(Arrays.asList(quickLinkData()));

    expectedEmptyModules.forEach(featuredModel::addModule);
    featuredModel.addModule(expectedNonEmptyHighlightCarouselModule);
    featuredModel.setQuickLinkModule(quickLinkModule);
    featuredModel.setSurfaceBetModule(surfaceBetModule);
    featuredModel.setFanzoneSegmentWiseModules(null);

    doAnswer(invocation -> acceptFeaturedModel(invocation, featuredModel))
        .when(featuredService)
        .getFeaturedPagesStructure(eq(generationId), any());

    when(sportsMiddlewareContext.getFeaturedCachedData().getPrimaryMarketCache())
        .thenReturn(Collections.emptyMap());
    when(sportsMiddlewareContext.getFeaturedCachedData().getStructure(any()))
        .thenReturn(featuredModel);
    when(sportsMiddlewareContext.featuredService()).thenReturn(featuredService);
    SocketIOServer socketServer = mock(SocketIOServer.class);
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketServer);
    BroadcastOperations broadcastOperations = mock(BroadcastOperations.class);
    when(socketServer.getRoomOperations(any())).thenReturn(broadcastOperations);

    PageCacheUpdate thisPageDataSpy =
        spy(new PageCacheUpdate(PageRawIndex.GenerationKey.fromString(generationId)));
    AtomicReference<AbstractWorker<PageRawIndex.GenerationKey, AbstractFeaturedModule<?>>>
        populateModulesWorkerSpy = new AtomicReference<>();

    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorker =
        sportsChainFactory.structureChanged(thisPageDataSpy);

    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorkerSpy =
        spy(structureChangedWorker);

    doAnswer(
            invocation ->
                spyOnWorkerPassedToAccept(
                    structureChangedWorker, populateModulesWorkerSpy, invocation))
        .when(structureChangedWorkerSpy)
        .accept(eq(PageRawIndex.GenerationKey.fromString(generationId)), any());

    structureChangedWorkerSpy.start(generationId);

    expectedEmptyModules.forEach(
        module -> verify(populateModulesWorkerSpy.get()).accept(eq(module), any()));
    verify(thisPageDataSpy).addModule(expectedNonEmptyHighlightCarouselModule);

    InOrder inOrder = inOrder(sportsMiddlewareContext);
    inOrder.verify(sportsMiddlewareContext).applyWorkingCache(thisPageDataSpy);
  }

  @Test
  public void acceptTest() {

    SocketIOClient socketIOClient = mock(SocketIOClient.class);
    SocketIoRoomSubscriber visitor =
        spy(new SocketIoRoomSubscriber(socketIOClient, sportsSessionContext));
    HighlightCarouselModule highlightCarouselModule =
        createSegmentedHighlightCarouselModule(PageType.sport, "HC", 0);
    highlightCarouselModule.accept(visitor, "segment");
    verify(visitor).visit(highlightCarouselModule);
  }

  @Test
  public void acceptTestVirtualEventModule() {

    SocketIOClient socketIOClient = mock(SocketIOClient.class);
    SocketIoRoomSubscriber visitor =
        spy(new SocketIoRoomSubscriber(socketIOClient, sportsSessionContext));
    VirtualEventModule virtualEventModule = new VirtualEventModule();
    virtualEventModule.accept(visitor);
    verify(visitor).visit(virtualEventModule);
  }

  @Test
  public void acceptTestPopularBetModule() {

    SocketIOClient socketIOClient = mock(SocketIOClient.class);
    SocketIoRoomSubscriber visitor =
        spy(new SocketIoRoomSubscriber(socketIOClient, sportsSessionContext));
    PopularBetModule popularBetModule = new PopularBetModule();
    popularBetModule.accept(visitor);
    verify(visitor).visit(popularBetModule);
  }

  @Test(expected = CloneNotSupportedException.class)
  public void copyWithEmptySegmentedDataTest() {
    QuickLinkData quickLinkData =
        new QuickLinkData() {
          @Override
          public QuickLinkData clone() throws CloneNotSupportedException {
            throw new CloneNotSupportedException("Clone Not Supported.");
          }
        };
    quickLinkData.setId(UUID.randomUUID().toString());

    String generationId = "sport::0::777";
    FeaturedService featuredService = mock(FeaturedService.class);
    FeaturedModel featuredModel = new FeaturedModel("0");
    featuredModel.setSegmented(true);

    QuickLinkModule expectedNonEmptyQuickLinkModule = new QuickLinkModule();
    expectedNonEmptyQuickLinkModule.setDisplayOrder(new BigDecimal(2));
    expectedNonEmptyQuickLinkModule.setData(Arrays.asList(quickLinkData));

    featuredModel.addModule(expectedNonEmptyQuickLinkModule);
    featuredModel.setQuickLinkModule(expectedNonEmptyQuickLinkModule);

    Map<String, SegmentView> segmentWiseModules = new HashMap();
    SegmentView segmentView = new SegmentView();
    quickLinkData.setSegmentOrder(2);
    SegmentOrderdModuleData segmentOrderdQlModuleData =
        new SegmentOrderdModuleData(quickLinkData.getSegmentOrder(), quickLinkData);
    segmentView.getQuickLinkData().put(quickLinkData.getId(), segmentOrderdQlModuleData);
    segmentWiseModules.put("Universal", segmentView);
    segmentWiseModules.put("segment-one", segmentView);
    featuredModel.setSegmentWiseModules(segmentWiseModules);

    doAnswer(invocation -> acceptFeaturedModel(invocation, featuredModel))
        .when(featuredService)
        .getFeaturedPagesStructure(eq(generationId), any());

    when(sportsMiddlewareContext.getFeaturedCachedData().getPrimaryMarketCache())
        .thenReturn(Collections.emptyMap());
    when(sportsMiddlewareContext.getFeaturedCachedData().getStructure(any()))
        .thenReturn(featuredModel);
    when(sportsMiddlewareContext.featuredService()).thenReturn(featuredService);
    PageCacheUpdate thisPageDataSpy =
        spy(new PageCacheUpdate(PageRawIndex.GenerationKey.fromString(generationId)));
    AtomicReference<AbstractWorker<PageRawIndex.GenerationKey, AbstractFeaturedModule<?>>>
        populateModulesWorkerSpy = new AtomicReference<>();

    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorker =
        sportsChainFactory.structureChanged(thisPageDataSpy);

    AbstractWorker<String, PageRawIndex.GenerationKey> structureChangedWorkerSpy =
        spy(structureChangedWorker);

    doAnswer(
            invocation ->
                spyOnWorkerPassedToAccept(
                    structureChangedWorker, populateModulesWorkerSpy, invocation))
        .when(structureChangedWorkerSpy)
        .accept(eq(PageRawIndex.GenerationKey.fromString(generationId)), any());

    structureChangedWorkerSpy.start(generationId);
  }

  @Test
  public void acceptTestLuckyDipModule() {

    SocketIOClient socketIOClient = mock(SocketIOClient.class);
    SocketIoRoomSubscriber visitor =
        spy(new SocketIoRoomSubscriber(socketIOClient, sportsSessionContext));
    LuckyDipModule luckyDipModule = new LuckyDipModule();
    luckyDipModule.accept(visitor);
    verify(visitor).visit(luckyDipModule);
  }

  private Map<String, SegmentView> segmentWiseModules() {
    Map<String, SegmentView> segmentWiseModules = new HashMap();
    SegmentView segmentView = new SegmentView();

    HighlightCarouselModule highlightCarouselModule = new HighlightCarouselModule();
    highlightCarouselModule.setDisplayOrder(new BigDecimal(3));
    highlightCarouselModule.setId(UUID.randomUUID().toString());
    SegmentOrderdModule segmentOrderdHcModule =
        new SegmentOrderdModule(
            highlightCarouselModule.getDisplayOrder().doubleValue(), highlightCarouselModule);
    segmentView
        .getHighlightCarouselModules()
        .put(highlightCarouselModule.getId(), segmentOrderdHcModule);

    EventsModule eventsModule = new EventsModule();
    eventsModule.setDisplayOrder(new BigDecimal(4));
    eventsModule.setId(UUID.randomUUID().toString());
    eventsModule.setData(Arrays.asList(eventData(), eventData(), eventData()));
    SegmentOrderdModule segmentOrderdEventModule =
        new SegmentOrderdModule(eventsModule.getDisplayOrder().doubleValue(), eventsModule);
    segmentView.getEventModules().put(eventsModule.getId(), segmentOrderdEventModule);

    QuickLinkData quickLinkData = quickLinkData();
    quickLinkData.setSegmentOrder(2);
    SegmentOrderdModuleData segmentOrderdQlModuleData =
        new SegmentOrderdModuleData(quickLinkData.getSegmentOrder(), quickLinkData);
    segmentView.getQuickLinkData().put(quickLinkData.getId(), segmentOrderdQlModuleData);

    SurfaceBetModuleData surfaceBetModuleData = surfaceBetModuleData();
    surfaceBetModuleData.setSegmentOrder(1);
    SegmentOrderdModuleData segmentOrderdSbModuleData =
        new SegmentOrderdModuleData(surfaceBetModuleData.getSegmentOrder(), surfaceBetModuleData);
    segmentView
        .getSurfaceBetModuleData()
        .put(surfaceBetModuleData.getId(), segmentOrderdSbModuleData);

    InplayModule inplayModule = createInplayModule("InplayModule");
    SegmentOrderdModuleData segmentOrderdModuleForInplay =
        new SegmentOrderdModuleData(1, inplayModule.getData().get(0));
    List<SegmentedEvents> limitedEvents = new ArrayList<>();
    SegmentedEvents segmentedEvents = new SegmentedEvents();
    TypeSegment eventByTypeName = new TypeSegment();
    EventsModuleData eventsModuleData = new EventsModuleData();
    List<EventsModuleData> events = new ArrayList<>();
    events.add(eventsModuleData);
    segmentedEvents.setEventByTypeName(eventByTypeName);
    segmentedEvents.setEvents(events);
    limitedEvents.add(segmentedEvents);
    segmentOrderdModuleForInplay.setLimitedEvents(limitedEvents);
    segmentView.getInplayModuleData().put(inplayModule.getId(), segmentOrderdModuleForInplay);

    segmentWiseModules.put("Universal", segmentView);
    segmentWiseModules.put("segment-one", segmentView);

    return segmentWiseModules;
  }

  private Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules() {
    Map<String, FanzoneSegmentView> fanzoneSegmentWiseModules = new HashMap();
    FanzoneSegmentView fanzoneSegmentView = new FanzoneSegmentView();

    HighlightCarouselModule highlightCarouselModule = new HighlightCarouselModule();
    highlightCarouselModule.setDisplayOrder(new BigDecimal(3));
    highlightCarouselModule.setId(UUID.randomUUID().toString());
    fanzoneSegmentView
        .getHighlightCarouselModules()
        .put(highlightCarouselModule.getId(), highlightCarouselModule);

    SurfaceBetModuleData surfaceBetModuleData = surfaceBetModuleData();
    surfaceBetModuleData.setSegmentOrder(1);
    fanzoneSegmentView
        .getSurfaceBetModuleData()
        .put(surfaceBetModuleData.getId(), surfaceBetModuleData);

    QuickLinkModule quickLinkModule = new QuickLinkModule();
    QuickLinkData quickLinkData = quickLinkData();
    quickLinkData.setSegmentOrder(1);
    quickLinkData.setFanzoneSegments(Arrays.asList(quickLinkData.getId()));
    quickLinkModule.setData(Arrays.asList(quickLinkData));
    fanzoneSegmentView.getQuickLinkModuleData().put(quickLinkData.getId(), quickLinkData);

    TeamBetsConfig teamBetsModuleData = createTeamBetsModuleData();
    fanzoneSegmentView.getTeamBetsModuleData().put(teamBetsModuleData.getId(), teamBetsModuleData);

    FanBetsConfig fanBetsModuleData = createFanBetsModuleData();
    fanzoneSegmentView.getFanBetsModuleData().put(fanBetsModuleData.getId(), fanBetsModuleData);

    fanzoneSegmentWiseModules.put("Universal", fanzoneSegmentView);
    fanzoneSegmentWiseModules.put("segment-one", fanzoneSegmentView);

    return fanzoneSegmentWiseModules;
  }

  private QuickLinkData quickLinkData() {
    QuickLinkData quickLinkData = new QuickLinkData();
    quickLinkData.setId(UUID.randomUUID().toString());

    return quickLinkData;
  }

  private SurfaceBetModuleData surfaceBetModuleData() {
    SurfaceBetModuleData surfaceBetModuleData = new SurfaceBetModuleData();
    surfaceBetModuleData.setId(UUID.randomUUID().toString());

    return surfaceBetModuleData;
  }

  private BybWidgetModuleData bybWidgetModuleData() {
    BybWidgetModuleData bybWidgetModuleData = new BybWidgetModuleData();
    bybWidgetModuleData.setId(UUID.randomUUID().toString());

    return bybWidgetModuleData;
  }

  private PopularAccaModuleData popularAccaModuleData() {
    PopularAccaModuleData popularAccaModuleData = new PopularAccaModuleData();
    popularAccaModuleData.setId(UUID.randomUUID().toString());

    TrendingPosition position = new TrendingPosition();
    PopularBetModuleData betData = new PopularBetModuleData();
    betData.setId("123");
    position.setEvent(betData);
    popularAccaModuleData.setPositions(Arrays.asList(position));

    return popularAccaModuleData;
  }

  private RpgConfig RpgData() {
    RpgConfig rpgConfig = new RpgConfig();
    rpgConfig.setTitle(UUID.randomUUID().toString());

    return rpgConfig;
  }

  private SuperButtonConfig superButtonData() {
    SuperButtonConfig config = new SuperButtonConfig();
    config.setPageId(0);

    return config;
  }

  private EventsModuleData eventData() {
    EventsModuleData eventsModuleData = new EventsModuleData();
    eventsModuleData.setId(UUID.randomUUID().toString());

    return eventsModuleData;
  }

  /**
   * This is an ugly but probably the only way to spy on Worker passed to {@link
   * AbstractWorker#accept(java.lang.Object, java.util.function.Supplier)}.
   *
   * @param targetWorker worker from which {@code accept} is being called. We need an original
   *     object instead of spy to be able to invoke method on it
   * @param workerSpyHolder holds Worker we need to spy on. Required due to limitation on assigning
   *     variables from lambdas
   * @param invocation mockito invocation on spy
   */
  private AbstractWorker spyOnWorkerPassedToAccept(
      AbstractWorker<String, PageRawIndex.GenerationKey> targetWorker,
      AtomicReference<AbstractWorker<PageRawIndex.GenerationKey, AbstractFeaturedModule<?>>>
          workerSpyHolder,
      InvocationOnMock invocation)
      throws Throwable {
    AbstractWorker<PageRawIndex.GenerationKey, AbstractFeaturedModule<?>> workerSpy =
        spy(((Supplier<AbstractWorker>) invocation.getArgument(1)).get());

    workerSpyHolder.set(workerSpy);

    invocation
        .getMethod()
        .invoke(
            targetWorker, invocation.getArgument(0), (Supplier<AbstractWorker>) () -> workerSpy);

    return targetWorker;
  }

  private Void acceptFeaturedModel(InvocationOnMock invocationOnMock, FeaturedModel featuredModel) {
    Arrays.stream(invocationOnMock.getArguments())
        .filter(arg -> Consumer.class.isAssignableFrom(arg.getClass()))
        .findFirst()
        .map(Consumer.class::cast)
        .ifPresent(consumer -> consumer.accept(featuredModel));

    return null;
  }

  private Void acceptPageRawIndex(
      InvocationOnMock invocationOnMock, Set<PageRawIndex.GenerationKey> generationKeySet) {
    Arrays.stream(invocationOnMock.getArguments())
        .filter(arg -> Consumer.class.isAssignableFrom(arg.getClass()))
        .findFirst()
        .map(Consumer.class::cast)
        .ifPresent(consumer -> consumer.accept(generationKeySet));

    return null;
  }

  @Test
  public void testModuleContentChangedWithJoinToRoomByContent() {
    when(sportsMiddlewareContext.getFeaturedCachedData()).thenReturn(new SportsCachedData(10, 30));
    SocketIOServer socketServer = mock(SocketIOServer.class);
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketServer);
    when(socketServer.getRoomOperations(any())).thenReturn(mock(BroadcastOperations.class));
    SocketIOClient socketIOClient = mock(SocketIOClient.class);
    when(socketServer.getAllClients()).thenReturn(Collections.singletonList(socketIOClient));
    when(socketIOClient.getAllRooms()).thenReturn(Collections.singleton("someRoom"));

    FeaturedService mock = mock(FeaturedService.class);
    mockFeaturedModuleLoading(
        mock,
        "123456",
        PageType.eventhub,
        6,
        () -> createEventsModule(PageType.eventhub, "event123", 6));

    when(sportsMiddlewareContext.featuredService()).thenReturn(mock);
    String[] keyHub = {"123456", "100"};
    sportsChainFactory.moduleContentChanged().start(keyHub);

    verify(socketIOClient, timeout(1000).times(1)).joinRoom("event123");
  }

  @Test
  public void testModuleContentChanged() {
    when(sportsMiddlewareContext.getFeaturedCachedData()).thenReturn(new SportsCachedData(10, 30));
    SocketIOServer socketServer = mock(SocketIOServer.class);
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketServer);
    when(socketServer.getRoomOperations(any())).thenReturn(mock(BroadcastOperations.class));
    FeaturedService mock = mock(FeaturedService.class);

    mockFeaturedModuleLoading(mock, "123456", PageType.eventhub, 6);
    when(sportsMiddlewareContext.featuredService()).thenReturn(mock);
    String[] keyHub = {"123456", "100"};
    sportsChainFactory.moduleContentChanged().start(keyHub);
    verify(sportsMiddlewareContext, times(1)).socketIOServer();

    mockFeaturedModuleLoading(mock, "12345", PageType.sport, 16);
    when(sportsMiddlewareContext.featuredService()).thenReturn(mock);
    String[] keySport = {"12345", "100"};
    sportsChainFactory.moduleContentChanged().start(keySport);
  }

  @Test
  public void testSegmentedModuleContentChanged() {
    when(sportsMiddlewareContext.getFeaturedCachedData()).thenReturn(new SportsCachedData(10, 30));
    SocketIOServer socketServer = mock(SocketIOServer.class);
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketServer);
    when(socketServer.getRoomOperations(any())).thenReturn(mock(BroadcastOperations.class));
    FeaturedService mock = mock(FeaturedService.class);

    mockFeaturedSegmentedQuickLinkModuleLoading(
        mock, "12345", PageType.sport, 0, true, "Universal");
    when(sportsMiddlewareContext.featuredService()).thenReturn(mock);
    String[] keySport = {"12345", "100"};
    sportsChainFactory.moduleContentChanged().start(keySport);

    mockFeaturedSegmentedSurfaceBetModuleLoading(
        mock, "12345", PageType.sport, 0, true, "Universal");
    when(sportsMiddlewareContext.featuredService()).thenReturn(mock);
    sportsChainFactory.moduleContentChanged().start(keySport);

    mockFeaturedSegmentedHighlightCarouselModuleLoading(mock, "12345", PageType.sport, 0, true);
    when(sportsMiddlewareContext.featuredService()).thenReturn(mock);
    sportsChainFactory.moduleContentChanged().start(keySport);

    mockFeaturedSegmentedQuickLinkModuleLoading(mock, "12345", PageType.sport, 0, true, "segment");
    when(sportsMiddlewareContext.featuredService()).thenReturn(mock);
    sportsChainFactory.moduleContentChanged().start(keySport);

    mockFeaturedSegmentedSurfaceBetModuleLoading(mock, "12345", PageType.sport, 0, true, "segment");
    when(sportsMiddlewareContext.featuredService()).thenReturn(mock);
    sportsChainFactory.moduleContentChanged().start(keySport);

    mockFeaturedSegmentedInplayModuleLoading(mock, "12345", PageType.sport, 0, true, "segment");
    when(sportsMiddlewareContext.featuredService()).thenReturn(mock);
    sportsChainFactory.moduleContentChanged().start(keySport);

    mockFeaturedSegmentedInplayModuleLoading(mock, "12345", PageType.sport, 0, true, "Universal");
    when(sportsMiddlewareContext.featuredService()).thenReturn(mock);
    sportsChainFactory.moduleContentChanged().start(keySport);

    verify(sportsMiddlewareContext, timeout(1000).times(7)).featuredService();
  }

  @Test
  public void testFanzoneSegmentedModuleContentChanged() {
    when(sportsMiddlewareContext.getFeaturedCachedData()).thenReturn(new SportsCachedData(10, 30));
    SocketIOServer socketServer = mock(SocketIOServer.class);
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketServer);
    when(socketServer.getRoomOperations(any())).thenReturn(mock(BroadcastOperations.class));
    FeaturedService mock = mock(FeaturedService.class);

    mockFeaturedFanzoneSegmentedHighlightCarouselModuleLoading(
        mock, "12345", PageType.sport, 160, true);
    when(sportsMiddlewareContext.featuredService()).thenReturn(mock);
    String[] keySport = {"12345", "100"};
    sportsChainFactory.moduleContentChanged().start(keySport);

    mockFeaturedFanzoneSegmentedSurfaceBetModuleLoading(
        mock, "12345", PageType.sport, 160, true, "segment");
    when(sportsMiddlewareContext.featuredService()).thenReturn(mock);
    sportsChainFactory.moduleContentChanged().start(keySport);

    mockFeaturedFanzoneSegmentedQuickLinkLoading(
        mock, "12345", PageType.sport, 160, true, "segment");
    when(sportsMiddlewareContext.featuredService()).thenReturn(mock);
    sportsChainFactory.moduleContentChanged().start(keySport);

    verify(sportsMiddlewareContext, timeout(1000).times(3)).featuredService();
  }

  @Test
  public void testFanzoneSegmentedModuleContentChangedTeamBets() {
    when(sportsMiddlewareContext.getFeaturedCachedData()).thenReturn(new SportsCachedData(10, 30));
    SocketIOServer socketServer = mock(SocketIOServer.class);
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketServer);
    when(socketServer.getRoomOperations(any())).thenReturn(mock(BroadcastOperations.class));
    FeaturedService mock = mock(FeaturedService.class);
    String[] keySport = {"12345", "100"};
    List<Integer> sportIds = new ArrayList<>(Arrays.asList(160, 60));
    sportIds.forEach(
        sportId -> {
          mockFeaturedFanzoneSegmentedTeamBetsModuleLoading(
              mock, "12345", PageType.sport, sportId, true, "segment");
          when(sportsMiddlewareContext.featuredService()).thenReturn(mock);
          sportsChainFactory.moduleContentChanged().start(keySport);
        });
    verify(sportsMiddlewareContext, timeout(1000).times(2)).featuredService();
  }

  @Test
  public void testFanzoneSegmentedModuleContentChangedFanBets() {
    when(sportsMiddlewareContext.getFeaturedCachedData()).thenReturn(new SportsCachedData(10, 30));
    SocketIOServer socketServer = mock(SocketIOServer.class);
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketServer);
    when(socketServer.getRoomOperations(any())).thenReturn(mock(BroadcastOperations.class));
    FeaturedService mock = mock(FeaturedService.class);
    String[] keySport = {"12345", "100"};
    List<Integer> sportIds = new ArrayList<>(Arrays.asList(160, 60));
    sportIds.forEach(
        sportId -> {
          mockFeaturedFanzoneSegmentedFanBetsModuleLoading(
              mock, "12345", PageType.sport, sportId, true, "segment");
          when(sportsMiddlewareContext.featuredService()).thenReturn(mock);
          sportsChainFactory.moduleContentChanged().start(keySport);
        });
    verify(sportsMiddlewareContext, timeout(1000).times(2)).featuredService();
  }

  private void mockFeaturedFanzoneSegmentedFanBetsModuleLoading(
      FeaturedService mock,
      String id,
      final PageType pageType,
      final int sportId,
      boolean createModule,
      String segment) {
    mockFeaturedModuleLoading(
        mock,
        id,
        pageType,
        sportId,
        createModule ? () -> createFanBetsModule(pageType, id, sportId, segment) : () -> null);
  }

  private FanBetsModule createFanBetsModule(
      PageType pageType, String id, int sportId, String segment) {
    FanBetsModule module = new FanBetsModule();
    module.setData(Arrays.asList(createFanBetsModuleData()));
    module.setSegmented(true);
    module.setPageType(pageType);
    module.setId(id);
    module.setSportId(sportId);
    module.setTitle("team bets");
    module.setSegmentOrder(0.1);
    module.setDisplayOrder(new BigDecimal(1));
    module.setFanzoneModuleSegmentView(
        new HashMap<>() {
          {
            put(
                segment,
                FanzoneSegmentView.builder()
                    .fanBetsModuleData(
                        new HashMap<>() {
                          {
                            put(segment, createFanBetsModuleData());
                          }
                        })
                    .build());
          }
        });
    return module;
  }

  private void mockFeaturedFanzoneSegmentedTeamBetsModuleLoading(
      FeaturedService mock,
      String id,
      final PageType pageType,
      final int sportId,
      boolean createModule,
      String segment) {
    mockFeaturedModuleLoading(
        mock,
        id,
        pageType,
        sportId,
        createModule ? () -> createTeamBetsModule(pageType, id, sportId, segment) : () -> null);
  }

  private TeamBetsModule createTeamBetsModule(
      PageType pageType, String id, int sportId, String segment) {
    TeamBetsModule module = new TeamBetsModule();
    module.setData(Arrays.asList(createTeamBetsModuleData()));
    module.setSegmented(true);
    module.setPageType(pageType);
    module.setId(id);
    module.setSportId(sportId);
    module.setTitle("team bets");
    module.setSegmentOrder(0.1);
    module.setDisplayOrder(new BigDecimal(1));
    module.setFanzoneModuleSegmentView(
        new HashMap<>() {
          {
            put(
                segment,
                FanzoneSegmentView.builder()
                    .teamBetsModuleData(
                        new HashMap<>() {
                          {
                            put(segment, createTeamBetsModuleData());
                          }
                        })
                    .build());
          }
        });
    return module;
  }

  private TeamBetsConfig createTeamBetsModuleData() {
    TeamBetsConfig data = new TeamBetsConfig();
    data.setId(UUID.randomUUID().toString());
    data.setNoOfMaxSelections(4);
    data.setGuid("tguid");
    data.setSegmentOrder(0.1);
    data.setFanzoneSegments(Arrays.asList("seg1", "seg2", "seg3", "seg4"));
    return data;
  }

  private FanBetsConfig createFanBetsModuleData() {
    FanBetsConfig data = new FanBetsConfig();
    data.setId(UUID.randomUUID().toString());
    data.setNoOfMaxSelections(4);
    data.setGuid("tguid");
    data.setFanzoneSegments(Arrays.asList("seg1", "seg2", "seg3", "seg4"));
    return data;
  }

  private void mockFeaturedModuleLoading(
      FeaturedService mock,
      String id,
      final PageType pageType,
      final int sportId,
      Supplier<? extends AbstractFeaturedModule<?>> moduleSupplier) {
    doAnswer(
            new AnswersWithDelay(
                500,
                invocation -> {
                  Consumer<AbstractFeaturedModule<?>> consumer = invocation.getArgument(2);
                  consumer.accept(moduleSupplier.get());
                  return null;
                }))
        .when(mock)
        .getModule(eq(id), eq("100"), any(Consumer.class));
  }

  private void mockFeaturedModuleLoading(
      FeaturedService mock,
      String id,
      final PageType pageType,
      final int sportId,
      boolean createModule) {
    mockFeaturedModuleLoading(
        mock,
        id,
        pageType,
        sportId,
        createModule ? () -> createModule(pageType, id, sportId) : () -> null);
  }

  private void mockFeaturedSegmentedQuickLinkModuleLoading(
      FeaturedService mock,
      String id,
      final PageType pageType,
      final int sportId,
      boolean createModule,
      String segment) {
    mockFeaturedModuleLoading(
        mock,
        id,
        pageType,
        sportId,
        createModule
            ? () -> createSegmentedQuickLinkModule(pageType, id, sportId, segment)
            : () -> null);
  }

  private void mockFeaturedSegmentedSurfaceBetModuleLoading(
      FeaturedService mock,
      String id,
      final PageType pageType,
      final int sportId,
      boolean createModule,
      String segment) {
    mockFeaturedModuleLoading(
        mock,
        id,
        pageType,
        sportId,
        createModule
            ? () -> createSegmentedSurfaceBetModule(pageType, id, sportId, segment)
            : () -> null);
  }

  private void mockFeaturedSegmentedHighlightCarouselModuleLoading(
      FeaturedService mock,
      String id,
      final PageType pageType,
      final int sportId,
      boolean createModule) {
    mockFeaturedModuleLoading(
        mock,
        id,
        pageType,
        sportId,
        createModule
            ? () -> createSegmentedHighlightCarouselModule(pageType, id, sportId)
            : () -> null);
  }

  private void mockFeaturedFanzoneSegmentedSurfaceBetModuleLoading(
      FeaturedService mock,
      String id,
      final PageType pageType,
      final int sportId,
      boolean createModule,
      String segment) {
    mockFeaturedModuleLoading(
        mock,
        id,
        pageType,
        sportId,
        createModule
            ? () -> createFanzoneSegmentedSurfaceBetModule(pageType, id, sportId, segment)
            : () -> null);
  }

  private void mockFeaturedFanzoneSegmentedQuickLinkLoading(
      FeaturedService mock,
      String id,
      final PageType pageType,
      final int sportId,
      boolean createModule,
      String segment) {
    mockFeaturedModuleLoading(
        mock,
        id,
        pageType,
        sportId,
        createModule
            ? () -> createFanzoneSegmentedQuickLinkModule(pageType, id, sportId, segment)
            : () -> null);
  }

  private void mockFeaturedFanzoneSegmentedHighlightCarouselModuleLoading(
      FeaturedService mock,
      String id,
      final PageType pageType,
      final int sportId,
      boolean createModule) {
    mockFeaturedModuleLoading(
        mock,
        id,
        pageType,
        sportId,
        createModule
            ? () -> createFanzoneSegmentedHighlightCarouselModule(pageType, id, sportId)
            : () -> null);
  }

  private void mockFeaturedModuleLoading(
      FeaturedService mock, String id, final PageType pageType, final int sportId) {
    mockFeaturedModuleLoading(mock, id, pageType, sportId, true);
  }

  private void mockFeaturedEmptyModuleLoading(
      FeaturedService mock, String id, final PageType pageType, final int sportId) {
    mockFeaturedModuleLoading(mock, id, pageType, sportId, false);
  }

  private void mockFeaturedSegmentedInplayModuleLoading(
      FeaturedService mock,
      String id,
      final PageType pageType,
      final int sportId,
      boolean createModule,
      String segment) {
    mockFeaturedModuleLoading(
        mock,
        id,
        pageType,
        sportId,
        createModule
            ? () -> createSegmentedInplayModule(pageType, id, sportId, segment)
            : () -> null);
  }

  private QuickLinkModule createModule(PageType eventhub, String id, int sportId) {
    QuickLinkModule quickLinkModule = new QuickLinkModule();
    quickLinkModule.setPageType(eventhub);
    quickLinkModule.setId(id);
    quickLinkModule.setSportId(sportId);
    return quickLinkModule;
  }

  private QuickLinkModule createSegmentedQuickLinkModule(
      PageType eventhub, String id, int sportId, String segment) {

    AbstractModuleData eventData = new QuickLinkData();
    eventData.setId("EVENT ID");
    ((QuickLinkData) eventData).setDestination("https://sports.ladbrokes.com/1-2-free");
    ((QuickLinkData) eventData).setSvgId("0ff5c599-a8cd-3497-8991-77e82bdaebde");

    List<AbstractModuleData> data = new ArrayList<>();
    data.add(eventData);

    QuickLinkModule quickLinkModule = new QuickLinkModule();
    quickLinkModule.setPageType(eventhub);
    quickLinkModule.setId(id);
    quickLinkModule.setSportId(sportId);
    quickLinkModule.setSegmented(true);
    quickLinkModule.setSegmentOrder(0.1);
    quickLinkModule.setDisplayOrder(new BigDecimal(2));
    quickLinkModule.setSegments(new ArrayList<>(Arrays.asList("universal")));
    quickLinkModule.setSegmented(true);

    SegmentOrderdModuleData segmentOrderdModule =
        SegmentOrderdModuleData.builder()
            .build()
            .builder()
            .segmentOrder(1.0)
            .quickLinkData((QuickLinkData) eventData)
            .build();

    quickLinkModule.setModuleSegmentView(
        new HashMap<String, SegmentView>() {
          {
            put(
                segment,
                SegmentView.builder()
                    .quickLinkData(
                        new HashMap<String, SegmentOrderdModuleData>() {
                          {
                            put(segment, segmentOrderdModule);
                          }
                        })
                    .build());
          }
        });

    return quickLinkModule;
  }

  private SurfaceBetModule createSegmentedSurfaceBetModule(
      PageType eventhub, String id, int sportId, String segment) {

    SurfaceBetModuleData eventData = new SurfaceBetModuleData();
    eventData.setId("EVENT ID");
    eventData.setTitle("surfaceBetModuleData");
    eventData.setSvgId("0ff5c599-a8cd-3497-8991-77e82bdaebde");

    SurfaceBetModule thisModule = new SurfaceBetModule();
    thisModule.setId("TEST ID");
    thisModule.setId(id);
    thisModule.setTitle("surfacebet");
    thisModule.setPageType(eventhub);
    thisModule.setSportId(sportId);
    thisModule.setSegmentOrder(0.1);
    thisModule.setDisplayOrder(new BigDecimal(1));
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
                segment,
                SegmentView.builder()
                    .surfaceBetModuleData(
                        new HashMap<String, SegmentOrderdModuleData>() {
                          {
                            put(segment, segmentOrderdModule);
                          }
                        })
                    .build());
          }
        });

    return thisModule;
  }

  private HighlightCarouselModule createSegmentedHighlightCarouselModule(
      PageType eventhub, String id, int sportId) {

    EventsModuleData eventData = new EventsModuleData();
    eventData.setId("EVENT ID");

    List<EventsModuleData> data = new ArrayList<>();
    data.add(eventData);

    HighlightCarouselModule thisModule = new HighlightCarouselModule();
    thisModule.setId("TEST ID");
    thisModule.setId(id);
    thisModule.setTitle("HighlightCarousel");
    thisModule.setSportId(sportId);
    thisModule.setPageType(eventhub);
    thisModule.setSegmentOrder(0.1);
    thisModule.setDisplayOrder(new BigDecimal(3));
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

  private SurfaceBetModule createFanzoneSegmentedSurfaceBetModule(
      PageType eventhub, String id, int sportId, String segment) {

    SurfaceBetModuleData eventData = new SurfaceBetModuleData();
    eventData.setId("EVENT ID");
    eventData.setTitle("surfaceBetModuleData");
    eventData.setSvgId("0ff5c599-a8cd-3497-8991-77e82bdaebde");

    SurfaceBetModule thisModule = new SurfaceBetModule();
    thisModule.setId("TEST ID");
    thisModule.setId(id);
    thisModule.setTitle("surfacebet");
    thisModule.setPageType(eventhub);
    thisModule.setSportId(sportId);
    thisModule.setSegmentOrder(0.1);
    thisModule.setDisplayOrder(new BigDecimal(1));
    thisModule.setSegments(new ArrayList<>(Arrays.asList("universal")));
    thisModule.setSegmented(true);

    thisModule.setFanzoneModuleSegmentView(
        new HashMap<String, FanzoneSegmentView>() {
          {
            put(
                segment,
                FanzoneSegmentView.builder()
                    .surfaceBetModuleData(
                        new HashMap<String, SurfaceBetModuleData>() {
                          {
                            put(segment, eventData);
                          }
                        })
                    .build());
          }
        });

    return thisModule;
  }

  private QuickLinkModule createFanzoneSegmentedQuickLinkModule(
      PageType eventhub, String id, int sportId, String segment) {

    QuickLinkData eventData = new QuickLinkData();
    eventData.setId("EVENT ID");
    eventData.setTitle("quick");
    eventData.setSvgId("0ff5c599-a8cd-3497-8991-77e82bdaebde");
    eventData.setFanzoneSegments(new ArrayList<>(Arrays.asList("segment")));

    QuickLinkModule thisModule = new QuickLinkModule();
    thisModule.setId("TEST ID");
    thisModule.setId(id);
    thisModule.setTitle("quicklink");
    thisModule.setPageType(eventhub);
    thisModule.setSportId(sportId);
    thisModule.setSegmentOrder(0.1);
    thisModule.setDisplayOrder(new BigDecimal(1));
    thisModule.setFanzoneSegments(new ArrayList<>(Arrays.asList("segment")));
    thisModule.setSegmented(true);

    thisModule.setFanzoneModuleSegmentView(
        new HashMap<String, FanzoneSegmentView>() {
          {
            put(
                segment,
                FanzoneSegmentView.builder()
                    .quickLinkModuleData(
                        new HashMap<String, QuickLinkData>() {
                          {
                            put(segment, eventData);
                          }
                        })
                    .build());
          }
        });

    return thisModule;
  }

  private HighlightCarouselModule createFanzoneSegmentedHighlightCarouselModule(
      PageType eventhub, String id, int sportId) {

    EventsModuleData eventData = new EventsModuleData();
    eventData.setId("EVENT ID");

    List<EventsModuleData> data = new ArrayList<>();
    data.add(eventData);

    HighlightCarouselModule thisModule = new HighlightCarouselModule();
    thisModule.setId("TEST ID");
    thisModule.setId(id);
    thisModule.setTitle("HighlightCarousel");
    thisModule.setSportId(sportId);
    thisModule.setPageType(eventhub);
    thisModule.setSegmentOrder(0.1);
    thisModule.setDisplayOrder(new BigDecimal(3));
    thisModule.setSegments(new ArrayList<>(Arrays.asList("universal")));
    thisModule.setSegmented(true);
    thisModule.setData(data);

    SegmentOrderdModule segmentOrderdModule =
        SegmentOrderdModule.builder().highlightCarouselModule(thisModule).build();

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

  private EventsModule createEventsModule(PageType eventhub, String id, int sportId) {
    EventsModule eventsModule = new EventsModule();
    eventsModule.setPageType(eventhub);
    eventsModule.setId(id);
    eventsModule.setSportId(sportId);
    EventsModuleData data = new EventsModuleData();
    data.setId("event123");
    eventsModule.setData(Arrays.asList(data));
    return eventsModule;
  }

  private InplayModule createSegmentedInplayModule(
      PageType eventhub, String id, int sportId, String segment) {

    SportSegment eventData = new SportSegment();
    eventData.setId("ID");
    eventData.setSvgId("0ff5c599-a8cd-3497-8991-77e82bdaebde");

    InplayModule thisModule = new InplayModule();
    thisModule.setId("TEST ID");
    thisModule.setId(id);
    thisModule.setTitle("InplayModule");
    thisModule.setPageType(eventhub);
    thisModule.setSportId(sportId);
    thisModule.setSegmentOrder(0.1);
    thisModule.setDisplayOrder(new BigDecimal(1));
    thisModule.setSegments(new ArrayList<>(Arrays.asList(segment)));
    thisModule.setSegmented(true);

    SegmentOrderdModuleData segmentOrderdModule =
        SegmentOrderdModuleData.builder()
            .build()
            .builder()
            .segmentOrder(1.0)
            .inplayData(eventData)
            .build();
    List<SegmentedEvents> limitedEvents = new ArrayList<>();
    SegmentedEvents segmentedEvents = new SegmentedEvents();
    TypeSegment eventByTypeName = new TypeSegment();
    EventsModuleData eventsModuleData = new EventsModuleData();
    List<EventsModuleData> events = new ArrayList<>();
    events.add(eventsModuleData);
    segmentedEvents.setEventByTypeName(eventByTypeName);
    segmentedEvents.setEvents(events);
    limitedEvents.add(segmentedEvents);
    segmentOrderdModule.setLimitedEvents(limitedEvents);
    thisModule.setModuleSegmentView(
        new HashMap<String, SegmentView>() {
          {
            put(
                segment,
                SegmentView.builder()
                    .inplayModuleData(
                        new HashMap<String, SegmentOrderdModuleData>() {
                          {
                            put(segment, segmentOrderdModule);
                          }
                        })
                    .build());
          }
        });

    return thisModule;
  }

  InplayModule createInplayModule(String id) {
    InplayModule module = new InplayModule();
    module.setType("InplayModule");
    module.setId(id);
    module.setDisplayOrder(new BigDecimal(1));
    SportSegment sportSegment = new SportSegment();
    List<SportSegment> data = new ArrayList();
    data.add(sportSegment);
    module.setData(data);
    return module;
  }

  private EventsModuleData highlightCarouselData() {
    EventsModuleData eventsModuleData = new EventsModuleData();
    eventsModuleData.setId("FZ001");
    return eventsModuleData;
  }
}
