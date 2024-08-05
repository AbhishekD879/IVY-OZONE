package com.ladbrokescoral.oxygen.notification.services;

import com.ladbrokescoral.oxygen.notification.controllers.NativeNotifications;
import com.ladbrokescoral.oxygen.notification.entities.*;
import com.ladbrokescoral.oxygen.notification.entities.dto.ChannelDTO;
import com.ladbrokescoral.oxygen.notification.entities.dto.Platform;
import com.ladbrokescoral.oxygen.notification.entities.dto.SubscriptionDTO;
import com.ladbrokescoral.oxygen.notification.entities.sportsbook.Event;
import com.ladbrokescoral.oxygen.notification.services.repositories.ChannelRepository;
import com.ladbrokescoral.oxygen.notification.services.repositories.Subscriptions;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageImpl;
import org.springframework.data.domain.PageRequest;
import org.springframework.data.domain.Pageable;
import org.springframework.data.redis.core.StringRedisTemplate;
import org.springframework.http.ResponseEntity;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.bind.WebDataBinder;

@RunWith(MockitoJUnitRunner.Silent.class)
public class NotificationSubscriptionServiceTest {

  @Mock private NotificationSubscriptionService service;
  @InjectMocks private NativeNotifications nativeNotifications;

  @Mock private ChannelRepository channelRepository;

  @Mock private Subscriptions subscriptions;

  @Mock private StringRedisTemplate redisTemplate;
  @Mock private EventService eventService;
  @Mock private SiteServerApiService siteServerApiService;
  private static final String DEEP_LINK_MOCK =
      "horse-racing/-horse-racing-live-/la-teste-de-buch/-12-00-la-teste-de-buch-/";

  @Before
  public void setUp() {
    MockitoAnnotations.initMocks(this);
    subscriptions = Mockito.mock(Subscriptions.class);
    eventService = Mockito.mock(EventService.class);
    service =
        new NotificationSubscriptionService(
            redisTemplate,
            86400L,
            eventService,
            channelRepository,
            siteServerApiService,
            subscriptions);
    ReflectionTestUtils.setField(
        nativeNotifications, "service", service, NotificationSubscriptionService.class);
  }

  @Test
  public void subscribeAlertsTest() {
    Item request =
        (Item)
            new Item()
                .setAppVersionInt(60700)
                .setEventId(10000L)
                .setSportUri(null)
                .setTypes(new ArrayList<String>())
                .setListOfChannelId(new ArrayList<String>())
                .setToken("test")
                .setPlatform("test");

    Item responseEntity =
        service.get(
            new ItemEmpty()
                .setAppVersionInt(60700)
                .setEventId(10000L)
                .setToken("test")
                .setPlatform("test"));
    Assert.assertNotNull(responseEntity);
    Assert.assertEquals(responseEntity, request);
  }

  @Test
  public void multiSubscribeAlertsTest() {
    Items request =
        (Items)
            new Items()
                .setIsEnable(false)
                .setAppVersionInt(60700)
                .setEventId(10000L)
                .setSportUri(null)
                .setTypes(new ArrayList<String>())
                .setListOfChannelId(new ArrayList<String>())
                .setToken("test")
                .setPlatform("test");

    List<Items> responseEntity =
        service.get(
            new ItemEmptys()
                .setAppVersionInt(60700)
                .setEventId(Arrays.asList(10000L))
                .setToken("test")
                .setPlatform("test"));
    Assert.assertNotNull(responseEntity);
    Assert.assertEquals(responseEntity, Arrays.asList(request));
  }

  @Test
  public void viewEventSubscriptionTest()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {
    Mockito.when(getDoubleIntegerMethod().invoke(service, 10000L))
        .thenReturn(
            Arrays.asList(
                SubscriptionDTO.builder()
                    .eventId(10000L)
                    .platform(Platform.ANDROID)
                    .type("kick_off")
                    .ownerId("test")
                    .token("test")
                    .build()));
    ResponseEntity<?> responseEntity =
        nativeNotifications.viewEventSubscription(
            new ItemEmptys()
                .setAppVersionInt(60700)
                .setEventId(Arrays.asList(10000L))
                .setToken("test")
                .setPlatform("test"));
    List<Items> responseEntityService =
        service.get(
            new ItemEmptys()
                .setAppVersionInt(60700)
                .setEventId(Arrays.asList(10000L))
                .setToken("test")
                .setPlatform("test"));
    WebDataBinder webDataBinder = new WebDataBinder(Object.class);
    nativeNotifications.populateRequest(webDataBinder);
    List<Items> items = (List<Items>) responseEntity.getBody();
    Assert.assertNotNull(responseEntityService);
    Assert.assertNotNull(responseEntity.getBody());
    Assert.assertEquals(items.get(0).getEventId(), responseEntityService.get(0).getEventId());
  }

