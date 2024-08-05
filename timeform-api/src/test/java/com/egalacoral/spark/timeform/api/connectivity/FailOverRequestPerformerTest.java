package com.egalacoral.spark.timeform.api.connectivity;

import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.ArgumentCaptor;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.invocation.InvocationOnMock;
import org.mockito.runners.MockitoJUnitRunner;
import org.mockito.stubbing.Answer;

import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.api.TimeFormException;

import retrofit2.Call;

@RunWith(MockitoJUnitRunner.class)
public class FailOverRequestPerformerTest {

  private FailOverRequestPerformer performer;

  @Mock
  private RequestPerformer delegate;

  @Mock
  private FailOverStrategy failOverStrategy;

  @Mock
  private Runnable reloginAction;

  @Mock
  private Call call;

  @Mock
  private Call callClone;

  @Mock
  private DataCallback dataCallback;

  private Object successResponseBody;

  @Before
  public void setUp() {
    performer = new FailOverRequestPerformer(delegate, failOverStrategy, reloginAction);

    Mockito.when(call.clone()).thenReturn(callClone);
    Mockito.when(callClone.clone()).thenReturn(callClone);

    successResponseBody = new Object();
    Mockito.doAnswer(invocation -> {
      ((DataCallback) invocation.getArguments()[1]).onResponse(successResponseBody);
      return null;
    }).when(delegate).invokeAsync(Mockito.any(), Mockito.any());
  }

  @Test
  public void testSuccessPassSync() {
    performer.invokeSync(call);

    Mockito.verify(delegate).invokeSync(call);
    Mockito.verify(failOverStrategy, Mockito.never()).onError(Mockito.any(), Mockito.anyInt());
    Mockito.verify(reloginAction, Mockito.never()).run();
  }

  @Test
  public void testSuccessPassAsync() {
    performer.invokeAsync(call, dataCallback);

    Mockito.verify(delegate).invokeAsync(Mockito.eq(call), Mockito.any(DataCallback.class));
    Mockito.verify(dataCallback, Mockito.timeout(1000)).onResponse(successResponseBody);
    Mockito.verify(failOverStrategy, Mockito.never()).onError(Mockito.any(), Mockito.anyInt());
    Mockito.verify(reloginAction, Mockito.never()).run();
  }

  @Test
  public void testRetrySync() {
    // preparation
    int count = 3;
    Mockito.doThrow(new RuntimeException()).when(delegate).invokeSync(Mockito.any());
    Mockito.when(failOverStrategy.onError(Mockito.any(), Mockito.anyInt()))
        .thenAnswer(new Answer<FailOverStrategy.FailOverAction>() {
          @Override
          public FailOverStrategy.FailOverAction answer(InvocationOnMock invocation) throws Throwable {
            return ((int) invocation.getArguments()[1]) <= count ? FailOverStrategy.FailOverAction.RETRY : null;
          }
        });

    try {
      // action
      performer.invokeSync(call);
      Assert.fail("TimeFormException should be thrown");
    } catch (TimeFormException e) {
      // verification
      Mockito.verify(delegate, Mockito.times(count + 1)).invokeSync(Mockito.any());
      Mockito.verify(failOverStrategy, Mockito.times(count + 1)).onError(Mockito.any(), Mockito.anyInt());
      Mockito.verify(reloginAction, Mockito.never()).run();
    } catch (Exception e) {
      Assert.fail("TimeFormException should be thrown");
    }
  }

  @Test
  public void testRetrySyncWithTimeFormException() {
    // preparation
    int count = 3;
    Mockito.doThrow(new TimeFormException()).when(delegate).invokeSync(Mockito.any());
    Mockito.when(failOverStrategy.onError(Mockito.any(), Mockito.anyInt()))
        .thenAnswer(new Answer<FailOverStrategy.FailOverAction>() {
          @Override
          public FailOverStrategy.FailOverAction answer(InvocationOnMock invocation) throws Throwable {
            return ((int) invocation.getArguments()[1]) <= count ? FailOverStrategy.FailOverAction.RETRY : null;
          }
        });

    try {
      // action
      performer.invokeSync(call);
      Assert.fail("TimeFormException should be thrown");
    } catch (TimeFormException e) {
      // verification
      Mockito.verify(delegate, Mockito.times(count + 1)).invokeSync(Mockito.any());
      Mockito.verify(failOverStrategy, Mockito.times(count + 1)).onError(Mockito.any(), Mockito.anyInt());
      Mockito.verify(reloginAction, Mockito.never()).run();
    } catch (Exception e) {
      Assert.fail("TimeFormException should be thrown");
    }
  }

