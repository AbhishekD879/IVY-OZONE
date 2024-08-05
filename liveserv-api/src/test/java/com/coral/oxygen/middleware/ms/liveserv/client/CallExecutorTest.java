package com.coral.oxygen.middleware.ms.liveserv.client;

import static com.coral.oxygen.middleware.ms.liveserv.utils.SubscriptionUtils.newSubscription;
import static com.coral.oxygen.middleware.ms.liveserv.utils.SubscriptionUtils.updatedSubscription;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.after;
import static org.mockito.Mockito.timeout;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.liveserv.model.SubscriptionStats;
import java.io.InterruptedIOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collection;
import java.util.Collections;
import java.util.List;
import java.util.function.Supplier;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CallExecutorTest {

  @Mock private Call call;

  @Mock private Supplier<Collection<SubscriptionStats>> subscriptionsSupplier;

  @Mock private LiveServerListener listener;

  private CallExecutor callExecutor;

  @Before
  public void setUp() {
    callExecutor = new CallExecutor(call, subscriptionsSupplier, listener);
    callExecutor.setWaitSubscriptionInterval(10);
  }

  @After
  public void setDown() throws Exception {
    callExecutor.shutdown();
  }

  @Test
  public void testSingleSubscription() throws Exception {
    // given
    when(subscriptionsSupplier.get())
        .thenReturn(Collections.singletonList(newSubscription("test")))
        .thenReturn(Collections.emptyList());

    // when
    callExecutor.execute();

    // then
    verify(call, timeout(500)).execute(anyString());
  }

  @Test
  public void testMultipleSubscriptions() throws Exception {
    // given
    List<SubscriptionStats> list = new ArrayList<>();
    Collections.addAll(list, newSubscription("test1"), newSubscription("test2"));
    when(subscriptionsSupplier.get()).thenReturn(list).thenReturn(Collections.emptyList());

    // when
    callExecutor.execute();

    // then
    verify(call, timeout(500)).execute(anyString());
  }

  @Test
  public void testAddingUpdateSubscriptions() throws Exception {
    // given
    List<SubscriptionStats> list = new ArrayList<>();
    Collections.addAll(
        list,
        updatedSubscription("sEVENT0000000001", "15"),
        updatedSubscription("sEVENT0000000002", "20"));

    when(subscriptionsSupplier.get())
        .thenReturn(Collections.singletonList(newSubscription("test")))
        .thenReturn(list)
        .thenReturn(Collections.emptyList());

    // when
    callExecutor.execute();

    // then
    verify(call, timeout(500).times(2)).execute(anyString());
  }

  @Test
  public void testStoppingExecutor() throws Exception {
    // given
    callExecutor.setWaitSubscriptionInterval(500);
    when(subscriptionsSupplier.get())
        .thenReturn(Collections.emptyList())
        .thenReturn(Collections.singletonList(newSubscription("test")));
    callExecutor.execute();

    // when
    callExecutor.shutdown();

    // then
    verify(call, after(1000).never()).execute(anyString());
  }

  @Test
  public void testInterruptedException() throws Exception {
    // given
    when(call.execute(anyString())).thenThrow(new InterruptedException());
    when(subscriptionsSupplier.get())
        .thenReturn(Collections.singletonList(newSubscription("test")));
    // when
    callExecutor.execute();
    // then
    verify(listener, after(100).never()).onMessages(any());
  }

  @Test
  public void testNestedInterruptedException() throws Exception {
    // given
    when(call.execute(anyString())).thenThrow(new RuntimeException(new InterruptedException()));
    when(subscriptionsSupplier.get())
        .thenReturn(Collections.singletonList(newSubscription("test")));
    // when
    callExecutor.execute();
    // then
    verify(listener, after(100).never()).onMessages(any());
  }

  @Test
  public void testInterruptedIOException() throws Exception {
    // given
    when(call.execute(anyString())).thenThrow(new InterruptedIOException());
    when(subscriptionsSupplier.get())
        .thenReturn(Collections.singletonList(newSubscription("test")));
    callExecutor.execute();
    // then
    verify(listener, after(100).never()).onMessages(any());
    callExecutor.shutdown();
  }

  /**
   * Sleep time is increased every time error is thrown: sleepAfterErrorTime * errorCount Total
   * sleep time we can calculate using formula: Sum = 10(10+1)/2 * 10 = 550 ms Fora safety we are
   * giving 1000.
   *
   * @throws Exception
   */
  @Test
  public void testNonInterruptedException() throws Exception {
    // given
    List<SubscriptionStats> subscriptions = Collections.singletonList(newSubscription("test"));
    RuntimeException exception = new RuntimeException("Some unexpected exception");
    callExecutor.setSleepAfterErrorTime(10);

    when(subscriptionsSupplier.get()).thenReturn(subscriptions);
    Throwable[] errors = new Throwable[11];
    Arrays.fill(errors, exception);
    when(call.execute(anyString())).thenThrow(errors).thenReturn("Response");

    // when
    callExecutor.execute();

    // then
    verify(listener, timeout(1000).times(11)).onError(subscriptions, exception);
  }
}
