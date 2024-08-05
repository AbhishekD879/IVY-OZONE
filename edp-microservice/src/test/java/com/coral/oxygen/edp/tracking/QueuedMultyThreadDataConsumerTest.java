package com.coral.oxygen.edp.tracking;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anySet;
import static org.mockito.ArgumentMatchers.anyString;

import java.util.Collections;
import java.util.HashSet;
import java.util.Map;
import java.util.Set;
import java.util.function.Function;
import java.util.stream.Collectors;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.invocation.InvocationOnMock;
import org.mockito.junit.MockitoJUnitRunner;
import org.mockito.stubbing.Answer;

/** Created by azayats on 28.12.17. */
@RunWith(MockitoJUnitRunner.class)
public class QueuedMultyThreadDataConsumerTest {

  private static final int QUEUE_SIZE = 5;
  private static final int THREADS_COUNT = 3;

  private static class TestedConsumer extends QueuedMultiThreadDataConsumer<Integer, String> {

    private Function<Set<Integer>, Map<Integer, String>> function;

    public TestedConsumer(
        int maxQueueSize, int threadsCount, Function<Set<Integer>, Map<Integer, String>> function) {
      super(maxQueueSize, threadsCount);
      this.function = function;
    }

    @Override
    protected Map<Integer, String> doConsume(Set<Integer> tickets) {
      return function.apply(tickets);
    }
  }

  @Mock private Function<Set<Integer>, Map<Integer, String>> consumeMock;

  @Mock private ConsumingListener<Integer, String> consumingListener;

  private QueuedMultiThreadDataConsumer<Integer, String> consumer;

  @Before
  public void setUp() {
    Mockito.when(consumeMock.apply(anySet()))
        .thenAnswer(
            new Answer<Map<Integer, String>>() {
              @Override
              public Map<Integer, String> answer(InvocationOnMock invocation) throws Throwable {
                Set<Integer> request = (Set) invocation.getArguments()[0];
                // delay to emulate long time consuming
                Thread.sleep(1000);
                return request.stream().collect(Collectors.toMap(key -> key, String::valueOf));
              }
            });
    consumer = new TestedConsumer(QUEUE_SIZE, THREADS_COUNT, consumeMock);
    consumer.setListener(consumingListener);
  }

  @Test
  public void testConsumeSingleValue() {
    consumer.consume(Collections.singleton(1));
    Mockito.verify(consumingListener, Mockito.timeout(2000))
        .onResponse(Collections.singletonMap(1, "1"));
  }

  /** When some ticket is under consuming other the same ticked should not cause consuming. */
  @Test
  public void testConsumeTwoTheSameTaskOnce() throws InterruptedException {
    // send ticket 1 to consuming
    consumer.consume(Collections.singleton(1));
    // wait a bit for starting consuming
    Thread.sleep(300);
    // send the same ticket. Previous ticket is under consuming now
    consumer.consume(Collections.singleton(1));
    // validate that result was sent to listener once
    Mockito.verify(consumingListener, Mockito.timeout(2000).times(1))
        .onResponse(Collections.singletonMap(1, "1"));
    // validate that request was sent once
    Mockito.verify(consumeMock, Mockito.times(1)).apply(Collections.singleton(1));
  }

  /** When few tickets are presented in queue we should merge them and receive in one request */
  @Test
  public void testMergingTasks() throws InterruptedException {
    // we need to make all threads busy
    for (int i = 0; i < THREADS_COUNT; i++) {
      consumer.consume(Collections.singleton(i + 100));
      // wait until each thread consume ticket
      Thread.sleep(100);
    }

    Set<Integer> s = new HashSet<>();
    s.add(1);
    s.add(2);
    // add more new tasks to queue
    s.forEach(ticket -> consumer.consume(Collections.singleton(ticket)));

    // verify that tickets was merged
    Mockito.verify(consumeMock, Mockito.timeout(2000)).apply(s);
  }

  /** Test error when queue is full */
  @Test
  public void testQueueLimit() throws InterruptedException {
    // we need to make all threads busy
    for (int i = 0; i < THREADS_COUNT; i++) {
      consumer.consume(Collections.singleton(i + 100));
      // wait until each thread consume ticket
      Thread.sleep(100);
    }

    // send more tickets
    for (int i = 0; i < QUEUE_SIZE + 1; i++) {
      consumer.consume(Collections.singleton(i + 1));
    }

    Mockito.verify(consumingListener).onError(anyString(), any());
  }

  /** Test error during consuming */
  @Test
  public void testErrorDuringConsuming() {
    Mockito.reset(consumeMock);
    Exception expectedException = new RuntimeException();
    Mockito.when(consumeMock.apply(anySet())).thenThrow(expectedException);

    consumer.consume(Collections.singleton(1));

    Mockito.verify(consumingListener, Mockito.timeout(1000)).onError(anyString(), any());
  }
}
