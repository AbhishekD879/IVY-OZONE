package com.oxygen.publisher.sportsfeatured.context;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import com.corundumstudio.socketio.HandshakeData;
import com.corundumstudio.socketio.SocketIOClient;
import com.corundumstudio.socketio.SocketIOServer;
import com.oxygen.publisher.SocketIoTestHelper;
import com.oxygen.publisher.model.ApplicationVersion;
import com.oxygen.publisher.model.PageType;
import com.oxygen.publisher.sportsfeatured.model.FeaturedModel;
import com.oxygen.publisher.sportsfeatured.model.ModuleRawIndex;
import com.oxygen.publisher.sportsfeatured.model.PageRawIndex;
import com.oxygen.publisher.sportsfeatured.model.SportsCachedData;
import com.oxygen.publisher.sportsfeatured.model.module.*;
import com.oxygen.publisher.sportsfeatured.model.module.data.SurfaceBetModuleData;
import com.oxygen.publisher.sportsfeatured.util.SportsHelper;
import java.lang.reflect.*;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.Map;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.*;
import org.mockito.junit.MockitoJUnitRunner;

@SuppressWarnings("java:S5976")
@RunWith(MockitoJUnitRunner.class)
public class SportsSessionContextTest {

  @Mock private ApplicationVersion appVersion;

  @Mock(answer = Answers.RETURNS_DEEP_STUBS)
  private SportsMiddlewareContext sportsMiddlewareContext;

  @InjectMocks SportsSessionContext sportsSessionContext;

  @Mock SportsCachedData sportsCachedData;

  private SocketIOClient client;
  private SocketIOServer socketIOServer;
  private HandshakeData handshakeData;

  @Before
  public void init() {
    Mockito.when(sportsMiddlewareContext.getFeaturedCachedData()).thenReturn(sportsCachedData);
    socketIOServer = mock(SocketIOServer.class);
    client = mock(SocketIOClient.class);
    handshakeData = mock(HandshakeData.class);
  }

