package com.coral.oxygen.middleware.ms.liveserv.impl;

import static java.util.Collections.emptyMap;
import static org.junit.Assert.assertEquals;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyLong;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.ArgumentMatchers.isNull;
import static org.mockito.Mockito.doNothing;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.reset;
import static org.mockito.Mockito.spy;
import static org.mockito.Mockito.times;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.verifyNoInteractions;
import static org.mockito.Mockito.verifyNoMoreInteractions;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.liveserv.LiveServeServiceFactory;
import com.coral.oxygen.middleware.ms.liveserv.MessageHandler;
import com.coral.oxygen.middleware.ms.liveserv.client.Call;
import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;
import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import java.util.Collections;
import java.util.function.Consumer;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;

public class ChunkedLiveServServiceImplTest {

  private ChunkedLiveServServiceImpl chunkliveServService;
  private ManagedLiveServeService liveServeService;
  private LiveServeServiceFactory factory;
  private Call call;
  private MessageHandler messageHandler;
  private EventIdResolver eventIdResolver;

  @Before
  public void setUp() {
    factory = spy(new LiveServeServiceFactory());
    call = mock(Call.class);
    messageHandler = mock(MessageHandler.class);
    eventIdResolver = mock(EventIdResolver.class);

    liveServeService = spy(createRealLiveServer());
    doReturn(liveServeService)
        .when(factory)
        .createCachingLiveServeService(
            eq(call), eq(messageHandler), eq(eventIdResolver), anyLong(), anyLong());
    chunkliveServService = new ChunkedLiveServServiceImpl(this::createRealLiveServer, 2L);
    reset(liveServeService, factory);
  }

  @After
  public void tearDown() throws Exception {
    liveServeService.stopConsuming();
  }

  ManagedLiveServeService createRealLiveServer() {
    return (ManagedLiveServeService)
        factory.createCachingLiveServeService(call, messageHandler, eventIdResolver, 2L, 30L);
  }

  @Test
  public void startConsuming() {
    doNothing().when(liveServeService).startConsuming();

    chunkliveServService.startConsuming();
    verify(liveServeService).startConsuming();
  }

  @Test
  public void stopConsuming() throws InterruptedException {
    chunkliveServService.stopConsuming();

    verify(liveServeService).stopConsuming();
  }

  @Test
  public void subscribe() throws ServiceException {
    String channel = "someevent1234567";
    when(eventIdResolver.resolveEventId(eq(channel))).thenReturn(123L);
    chunkliveServService.subscribe(channel);

    verifyNoMoreInteractions(factory);
    verify(liveServeService).subscribe(eq(channel), isNull(), any(Consumer.class));
    assertEquals(1, liveServeService.subscriptionsSize());
  }

  @Test
  public void subscribeMultipleAddNewChunk() throws ServiceException {
    String channel = "someevent123456";
    ManagedLiveServeService secondChunk = mock(ManagedLiveServeService.class);
    when(eventIdResolver.resolveEventId(anyString())).thenReturn(123L);
    when(factory.createCachingLiveServeService(any(), any(), any(), anyLong(), anyLong()))
        .thenReturn(secondChunk);

    chunkliveServService.subscribe(channel + "1");
    chunkliveServService.subscribe(channel + "2");
    chunkliveServService.subscribe(channel + "2");
    chunkliveServService.subscribe(channel + "3");
    chunkliveServService.subscribe(channel + "1");

    verify(liveServeService, times(2)).subscribe(eq(channel + "1"), isNull(), any(Consumer.class));
    verify(liveServeService, times(2)).subscribe(eq(channel + "2"), isNull(), any(Consumer.class));
    verify(factory, times(1))
        .createCachingLiveServeService(any(), any(), any(), anyLong(), anyLong());
    verify(secondChunk, times(1)).subscribe(eq(channel + "3"), isNull(), any(Consumer.class));

    assertEquals(2, liveServeService.subscriptionsSize());
  }

  @Test
  public void testSubscribeWithEventId() throws ServiceException, InterruptedException {
    String channel = "someevent1234567";
    chunkliveServService.subscribe(channel, 123L);

    verifyNoMoreInteractions(factory);
    verify(liveServeService).subscribe(eq(channel), eq(123L), any(Consumer.class));
    assertEquals(1, liveServeService.subscriptionsSize());
    verifyNoInteractions(eventIdResolver);

    liveServeService.stopConsuming();
  }