  @Test
  public void testReloginSync() {
    // preparation
    // exception for first call
    Mockito.doThrow(new TimeFormException()).when(delegate).invokeSync(call);
    // success for second call
    Mockito.doReturn(successResponseBody).when(delegate).invokeSync(callClone);
    Mockito.when(failOverStrategy.onError(Mockito.any(), Mockito.anyInt()))
        .thenReturn(FailOverStrategy.FailOverAction.RELOGIN_AND_RETRY);

    // action
    Object result = performer.invokeSync(call);
    Assert.assertEquals(successResponseBody, result);
    Mockito.verify(delegate, Mockito.times(2)).invokeSync(Mockito.any());
    Mockito.verify(reloginAction).run();
  }

  @Test
  public void testRetryReloginSync() {
    // preparation
    int count = 1;
    Mockito.doThrow(new RuntimeException()).when(delegate).invokeSync(Mockito.any());
    Mockito.doThrow(new RuntimeException()).when(reloginAction).run();
    Mockito.when(failOverStrategy.onError(Mockito.any(), Mockito.anyInt()))
        .thenAnswer(new Answer<FailOverStrategy.FailOverAction>() {
          @Override
          public FailOverStrategy.FailOverAction answer(InvocationOnMock invocation) throws Throwable {
            return ((int) invocation.getArguments()[1]) <= count ? FailOverStrategy.FailOverAction.RELOGIN_AND_RETRY
                : null;
          }
        });
    Mockito.when(failOverStrategy.onReloginError(Mockito.any(), Mockito.anyInt()))
        .thenAnswer(new Answer<FailOverStrategy.FailOverAction>() {
          @Override
          public FailOverStrategy.FailOverAction answer(InvocationOnMock invocation) throws Throwable {
            return ((int) invocation.getArguments()[1]) <= count ? FailOverStrategy.FailOverAction.RETRY : null;
          }
        });

    try {
      // action
      performer.invokeSync(call);
      Assert.fail("TimeFormException should be thrown");
    } catch (TimeFormException e) {
      // verification
      Mockito.verify(delegate, Mockito.times(1)).invokeSync(Mockito.any());
      Mockito.verify(failOverStrategy, Mockito.times(1)).onError(Mockito.any(), Mockito.anyInt());
      Mockito.verify(failOverStrategy, Mockito.times(count + 1)).onReloginError(Mockito.any(), Mockito.anyInt());
      Mockito.verify(reloginAction, Mockito.times(count + 1)).run();
    } catch (Exception e) {
      Assert.fail("TimeFormException should be thrown");
    }
  }

  @Test
  public void testRetryAsyncWithErrorInDelegate() {
    // preparation
    int count = 3;
    RuntimeException rte = new RuntimeException();
    Mockito.doThrow(rte).when(delegate).invokeAsync(Mockito.any(), Mockito.any());
    Mockito.when(failOverStrategy.onError(Mockito.any(), Mockito.anyInt()))
        .thenAnswer(new Answer<FailOverStrategy.FailOverAction>() {
          @Override
          public FailOverStrategy.FailOverAction answer(InvocationOnMock invocation) throws Throwable {
            return ((int) invocation.getArguments()[1]) <= count ? FailOverStrategy.FailOverAction.RETRY : null;
          }
        });

    // action
    performer.invokeAsync(call, dataCallback);
    // verification
    Mockito.verify(dataCallback, Mockito.timeout(1000)).onError(Mockito.any(TimeFormException.class));

    Mockito.verify(failOverStrategy, Mockito.times(count + 1)).onError(Mockito.any(), Mockito.anyInt());
    Mockito.verify(delegate, Mockito.times(count + 1)).invokeAsync(Mockito.any(), Mockito.any());
    Mockito.verify(reloginAction, Mockito.never()).run();
  }