  @Test
  public void onSubscribeSport() {
    AbstractFeaturedModule module = createModule(PageType.sport, "123456", 8);
    sportsCachedData.updateModule(ModuleRawIndex.fromModule(module), module);
    when(sportsCachedData.getSportPageData()).thenReturn(SocketIoTestHelper.getSportPageMapCache());
    try (MockedStatic<SportsHelper> mockedStatic = Mockito.mockStatic(SportsHelper.class)) {
      mockedStatic
          .when(() -> SportsHelper.checkValidSportId(client, sportsCachedData, "8"))
          .thenReturn(PageRawIndex.forSport(8));
    }
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketIOServer);
    when(client.getHandshakeData()).thenReturn(handshakeData);
    sportsSessionContext.onSubscribe(client, "8#123456", null);
    Mockito.verify(client, Mockito.times(1)).joinRoom(module.getSportId() + "#" + "123456");
    Mockito.verify(client, Mockito.times(0)).sendEvent(Mockito.eq("123456"), any());
  }

  @Test
  public void onSubscribeSportWithNullModuleId()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {

    Method method = getReflectMethod();
    method.setAccessible(true);
    Object[] param = {client, null, "", "", PageRawIndex.forSport(8)};
    method.invoke(sportsSessionContext, param);
    Assert.assertNotNull(param);
  }

  @Test
  public void onSubscribeSportWithModuleId()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {

    Method method = getReflectMethod();
    method.setAccessible(true);
    Object[] param = {client, "8#123456#seg1", "", "", PageRawIndex.forSport(8)};
    method.invoke(sportsSessionContext, param);
    Assert.assertNotNull(param);
  }

  @Test
  public void onSubscribeSportWithEmptyModuleId()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {

    Method method = getReflectMethod();
    method.setAccessible(true);
    Object[] param = {client, "", "", "", PageRawIndex.forSport(8)};
    method.invoke(sportsSessionContext, param);
    Assert.assertNotNull(param);
  }

  @Test
  public void onSegmentedSubscribeSport() {
    AbstractFeaturedModule module = createModule(PageType.sport, "123456", 8);
    sportsCachedData.updateModule(ModuleRawIndex.fromModule(module), module);
    when(sportsCachedData.getSportPageData()).thenReturn(SocketIoTestHelper.getSportPageMapCache());
    try (MockedStatic<SportsHelper> mockedStatic = Mockito.mockStatic(SportsHelper.class)) {
      mockedStatic
          .when(() -> SportsHelper.checkValidSportId(client, sportsCachedData, "8"))
          .thenReturn(PageRawIndex.forSport(8));
    }
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketIOServer);
    when(client.getHandshakeData()).thenReturn(handshakeData);
    sportsSessionContext.onSubscribe(client, "8#123456#seg1", null);
    Mockito.verify(client, Mockito.times(1)).joinRoom("8#123456");
    Mockito.verify(client, Mockito.times(0)).sendEvent(Mockito.eq("123456#seg1"), any());
  }

  @Test
  public void whenNoModuleIdSentFromFE() {
    AbstractFeaturedModule module = createModule(PageType.sport, "123456", 8);
    sportsCachedData.updateModule(ModuleRawIndex.fromModule(module), module);
    try (MockedStatic<SportsHelper> mockedStatic = Mockito.mockStatic(SportsHelper.class)) {
      mockedStatic
          .when(() -> SportsHelper.checkValidSportId(client, sportsCachedData, "8"))
          .thenReturn(PageRawIndex.forSport(8));
    }
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketIOServer);
    when(client.getHandshakeData()).thenReturn(handshakeData);
    sportsSessionContext.onSubscribe(client, null, null);
    Mockito.verify(client, Mockito.times(0)).joinRoom("8#123456");
    Mockito.verify(client, Mockito.times(0)).sendEvent(Mockito.eq("123456"), any());
  }

  @Test
  public void onSubscribeEventHub() {
    AbstractFeaturedModule module = createModule(PageType.eventhub, "123456", 8);
    sportsCachedData.updateModule(ModuleRawIndex.fromModule(module), module);
    when(sportsCachedData.getSportPageData()).thenReturn(SocketIoTestHelper.getSportPageMapCache());
    try (MockedStatic<SportsHelper> mockedStatic = Mockito.mockStatic(SportsHelper.class)) {
      mockedStatic
          .when(() -> SportsHelper.checkValidSportId(client, sportsCachedData, "8"))
          .thenReturn(PageRawIndex.forSport(8));
    }
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketIOServer);
    when(client.getHandshakeData()).thenReturn(handshakeData);
    sportsSessionContext.onSubscribe(client, "8#123456", null);
    Mockito.verify(client, Mockito.times(1)).joinRoom("8#123456");
    Mockito.verify(client, Mockito.times(0)).sendEvent(Mockito.eq("123456"), any());
  }

  @Test
  public void onSubscribeNoData() {
    when(sportsCachedData.getSportPageData()).thenReturn(SocketIoTestHelper.getSportPageMapCache());
    try (MockedStatic<SportsHelper> mockedStatic = Mockito.mockStatic(SportsHelper.class)) {
      mockedStatic
          .when(() -> SportsHelper.checkValidSportId(client, sportsCachedData, "8"))
          .thenReturn(PageRawIndex.forSport(8));
    }
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketIOServer);
    when(client.getHandshakeData()).thenReturn(handshakeData);
    when(handshakeData.getSingleUrlParam(any())).thenReturn("ios");
    sportsSessionContext.onSubscribe(client, "8#123456", null);
    Mockito.verify(client, Mockito.times(1)).joinRoom("8#123456");
    Mockito.verify(client, Mockito.never()).sendEvent(Mockito.eq("123456"), any());
  }

  @Test
  public void onLoginSport() {
    FeaturedModel featuredModel = createStructureWithSegmentWiseModules("0");
    new SportsCachedData(100, 159).getStructureMap().put(PageRawIndex.forSport(0), featuredModel);
    when(sportsCachedData.getSportPageData()).thenReturn(SocketIoTestHelper.getSportPageMapCache());
    try (MockedStatic<SportsHelper> mockedStatic = Mockito.mockStatic(SportsHelper.class)) {
      mockedStatic
          .when(() -> SportsHelper.checkValidSportId(client, sportsCachedData, "0"))
          .thenReturn(PageRawIndex.forSport(0));
    }
    when(sportsMiddlewareContext.socketIOServer()).thenReturn(socketIOServer);
    sportsSessionContext.onLogin(client, "0#segment");
    Mockito.verify(client, Mockito.times(0)).joinRoom("0#segment");
  }

  private QuickLinkModule createModule(PageType eventhub, String id, int sportId) {
    QuickLinkModule quickLinkModule = new QuickLinkModule();
    quickLinkModule.setPageType(eventhub);
    quickLinkModule.setId(id);
    quickLinkModule.setSportId(sportId);
    return quickLinkModule;
  }

  FeaturedModel createStructureWithSegmentWiseModules(String pageId) {
    FeaturedModel model = new FeaturedModel(pageId);
    Map<String, SegmentView> segmentWiseModules = new HashMap<>();
    SegmentView segmentView = new SegmentView();
    HighlightCarouselModule highlightCarouselModule =
        createHighlightCarouselModule("Highlight Carousel");
    model.addModule(highlightCarouselModule);
    SegmentOrderdModule segmentOrderdModuleForHc =
        new SegmentOrderdModule(1, highlightCarouselModule);
    segmentView
        .getHighlightCarouselModules()
        .put(highlightCarouselModule.getId(), segmentOrderdModuleForHc);

    segmentWiseModules.put("segment", segmentView);
    model.setSegmentWiseModules(segmentWiseModules);
    return model;
  }

  HighlightCarouselModule createHighlightCarouselModule(String id) {
    HighlightCarouselModule module = new HighlightCarouselModule();
    module.setType("HighlightCarouselModule");
    module.setId(id);
    SurfaceBetModuleData data = new SurfaceBetModuleData();
    data.setId("123");
    ArrayList list = new ArrayList();
    list.add(data);
    module.setData(list);
    return module;
  }

  private Method getReflectMethod() throws NoSuchMethodException {

    return SportsSessionContext.class.getDeclaredMethod(
        "subscribeToModule",
        SocketIOClient.class,
        String.class,
        String.class,
        String.class,
        PageRawIndex.class);
  }
}