  @Test
  public void unsubscribeNoSubscription() throws ServiceException {
    String channel = "someevent1234560";
    when(eventIdResolver.resolveEventId(eq(channel))).thenReturn(123L);

    chunkliveServService.unsubscribe(channel);
    verify(liveServeService, times(0)).unsubscribe(anyString());
  }

  @Test
  public void unsubscribeAfterSubscription() throws ServiceException {
    String channel = "someevent1234567";
    when(eventIdResolver.resolveEventId(eq(channel))).thenReturn(123L);
    chunkliveServService.subscribe(channel);
    chunkliveServService.unsubscribe(channel);
    chunkliveServService.unsubscribe(channel);
    verify(liveServeService).unsubscribe(channel);
  }

  @Test
  public void unsubscribeCompactChunks() throws ServiceException, InterruptedException {
    String channel = "someevent123456";
    when(eventIdResolver.resolveEventId(eq(channel))).thenReturn(123L);
    ManagedLiveServeService secondChunk = mock(ManagedLiveServeService.class);
    when(factory.createCachingLiveServeService(any(), any(), any(), anyLong(), anyLong()))
        .thenReturn(secondChunk);
    when(secondChunk.subscriptionsSize()).thenReturn(2);

    chunkliveServService.subscribe(channel + "1");
    chunkliveServService.subscribe(channel + "2");
    chunkliveServService.subscribe(channel + "3");
    chunkliveServService.subscribe(channel + "4");

    verify(liveServeService, times(2)).subscribe(anyString(), isNull(), any(Consumer.class));
    verify(factory, times(2))
        .createCachingLiveServeService(any(), any(), any(), anyLong(), anyLong());

    chunkliveServService.unsubscribe(channel + "1");
    chunkliveServService.unsubscribe(channel + "2");
    chunkliveServService.unsubscribe(channel + "3");
    chunkliveServService.unsubscribe(channel + "4");
    when(secondChunk.subscriptionsSize()).thenReturn(0);
    when(secondChunk.getSubscriptions()).thenReturn(emptyMap());

    verify(liveServeService, times(2)).unsubscribe(anyString());
    verify(secondChunk, times(2)).unsubscribe(anyString());
    verify(secondChunk, times(2)).stopConsuming();
  }

  @Test
  public void unsubscribeCompactChunksMoveSubscriptions()
      throws ServiceException, InterruptedException {
    String channel = "someevent123456";
    when(eventIdResolver.resolveEventId(eq(channel))).thenReturn(123L);
    ManagedLiveServeService secondChunk = mock(ManagedLiveServeService.class);
    when(factory.createCachingLiveServeService(any(), any(), any(), anyLong(), anyLong()))
        .thenReturn(secondChunk);
    when(secondChunk.subscriptionsSize()).thenReturn(2);

    chunkliveServService.subscribe(channel + "1");
    chunkliveServService.subscribe(channel + "2");
    chunkliveServService.subscribe(channel + "3");
    chunkliveServService.subscribe(channel + "4");

    verify(liveServeService, times(2)).subscribe(anyString(), isNull(), any(Consumer.class));
    verify(factory, times(2))
        .createCachingLiveServeService(any(), any(), any(), anyLong(), anyLong());

    chunkliveServService.unsubscribe(channel + "1");
    chunkliveServService.unsubscribe(channel + "2");

    when(secondChunk.subscriptionsSize()).thenReturn(1);
    when(secondChunk.getSubscriptions())
        .thenReturn(
            Collections.singletonMap(channel + "4", new SubscriptionStats(channel + "4", 123)));

    chunkliveServService.unsubscribe(channel + "3");

    verify(liveServeService, times(2)).unsubscribe(anyString());
    verify(liveServeService, times(1))
        .addSubscription(eq(channel + "4"), any(SubscriptionStats.class));
    verify(secondChunk, times(1)).unsubscribe(anyString());
    verify(secondChunk, times(2)).stopConsuming();
  }
}
