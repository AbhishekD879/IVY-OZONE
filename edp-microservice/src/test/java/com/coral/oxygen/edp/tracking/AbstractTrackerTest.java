package com.coral.oxygen.edp.tracking;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;

import java.util.Collections;
import java.util.HashSet;
import java.util.Set;
import java.util.function.Consumer;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;

/** Created by azayats on 29.12.17. */
@RunWith(MockitoJUnitRunner.class)
public class AbstractTrackerTest {

  public static final String CLIENT_ID = "client";

  private static class TestedTracker extends AbstractTracker<Integer, String> {

    public TestedTracker(
        DataStorage<Integer, String> storage,
        DataConsumer<Integer, String> consumer,
        ChangeDetector<String> changeDetector) {
      super(storage, consumer, changeDetector);
    }
  }

  private AbstractTracker<Integer, String> tracker;

  @Mock private DataStorage<Integer, String> storage;

  @Mock private DataConsumer<Integer, String> consumer;

  @Mock private ChangeDetector<String> changeDetector;

  @Mock private Consumer<String> emitMock;

  private ConsumingListener<Integer, String> consumingListener;

  @Before
  public void setUp() {
    Mockito.when(changeDetector.dataIsChanged(anyString(), any())).thenReturn(true);
    Mockito.doAnswer(
            invocation -> {
              consumingListener = (ConsumingListener) invocation.getArguments()[0];
              return null;
            })
        .when(consumer)
        .setListener(any());
    tracker = new TestedTracker(storage, consumer, changeDetector);
  }

  private Subscription<Integer, String> createSubscription(int ticket) {
    return new Subscription<Integer, String>(CLIENT_ID, ticket, 5) {
      @Override
      public void emit(String data) {
        emitMock.accept(data);
      }
    };
  }

  @Test
  public void testSubscribeAndEmitData() {
    tracker.addSubscription(createSubscription(1));

    Mockito.verify(emitMock, Mockito.never()).accept(any());
    consumingListener.onResponse(Collections.singletonMap(1, "1"));

    Mockito.verify(emitMock).accept("1");
  }

  @Test
  public void testSubscribeAndEmitDataTwice() {
    tracker.addSubscription(createSubscription(1));

    Mockito.verify(emitMock, Mockito.never()).accept(any());
    consumingListener.onResponse(Collections.singletonMap(1, "1"));
    consumingListener.onResponse(Collections.singletonMap(1, "2"));

    Mockito.verify(emitMock).accept("1");
    Mockito.verify(emitMock).accept("2");
  }

  @Test
  public void testUnSubscribe() {
    tracker.addSubscription(createSubscription(1));
    tracker.removeSubscription(CLIENT_ID, 1);
    Mockito.verify(emitMock, Mockito.never()).accept(any());
  }

  @Test
  public void testUnSubscribeMissingSubscription() {
    tracker.addSubscription(createSubscription(1));
    tracker.removeSubscription(CLIENT_ID, 2);
  }

  @Test
  public void testSubscribeTwoClientsAndEmitData() {
    tracker.addSubscription(createSubscription(1));
    Consumer<String> emitMock2 = Mockito.mock(Consumer.class);
    final String SECOND_CLIENT_ID = "SecondClient";
    tracker.addSubscription(
        new Subscription<Integer, String>(SECOND_CLIENT_ID, 1, 5) {
          @Override
          public void emit(String data) {
            emitMock2.accept(data);
          }
        });

    Mockito.verify(emitMock, Mockito.never()).accept(any());
    consumingListener.onResponse(Collections.singletonMap(1, "1"));

    Mockito.verify(emitMock).accept("1");
    Mockito.verify(emitMock2).accept("1");
  }

  @Test
  public void testSubscribeTwoClientsAndUnsubscribeOneAndEmitData() {
    tracker.addSubscription(createSubscription(1));
    Consumer<String> emitMock2 = Mockito.mock(Consumer.class);
    final String SECOND_CLIENT_ID = "SecondClient";
    tracker.addSubscription(
        new Subscription<Integer, String>(SECOND_CLIENT_ID, 1, 5) {
          @Override
          public void emit(String data) {
            emitMock2.accept(data);
          }
        });
    tracker.removeSubscription(SECOND_CLIENT_ID, 1);

    consumingListener.onResponse(Collections.singletonMap(1, "1"));

    Mockito.verify(emitMock).accept("1");
    Mockito.verify(emitMock2, Mockito.never()).accept("1");
  }

  @Test
  public void testEmitDataFromStorage() {
    Mockito.when(storage.get(1)).thenReturn("1_stored");

    tracker.addSubscription(createSubscription(1));

    Mockito.verify(emitMock).accept("1_stored");
  }

  @Test
  public void testRefreshData() {

    tracker.addSubscription(createSubscription(1));
    tracker.addSubscription(createSubscription(2));
    tracker.refreshData();

    Set<Integer> expectedSet = new HashSet<>();
    expectedSet.add(1);
    expectedSet.add(2);
    Mockito.verify(consumer).consume(expectedSet);
  }
}
