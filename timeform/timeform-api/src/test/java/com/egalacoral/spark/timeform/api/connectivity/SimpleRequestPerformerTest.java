package com.egalacoral.spark.timeform.api.connectivity;

import com.egalacoral.spark.timeform.api.DataCallback;
import com.egalacoral.spark.timeform.api.TimeFormException;
import java.io.IOException;
import okhttp3.MediaType;
import okhttp3.ResponseBody;
import org.junit.*;
import org.junit.rules.ExpectedException;
import org.mockito.ArgumentCaptor;
import org.mockito.ArgumentMatcher;
import org.mockito.Mockito;
import retrofit2.Call;
import retrofit2.Callback;
import retrofit2.Response;

public class SimpleRequestPerformerTest {

  @Rule public ExpectedException expectedException = ExpectedException.none();

  private SimpleRequestPerformer performer;
  private Call<?> call;
  private Response response;
  private DataCallback dataCallback;
  private Object successResponseBody;

  @Before
  public void setUp() throws IOException {
    performer = new SimpleRequestPerformer();
    call = Mockito.mock(Call.class);
    successResponseBody = new Object();
    response = Response.success(successResponseBody);
    dataCallback = Mockito.mock(DataCallback.class);
    Mockito.when(call.execute()).thenReturn(response);
    Mockito.doAnswer(
            invocation -> {
              ((Callback) invocation.getArguments()[0]).onResponse(call, response);
              return null;
            })
        .when(call)
        .enqueue(Mockito.any(Callback.class));
  }

  @After
  public void tearDown() {
    performer = null;
    call = null;
  }

  @Test
  public void testSync() throws IOException {
    Object response = performer.invokeSync(call);
    Mockito.verify(call).execute();
    Assert.assertEquals(successResponseBody, response);
  }

  @Test
  public void testAsync() throws IOException {
    performer.invokeAsync(call, dataCallback);
    Mockito.verify(call).enqueue(Mockito.any());
    Mockito.verify(dataCallback).onResponse(Mockito.eq(successResponseBody));
  }

  @Test
  public void testSyncErrorResponse() throws IOException {
    Object errorResponse = new Object();
    int httpCode = 400;
    response = Response.error(httpCode, ResponseBody.create(MediaType.parse("text/json"), "{}"));
    Mockito.when(call.execute()).thenReturn(response);

    expectedException.expect(TimeFormException.class);
    expectedException.expect(
        new ArgumentMatcher<Object>() {
          @Override
          public boolean matches(Object argument) {
            TimeFormException tfe = (TimeFormException) argument;
            Assert.assertEquals("error code", Integer.valueOf(httpCode), tfe.getHttpCode());
            return true;
          }
        });

    performer.invokeSync(call);
  }

  @Test
  public void testSyncInternalError() throws IOException {
    Object errorResponse = new Object();
    int httpCode = 400;
    RuntimeException rte = new RuntimeException();
    Mockito.when(call.execute()).thenThrow(rte);

    expectedException.expect(TimeFormException.class);
    expectedException.expect(
        new ArgumentMatcher<Object>() {
          @Override
          public boolean matches(Object argument) {
            TimeFormException tfe = (TimeFormException) argument;
            Assert.assertEquals("caused by", rte, tfe.getCause());
            return true;
          }
        });

    performer.invokeSync(call);
  }

  @Test
  public void testAsyncErrorResponse() throws IOException {
    Object errorResponse = new Object();
    int httpCode = 400;
    response = Response.error(httpCode, ResponseBody.create(MediaType.parse("text/json"), "{}"));

    Mockito.doAnswer(
            invocation -> {
              ((Callback) invocation.getArguments()[0]).onResponse(call, response);
              return null;
            })
        .when(call)
        .enqueue(Mockito.any(Callback.class));

    performer.invokeAsync(call, dataCallback);

    Mockito.verify(dataCallback, Mockito.never()).onResponse(Mockito.any());
    ArgumentCaptor<Exception> captor = ArgumentCaptor.forClass(Exception.class);
    Mockito.verify(dataCallback).onError(captor.capture());
    Throwable throwable = captor.getValue();
    Assert.assertEquals(TimeFormException.class, throwable.getClass());
    TimeFormException tfe = (TimeFormException) throwable;
    Assert.assertEquals(Integer.valueOf(httpCode), tfe.getHttpCode());
  }

  @Test
  public void testAsyncInternalError() throws IOException {
    Object errorResponse = new Object();
    RuntimeException rte = new RuntimeException();

    Mockito.doThrow(rte).when(call).enqueue(Mockito.any(Callback.class));

    performer.invokeAsync(call, dataCallback);

    Mockito.verify(dataCallback, Mockito.never()).onResponse(Mockito.any());
    ArgumentCaptor<Exception> captor = ArgumentCaptor.forClass(Exception.class);
    Mockito.verify(dataCallback).onError(captor.capture());
    Throwable throwable = captor.getValue();
    Assert.assertEquals(TimeFormException.class, throwable.getClass());
    TimeFormException tfe = (TimeFormException) throwable;
    Assert.assertEquals(rte, tfe.getCause());
  }

  @Test
  public void testAsyncErrorDetectedByRetrofit() throws IOException {
    Object errorResponse = new Object();
    RuntimeException rte = new RuntimeException();

    Mockito.doAnswer(
            invocation -> {
              ((Callback) invocation.getArguments()[0]).onFailure(call, rte);
              return null;
            })
        .when(call)
        .enqueue(Mockito.any(Callback.class));

    performer.invokeAsync(call, dataCallback);

    Mockito.verify(dataCallback, Mockito.never()).onResponse(Mockito.any());
    ArgumentCaptor<Exception> captor = ArgumentCaptor.forClass(Exception.class);
    Mockito.verify(dataCallback).onError(captor.capture());
    Throwable throwable = captor.getValue();
    Assert.assertEquals(TimeFormException.class, throwable.getClass());
    TimeFormException tfe = (TimeFormException) throwable;
    Assert.assertEquals(rte, tfe.getCause());
  }

  @Test
  public void testAsyncTimeFormInternalError() throws IOException {
    Object errorResponse = new Object();
    TimeFormException rte = new TimeFormException();

    Mockito.doThrow(rte).when(call).enqueue(Mockito.any(Callback.class));

    performer.invokeAsync(call, dataCallback);

    Mockito.verify(dataCallback, Mockito.never()).onResponse(Mockito.any());
    ArgumentCaptor<Exception> captor = ArgumentCaptor.forClass(Exception.class);
    Mockito.verify(dataCallback).onError(captor.capture());
    Throwable throwable = captor.getValue();
    Assert.assertEquals(rte, throwable);
  }

  @Test
  public void testAsyncTimeFormErrorDetectedByRetrofit() throws IOException {
    Object errorResponse = new Object();
    TimeFormException rte = new TimeFormException();

    Mockito.doAnswer(
            invocation -> {
              ((Callback) invocation.getArguments()[0]).onFailure(call, rte);
              return null;
            })
        .when(call)
        .enqueue(Mockito.any(Callback.class));

    performer.invokeAsync(call, dataCallback);

    Mockito.verify(dataCallback, Mockito.never()).onResponse(Mockito.any());
    ArgumentCaptor<Exception> captor = ArgumentCaptor.forClass(Exception.class);
    Mockito.verify(dataCallback).onError(captor.capture());
    Throwable throwable = captor.getValue();
    Assert.assertEquals(throwable, rte);
  }
}
