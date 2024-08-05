package com.egalacoral.spark.liveserver.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.Mockito.times;

import com.egalacoral.spark.liveserver.Subscriber;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

public class LiveServerSubscriberTest {
  private Subscriber subscriber;
  private LiveServerSubscriber liveServerSubscriber;

  @Before
  public void setUp() {
    this.subscriber = Mockito.mock(Subscriber.class);
    this.liveServerSubscriber = new LiveServerSubscriber(subscriber);
  }

  @Test
  public void testSubscriber() {
    LiveServerSubscriber.EventSubscribeInfo subInfo =
        LiveServerSubscriber.EventSubscribeInfo.builder()
            .categoryId(1)
            .id("123")
            .market("345")
            .outcome("567")
            .outcome("789")
            .build();

    liveServerSubscriber.subscribe(subInfo);

    Mockito.verify(subscriber).subscribeOnEvent("123", 1);
    Mockito.verify(subscriber).subscribeOnScore("123");
    Mockito.verify(subscriber).subscribeOnClock("123");
    Mockito.verify(subscriber).subscribeOnMarket("345", "123");
    Mockito.verify(subscriber).subscribeOnSelection("567", "123");
    Mockito.verify(subscriber).subscribeOnSelection("789", "123");
  }

  @Test
  public void subscribeWithoutMarketsAndEventsWorks() {
    LiveServerSubscriber.EventSubscribeInfo subInfo =
        LiveServerSubscriber.EventSubscribeInfo.builder().categoryId(1).id("123").build();

    liveServerSubscriber.subscribe(subInfo);

    Mockito.verify(subscriber).subscribeOnEvent("123", 1);
    Mockito.verify(subscriber).subscribeOnScore("123");
    Mockito.verify(subscriber).subscribeOnClock("123");
    Mockito.verify(subscriber, times(0)).subscribeOnMarket(any(), any());
    Mockito.verify(subscriber, times(0)).subscribeOnSelection(any(), any());
    Mockito.verify(subscriber, times(0)).subscribeOnSelection(any(), any());
  }

  @Test
  public void subscribeWithNoDataDoesNotThrowException() {
    LiveServerSubscriber.EventSubscribeInfo subInfo =
        LiveServerSubscriber.EventSubscribeInfo.builder().build();

    liveServerSubscriber.subscribe(subInfo);

    Mockito.verify(subscriber, times(0)).subscribeOnEvent(any(), anyInt());
    Mockito.verify(subscriber, times(0)).subscribeOnScore(any());
    Mockito.verify(subscriber, times(0)).subscribeOnClock(any());
    Mockito.verify(subscriber, times(0)).subscribeOnMarket(any(), any());
    Mockito.verify(subscriber, times(0)).subscribeOnSelection(any(), any());
    Mockito.verify(subscriber, times(0)).subscribeOnSelection(any(), any());
  }

  @Test
  public void subscribeWithNullInputDoesNotThrowException() {
    liveServerSubscriber.subscribe(null);

    Mockito.verify(subscriber, times(0)).subscribeOnEvent(any(), anyInt());
    Mockito.verify(subscriber, times(0)).subscribeOnScore(any());
    Mockito.verify(subscriber, times(0)).subscribeOnClock(any());
    Mockito.verify(subscriber, times(0)).subscribeOnMarket(any(), any());
    Mockito.verify(subscriber, times(0)).subscribeOnSelection(any(), any());
    Mockito.verify(subscriber, times(0)).subscribeOnSelection(any(), any());
  }
}