  @Test
  public void viewEventSubscriptionTestwithouttypes() {
    ResponseEntity<?> responseEntity =
        nativeNotifications.viewEventSubscription(
            new ItemEmptys()
                .setAppVersionInt(60700)
                .setEventId(Arrays.asList(10000L))
                .setToken("test")
                .setPlatform("test"));
    List<Items> responseEntityService =
        service.get(
            new ItemEmptys()
                .setAppVersionInt(60700)
                .setEventId(Arrays.asList(10000L))
                .setToken("test")
                .setPlatform("test"));
    WebDataBinder webDataBinder = new WebDataBinder(Object.class);
    nativeNotifications.populateRequest(webDataBinder);
    List<Items> items = (List<Items>) responseEntity.getBody();
    Assert.assertNotNull(responseEntityService);
    Assert.assertNotNull(responseEntity.getBody());
    Assert.assertEquals(items.get(0).getEventId(), responseEntityService.get(0).getEventId());
  }

  public Method getDoubleIntegerMethod() throws NoSuchMethodException {
    Method method =
        NotificationSubscriptionService.class.getDeclaredMethod(
            "subscriptionsForEvent", long.class);
    method.setAccessible(true);
    return method;
  }

  @Test
  public void saveSubscription() {
    Item request =
        (Item)
            new Item()
                .setAppVersionInt(60700)
                .setEventId(10000L)
                .setSportUri(null)
                .setTypes(Arrays.asList("cards", "goals", "periods"))
                .setListOfChannelId(new ArrayList<String>())
                .setToken("test")
                .setPlatform("test");
    ChannelDTO channelDTO = new ChannelDTO();
    channelDTO.setName("cards");
    channelRepository.save(channelDTO);
    Event event =
        Event.builder()
            .eventId(10000L)
            .name("|Grand National Event|")
            .startTime("2023-07-06T16:00:00Z")
            .categoryId("21")
            .sportUri(DEEP_LINK_MOCK)
            .homeTeamName("Uzhhorod")
            .awayTeamName("Mukacheve")
            .build();
    Mockito.when(subscriptions.save(Mockito.any())).thenReturn(initStreamSubscriptionsRes());
    Mockito.when(eventService.process(10000L)).thenReturn(event);
    Item responseEntity = service.save(request);
    Assert.assertNotNull(responseEntity);
  }

  @Test
  public void saveSubscriptionTest() {
    Item request =
        (Item)
            new Item()
                .setAppVersionInt(60700)
                .setEventId(10000L)
                .setSportUri(null)
                .setTypes(Arrays.asList("cards", "goals"))
                .setListOfChannelId(new ArrayList<String>())
                .setToken("test")
                .setPlatform("test");
    ChannelDTO channelDTO = new ChannelDTO();
    channelDTO.setName("cards");
    channelRepository.save(channelDTO);
    Event event =
        Event.builder()
            .eventId(10000L)
            .name("|Grand National Event|")
            .startTime("2023-07-06T16:00:00Z")
            .categoryId("21")
            .sportUri(DEEP_LINK_MOCK)
            .homeTeamName("Uzhhorod")
            .awayTeamName("Mukacheve")
            .build();
    Mockito.when(eventService.process(10000L)).thenReturn(event);
    Mockito.when(subscriptions.save(Mockito.any())).thenReturn(initStreamSubscriptionsRes());
    Item responseEntity = service.save(request);
    Assert.assertNotNull(responseEntity);
  }

  @Test
  public void saveSubscriptionDifferentTest() {
    Item request =
        (Item)
            new Item()
                .setAppVersionInt(60700)
                .setEventId(100L)
                .setSportUri(null)
                .setTypes(Arrays.asList("goals"))
                .setListOfChannelId(new ArrayList<String>())
                .setToken("test")
                .setPlatform("test");
    ChannelDTO channelDTO = new ChannelDTO();
    channelDTO.setName("cards");
    channelRepository.save(channelDTO);
    Event event =
        Event.builder()
            .eventId(100L)
            .name("|Grand National Event|")
            .startTime("2026-06-21T17:00:00Z")
            .categoryId("21")
            .sportUri(DEEP_LINK_MOCK)
            .homeTeamName("Uzhhorod")
            .awayTeamName("Mukacheve")
            .build();
    Mockito.when(eventService.process(100L)).thenReturn(event);
    Mockito.when(subscriptions.save(Mockito.any())).thenReturn(initSubscriptions());
    Item responseEntity = service.save(request);
    Assert.assertNotNull(responseEntity);
  }

  @Test
  public void saveSubscriptionexceptionStartTimeTest() {
    Item request =
        (Item)
            new Item()
                .setAppVersionInt(60700)
                .setEventId(100L)
                .setSportUri(null)
                .setTypes(Arrays.asList("goals", "stream_starting"))
                .setListOfChannelId(new ArrayList<String>())
                .setToken("test")
                .setPlatform("test");
    ChannelDTO channelDTO = new ChannelDTO();
    channelDTO.setName("cards");
    channelRepository.save(channelDTO);
    Event event =
        Event.builder()
            .eventId(100L)
            .name("|Grand National Event|")
            .startTime("2026-06.7:00:00Z")
            .categoryId("21")
            .sportUri(DEEP_LINK_MOCK)
            .homeTeamName("Uzhhorod")
            .awayTeamName("Mukacheve")
            .build();
    Mockito.when(eventService.process(100L)).thenReturn(event);
    Mockito.when(subscriptions.save(Mockito.any())).thenReturn(initSubscriptionsRes());
    Item responseEntity = service.save(request);
    Assert.assertNotNull(responseEntity);
  }

