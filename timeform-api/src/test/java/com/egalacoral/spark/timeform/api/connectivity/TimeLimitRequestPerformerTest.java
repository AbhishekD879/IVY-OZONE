package com.egalacoral.spark.timeform.api.connectivity;

import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.api.TimeFormException;
import org.junit.*;
import org.junit.rules.ExpectedException;
import org.junit.runner.RunWith;
import org.mockito.ArgumentMatcher;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.invocation.InvocationOnMock;
import org.mockito.runners.MockitoJUnitRunner;
import org.mockito.stubbing.Answer;
import retrofit2.Call;

import java.util.HashMap;
import java.util.Map;

@RunWith(MockitoJUnitRunner.class)
public class TimeLimitRequestPerformerTest {

  private static final long LIMIT_TIME_1 = 1000;
  private static final long LIMIT_TIME_2 = 1000L * 60 * 60;
  private static final int LIMIT_COUNT_1 = 1;
  private static final int LIMIT_COUNT_2 = 3000;

  @Rule
  public ExpectedException expectedException = ExpectedException.none();

  private TimeLimitRequestPerformer performer;

  @Mock
  private RequestPerformer delegate;

  @Mock
  private TimeProvider timeProvider;

  @Mock
  private Call call;

  @Mock
  private DataCallback dataCallback;

  @Before
  public void setUp() {
    Map<Long, Integer> limitations = new HashMap<>();
    limitations.put(LIMIT_TIME_1, LIMIT_COUNT_1);
    limitations.put(LIMIT_TIME_2, LIMIT_COUNT_2);
    performer = new TimeLimitRequestPerformer(delegate, timeProvider, limitations);
  }

  @Test
  public void testFollowRulesSync() {
    long delay = Math.max(LIMIT_TIME_1 / LIMIT_COUNT_1 + 1, LIMIT_TIME_2 / LIMIT_COUNT_2 + 1);
    int iterations = Math.max(LIMIT_COUNT_1, LIMIT_COUNT_2) * 2;

    for (int i = 0; i < iterations; i++) {
      Mockito.when(timeProvider.currentTime()).thenReturn(delay * i);
      performer.invokeSync(call);
    }

    Mockito.verify(delegate, Mockito.times(iterations)).invokeSync(call);
  }

  @Test
  public void testFollowRulesAsync() {
    long delay = Math.max(LIMIT_TIME_1 / LIMIT_COUNT_1 + 1, LIMIT_TIME_2 / LIMIT_COUNT_2 + 1);
    int iterations = Math.max(LIMIT_COUNT_1, LIMIT_COUNT_2) * 2;
    Mockito.when(timeProvider.currentTime()).thenAnswer(new Answer<Object>() {
      private volatile int count;
      @Override
      public synchronized Object answer(InvocationOnMock invocation) throws Throwable {
        return count++ * delay;
      }
    });

    for (int i = 0; i < iterations; i++) {
      performer.invokeAsync(call, dataCallback);
    }

    Mockito.verify(delegate, Mockito.timeout(10000).times(iterations)).invokeAsync(call, dataCallback);
  }

  @Test
  public void testWaitAsync() {
    performer.invokeAsync(call, dataCallback);
    performer.invokeAsync(call, dataCallback);
    Mockito.verify(delegate, Mockito.timeout(500).times(1)).invokeAsync(call, dataCallback);

    long delay = Math.min(LIMIT_TIME_1, LIMIT_TIME_2);

    Mockito.verify(delegate, Mockito.timeout((int) (delay + 500)).times(2)).invokeAsync(call, dataCallback);
  }

  @Test
  public void testWaitSync() {
    performer.invokeSync(call);
    Mockito.verify(delegate, Mockito.times(1)).invokeSync(call);
    long startTime = System.currentTimeMillis();
    performer.invokeSync(call);
    long current = System.currentTimeMillis();
    long delay = Math.min(LIMIT_TIME_1, LIMIT_TIME_2);

    Mockito.verify(delegate, Mockito.times(2)).invokeSync(call);
    Assert.assertTrue(current - startTime >= delay);
  }

  @Test
  public void testDelegateFailsSync() {
    RuntimeException rte = new RuntimeException();
    Mockito.doThrow(rte).when(delegate).invokeSync(call);

    expectedException.expect(TimeFormException.class);
    performer.invokeSync(call);
  }

  @Test
  public void testDelegateFailsWithTimeFormExceptionSync() {
    TimeFormException tfe = new TimeFormException();
    Mockito.doThrow(tfe).when(delegate).invokeSync(call);

    expectedException.expect(new ArgumentMatcher<Object>() {
      @Override
      public boolean matches(Object argument) {
        return tfe.equals(argument);
      }
    });
    performer.invokeSync(call);
  }

  @Test
  public void testDelegateFailsAsync() {
    RuntimeException rte = new RuntimeException();
    Mockito.doThrow(rte).when(delegate).invokeAsync(call, dataCallback);

    performer.invokeAsync(call, dataCallback);

    Mockito.verify(dataCallback, Mockito.timeout(1000)).onError(Mockito.any(TimeFormException.class));
  }

  @Test
  public void testDelegateFailsWithTimeFormExceptionAsync() {
    TimeFormException tfe = new TimeFormException();
    Mockito.doThrow(tfe).when(delegate).invokeAsync(call, dataCallback);

    performer.invokeAsync(call, dataCallback);

    Mockito.verify(dataCallback, Mockito.timeout(1000)).onError(tfe);
  }

}
