package com.coral.oxygen.middleware.ms.liveserv.client;

import com.coral.oxygen.middleware.ms.liveserv.exceptions.RequestFailedException;
import com.coral.oxygen.middleware.ms.liveserv.exceptions.ServiceException;
import java.io.IOException;
import java.io.InterruptedIOException;
import java.util.Optional;
import java.util.concurrent.*;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;

/** Created by azayats on 18.05.17. */
public class RetryableCallTest {

  private Call delegate;

  private RetryableCall retryableCall;

  @Before
  public void setUp() {
    delegate = Mockito.mock(Call.class);
    retryableCall = new RetryableCall(delegate);
    retryableCall.setRetriesDelay(1);
  }

  @Test
  public void testDelegateExecute() throws IOException, ServiceException, InterruptedException {
    String request = "REQ";
    String response = "RESP";
    Mockito.doReturn(response).when(delegate).execute(request);

    // action
    String result = retryableCall.execute(request);

    // verification
    Mockito.verify(delegate).execute(request);
    Assert.assertEquals(response, result);
  }

  @Test
  public void testRetries() throws IOException, ServiceException, InterruptedException {
    String request = "REQ";
    String response = "RESP";
    Mockito.when(delegate.execute(request)) //
        .thenThrow(new IOException()) //
        .thenThrow(new IOException()) //
        .thenThrow(new IOException()) //
        .thenReturn(response);
    retryableCall.setRetriesCount(3);

    // action
    String result = retryableCall.execute(request);

    // verification
    Mockito.verify(delegate, Mockito.times(4)).execute(request);
    Assert.assertEquals(response, result);
  }

  @Test
  public void testRetriesExceeded() throws IOException, ServiceException, InterruptedException {
    String request = "REQ";
    Mockito.when(delegate.execute(request)) //
        .thenThrow(new IOException());
    retryableCall.setRetriesCount(3);

    // action
    try {
      retryableCall.execute(request);
      // verification
      Assert.fail("Exception should be thrown");
    } catch (ServiceException e) {
      // verification
      Assert.assertEquals(RequestFailedException.class, e.getClass());
    }

    // verification
    Mockito.verify(delegate, Mockito.times(4)).execute(request);
  }

  @Test
  public void testNoRetryAfterServiceException()
      throws IOException, ServiceException, InterruptedException {
    String request = "REQ";
    ServiceException expectedException = new ServiceException();
    Mockito.when(delegate.execute(request)) //
        .thenThrow(expectedException);
    retryableCall.setRetriesCount(3);

    // action
    try {
      retryableCall.execute(request);
      // verification
      Assert.fail("Exception should be thrown");
    } catch (ServiceException e) {
      // verification
      Assert.assertSame(expectedException, e);
    }

    // verification
    Mockito.verify(delegate, Mockito.times(1)).execute(request);
  }

  @Test
  public void testInterruptSlleping()
      throws IOException, ServiceException, InterruptedException, TimeoutException,
          ExecutionException {
    String request = "REQ";
    Mockito.when(delegate.execute(request)) //
        .thenThrow(new IOException());
    retryableCall.setRetriesCount(3);
    retryableCall.setRetriesDelay(10000);

    // action
    ExecutorService executor = Executors.newSingleThreadExecutor();
    Future<Optional<Exception>> future =
        executor.submit(
            () -> {
              try {
                retryableCall.execute(request);
                return Optional.empty();
              } catch (Exception e) {
                return Optional.of(e);
              }
            });
    Thread.sleep(500);
    executor.shutdownNow();

    Optional<Exception> exception = future.get(1000, TimeUnit.MILLISECONDS);

    // verification
    Assert.assertEquals(InterruptedException.class, exception.get().getClass());
    Assert.assertTrue(executor.isShutdown());
  }

  @Test
  public void testUnhandledInterruptedIOException()
      throws IOException, ServiceException, InterruptedException, TimeoutException,
          ExecutionException {
    String request = "REQ";
    InterruptedIOException expectedException = new InterruptedIOException();
    Mockito.when(delegate.execute(request)) //
        .thenThrow(expectedException);
    retryableCall.setRetriesCount(3);
    retryableCall.setRetriesDelay(10000);

    // action
    // action
    try {
      retryableCall.execute(request);
      // verification
      Assert.fail("Exception should be thrown");
    } catch (Exception e) {
      // verification
      Assert.assertSame(expectedException, e);
    }

    // verification
    Mockito.verify(delegate, Mockito.times(1)).execute(request);
  }

  @Test
  public void testUnhandledInterruptedExceptionInCause()
      throws IOException, ServiceException, InterruptedException, TimeoutException,
          ExecutionException {
    String request = "REQ";
    IOException expectedException = new IOException(new InterruptedException());
    Mockito.when(delegate.execute(request)) //
        .thenThrow(expectedException);
    retryableCall.setRetriesCount(3);
    retryableCall.setRetriesDelay(10000);

    // action
    // action
    try {
      retryableCall.execute(request);
      // verification
      Assert.fail("Exception should be thrown");
    } catch (Exception e) {
      // verification
      Assert.assertEquals(InterruptedException.class, e.getClass());
    }

    // verification
    Mockito.verify(delegate, Mockito.times(1)).execute(request);
  }
}