  @Test
  public void testRetryAsyncWithErrorCallbackFromDelegate() {
    // preparation
    int count = 3;
    RuntimeException rte = new RuntimeException();
    Mockito.doAnswer(new Answer() {
      @Override
      public Object answer(InvocationOnMock invocation) throws Throwable {
        ((DataCallback) invocation.getArguments()[0]).onError(rte);
        return null;
      }
    }).when(delegate).invokeAsync(Mockito.any(), Mockito.any());
    Mockito.when(failOverStrategy.onError(Mockito.any(), Mockito.anyInt()))
            .thenAnswer(new Answer<FailOverStrategy.FailOverAction>() {
              @Override
              public FailOverStrategy.FailOverAction answer(InvocationOnMock invocation) throws Throwable {
                return ((int) invocation.getArguments()[1]) <= count ? FailOverStrategy.FailOverAction.RETRY : null;
              }
            });

    // action
    performer.invokeAsync(call, dataCallback);
    // verification
    Mockito.verify(dataCallback, Mockito.timeout(1000)).onError(Mockito.any(TimeFormException.class));

    Mockito.verify(failOverStrategy, Mockito.times(count + 1)).onError(Mockito.any(), Mockito.anyInt());
    Mockito.verify(delegate, Mockito.times(count + 1)).invokeAsync(Mockito.any(), Mockito.any());
    Mockito.verify(reloginAction, Mockito.never()).run();
  }

  @Test
  public void testReloginAsyncWithErrorCallbackFromDelegate() {
    // preparation
    int count = 1;
    RuntimeException rte = new RuntimeException();
    Mockito.doAnswer(new Answer() {
      @Override
      public Object answer(InvocationOnMock invocation) throws Throwable {
        ((DataCallback) invocation.getArguments()[0]).onError(rte);
        return null;
      }
    }).when(delegate).invokeAsync(Mockito.any(), Mockito.any());
    Mockito.when(failOverStrategy.onError(Mockito.any(), Mockito.anyInt()))
            .thenAnswer(new Answer<FailOverStrategy.FailOverAction>() {
              @Override
              public FailOverStrategy.FailOverAction answer(InvocationOnMock invocation) throws Throwable {
                return ((int) invocation.getArguments()[1]) <= count ? FailOverStrategy.FailOverAction.RELOGIN_AND_RETRY : null;
              }
            });

    // action
    performer.invokeAsync(call, dataCallback);
    // verification
    Mockito.verify(dataCallback, Mockito.timeout(1000)).onError(Mockito.any(TimeFormException.class));

    Mockito.verify(failOverStrategy, Mockito.times(count + 1)).onError(Mockito.any(), Mockito.anyInt());
    Mockito.verify(delegate, Mockito.times(count + 1)).invokeAsync(Mockito.any(), Mockito.any());
    Mockito.verify(reloginAction).run();
  }

  @Test
  public void testThrowCustomExceptionFromStrategySync() {
    // preparation
    int count = 1;
    Mockito.doThrow(new RuntimeException()).when(delegate).invokeSync(Mockito.any());
    Exception customException = new IllegalArgumentException();
    // this is main simulation. Exception is thrown from failover stgrategy
    Mockito.doThrow(customException).when(failOverStrategy).onError(Mockito.any(), Mockito.anyInt());

    try {
      // action
      performer.invokeSync(call);
      Assert.fail("TimeFormException should be thrown");
    } catch (Exception e) {
      // verification
      Assert.assertEquals(e, customException);
    }
  }

  @Test
  public void testThrowCustomExceptionFromStrategyAsync() {
    // preparation
    int count = 3;
    RuntimeException rte = new RuntimeException();
    Mockito.doAnswer(new Answer() {
      @Override
      public Object answer(InvocationOnMock invocation) throws Throwable {
        ((DataCallback) invocation.getArguments()[0]).onError(rte);
        return null;
      }
    }).when(delegate).invokeAsync(Mockito.any(), Mockito.any());

    Exception customException = new IllegalArgumentException();
    // this is main simulation. Exception is thrown from failover stgrategy
    Mockito.doThrow(customException).when(failOverStrategy).onError(Mockito.any(), Mockito.anyInt());

    // action
    performer.invokeAsync(call, dataCallback);
    // verification
    ArgumentCaptor<Throwable> captor = ArgumentCaptor.forClass(Throwable.class);
    Mockito.verify(dataCallback, Mockito.timeout(1000)).onError(captor.capture());
    Assert.assertEquals(customException, captor.getValue());
  }

}