  @Test
  public void saveSubscriptionSameTest() {
    Item request =
        (Item)
            new Item()
                .setAppVersionInt(60700)
                .setEventId(10L)
                .setSportUri(null)
                .setTypes(Arrays.asList("periods"))
                .setListOfChannelId(new ArrayList<String>())
                .setToken("test")
                .setPlatform("test");
    ChannelDTO channelDTO = new ChannelDTO();
    channelDTO.setName("cards");
    channelRepository.save(channelDTO);
    Event event =
        Event.builder()
            .eventId(10L)
            .name("|Grand National Event|")
            .startTime("2026-06-21T17:00:00Z")
            .categoryId("21")
            .sportUri(DEEP_LINK_MOCK)
            .homeTeamName("Uzhhorod")
            .awayTeamName("Mukacheve")
            .build();
    Mockito.when(eventService.process(10L)).thenReturn(event);
    Mockito.when(subscriptions.save(Mockito.any())).thenReturn(initSubscriptionsRes());
    Item responseEntity = service.save(request);
    Assert.assertNotNull(responseEntity);
  }

  @Test
  public void getNoTTLRecordsTest() {
    Pageable pageable = PageRequest.of(1, 1);
    Mockito.when(subscriptions.findAll(pageable))
        .thenReturn((Page<SubscriptionDTO>) initSubscriptionsSame());
    Long nottelValue = service.getNoTTLRecords(1, 1);
    Assert.assertNotNull(nottelValue);
  }

  @Test
  public void getNoTTLRecordsExceptionTest() {
    Pageable pageable = PageRequest.of(1, 1);
    Mockito.when(subscriptions.findAll(pageable))
        .thenReturn((Page<SubscriptionDTO>) initSubscriptionsException());
    Long nottelValue = service.getNoTTLRecords(1, 1);
    Assert.assertNotNull(nottelValue);
  }

  @Test
  public void getNoTTLRecordsAfterDateTest() {
    Pageable pageable = PageRequest.of(1, 1);
    Mockito.when(subscriptions.findAll(pageable))
        .thenReturn((Page<SubscriptionDTO>) initSubscriptionsDate());
    Long nottelValue = service.getNoTTLRecords(1, 1);
    Assert.assertNotNull(nottelValue);
  }

  private Page<SubscriptionDTO> initSubscriptionsSame() {

    List<SubscriptionDTO> subscriptionDTOS = new ArrayList<>();
    subscriptionDTOS.add(
        SubscriptionDTO.builder()
            .eventId(10L)
            .startTime("2023-07-06T16:00:00Z")
            .platform(Platform.ANDROID)
            .type("periods")
            .appVersionInt(60700)
            .token("test")
            .build());
    Page<SubscriptionDTO> page = new PageImpl<>(subscriptionDTOS);
    return page;
  }

  private Page<SubscriptionDTO> initSubscriptionsException() {

    List<SubscriptionDTO> subscriptionDTOS = new ArrayList<>();
    subscriptionDTOS.add(
        SubscriptionDTO.builder()
            .eventId(10L)
            .startTime("2023-.:00:00Z")
            .platform(Platform.ANDROID)
            .type("periods")
            .appVersionInt(60700)
            .token("test")
            .build());
    Page<SubscriptionDTO> page = new PageImpl<>(subscriptionDTOS);
    return page;
  }

  private Page<SubscriptionDTO> initSubscriptionsDate() {

    List<SubscriptionDTO> subscriptionDTOS = new ArrayList<>();
    subscriptionDTOS.add(
        SubscriptionDTO.builder()
            .eventId(10L)
            .startTime("2022-07-06T16:00:00Z")
            .platform(Platform.ANDROID)
            .type("periods")
            .appVersionInt(60700)
            .token("test")
            .build());
    Page<SubscriptionDTO> page = new PageImpl<>(subscriptionDTOS);
    return page;
  }

  private SubscriptionDTO initStreamSubscriptionsRes() {
    return SubscriptionDTO.builder()
        .eventId(100L)
        .platform(Platform.ANDROID)
        .type("stream_starting")
        .token("test")
        .build();
  }

  private SubscriptionDTO initSubscriptionsRes() {
    return SubscriptionDTO.builder()
        .eventId(100L)
        .platform(Platform.ANDROID)
        .type("stream_starting")
        .token("test")
        .build();
  }

  private SubscriptionDTO initSubscriptions() {
    return SubscriptionDTO.builder()
        .eventId(10000L)
        .platform(Platform.ANDROID)
        .type("kick_off")
        .token("test")
        .build();
  }
}
