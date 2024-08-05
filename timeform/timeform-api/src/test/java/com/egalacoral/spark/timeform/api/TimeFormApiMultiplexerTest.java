package com.egalacoral.spark.timeform.api;

import com.egalacoral.spark.timeform.api.multiplexer.TimeFormAPIMultiplexer;
import com.egalacoral.spark.timeform.model.greyhound.Meeting;
import java.io.IOException;
import java.io.InputStream;
import java.util.*;
import okhttp3.*;
import okhttp3.internal.http.RealResponseBody;
import okio.Buffer;
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

@RunWith(MockitoJUnitRunner.class)
public class TimeFormApiMultiplexerTest {

  private final int WAIT_TIMEOUT = 500;

  private final String USER_NAME = "user123";
  private final String PASSWORD = "password123";

  private final String LOGIN_URL = "http://127.0.0.1";
  private final String DATA_URL = "http://127.0.0.2/";
  private final String IMG_URL = "http://127.0.0.3/";
  private final String GH_SUFFIX = "gh";
  private final String HR_SUFFIX = "hr";

  private DelegateInterceptor interceptor1;
  private DelegateInterceptor interceptor2;

  private TimeFormAPI api;

  @Mock private DataCallback dataCallback;

  @Before
  public void setUp() {
    interceptor1 = new DelegateInterceptor();
    interceptor2 = new DelegateInterceptor();
    TimeFormAPI api1 =
        new TimeFormAPIBuilder(LOGIN_URL, DATA_URL, "gh", "hr", IMG_URL) //
            .setTestInterceptor(interceptor1)
            .build();
    TimeFormAPI api2 =
        new TimeFormAPIBuilder(LOGIN_URL, DATA_URL, "gh", "hr", IMG_URL) //
            .setTestInterceptor(interceptor2)
            .build();
    api = new TimeFormAPIMultiplexer(api1, api2);
  }

  @Test
  public void testRequestData() {
    Date d = new Date();
    TimeFormService service = doLogin();

    interceptor1.setDelegate(
        chain -> {
          Request request = chain.request();
          return makeResponse(200, "gh_meetings.json", request);
        });
    interceptor2.setDelegate(interceptor1);

    service.getMeetingsForDate(d, dataCallback);

    ArgumentCaptor<List> captor = ArgumentCaptor.forClass(List.class);
    Mockito.verify(dataCallback, Mockito.timeout(WAIT_TIMEOUT)).onResponse(captor.capture());
    Assert.assertTrue(interceptor1.getCallsCount() > 0);
    Assert.assertTrue(interceptor2.getCallsCount() > 0);
    Assert.assertEquals(18, captor.getValue().size());
    Assert.assertTrue(captor.getValue().get(0) instanceof Meeting);
  }

  @Test
  public void testFirstApiReturnError() {
    TimeFormService service = doLogin();

    interceptor1.setDelegate(
        chain -> {
          Request request = chain.request();
          return makeResponse(404, "gh_tracks.json", request);
        });
    interceptor2.setDelegate(
        chain -> {
          Request request = chain.request();
          return makeResponse(200, "gh_tracks.json", request);
        });

    service.getTracks(dataCallback);

    ArgumentCaptor<List> captor = ArgumentCaptor.forClass(List.class);
    Mockito.verify(dataCallback, Mockito.timeout(WAIT_TIMEOUT)).onError(Mockito.any());
    Assert.assertTrue(interceptor1.getCallsCount() > 0);
    Assert.assertTrue(interceptor2.getCallsCount() == 0);
  }

  @Test
  public void testSecondApiReturnError() {
    TimeFormService service = doLogin();

    interceptor1.setDelegate(
        chain -> {
          Request request = chain.request();
          return makeResponse(200, "gh_tracks.json", request);
        });
    interceptor2.setDelegate(
        chain -> {
          Request request = chain.request();
          return makeResponse(404, "gh_tracks.json", request);
        });

    service.getTracks(dataCallback);

    ArgumentCaptor<List> captor = ArgumentCaptor.forClass(List.class);
    Mockito.verify(dataCallback, Mockito.timeout(WAIT_TIMEOUT)).onError(Mockito.any());
    Assert.assertTrue(interceptor1.getCallsCount() > 0);
    Assert.assertTrue(interceptor2.getCallsCount() > 0);
  }

  @Test
  public void testFirstApiFail() {
    TimeFormAPI api1 = Mockito.mock(TimeFormAPI.class);
    TimeFormAPI api2 = Mockito.mock(TimeFormAPI.class);
    TimeFormService service1 = Mockito.mock(TimeFormService.class);
    TimeFormService service2 = Mockito.mock(TimeFormService.class);
    Mockito.when(api1.login(Mockito.anyString(), Mockito.anyString())).thenReturn(service1);
    Mockito.when(api2.login(Mockito.anyString(), Mockito.anyString())).thenReturn(service2);
    Mockito.doThrow(new RuntimeException()).when(service1).getTracks(Mockito.any());

    api = new TimeFormAPIMultiplexer(api1, api2);
    TimeFormService service = doLogin();

    service.getTracks(dataCallback);

    ArgumentCaptor<List> captor = ArgumentCaptor.forClass(List.class);
    Mockito.verify(dataCallback, Mockito.timeout(WAIT_TIMEOUT)).onError(Mockito.any());
  }

  @Test
  public void testSecondApiFail() {
    TimeFormAPI api1 = Mockito.mock(TimeFormAPI.class);
    TimeFormAPI api2 = Mockito.mock(TimeFormAPI.class);
    TimeFormService service1 = Mockito.mock(TimeFormService.class);
    TimeFormService service2 = Mockito.mock(TimeFormService.class);
    Mockito.when(api1.login(Mockito.anyString(), Mockito.anyString())).thenReturn(service1);
    Mockito.when(api2.login(Mockito.anyString(), Mockito.anyString())).thenReturn(service2);
    Mockito.doAnswer(
            new Answer() {
              @Override
              public Object answer(InvocationOnMock invocation) throws Throwable {
                ((DataCallback) invocation.getArguments()[0]).onResponse(new ArrayList());
                return null;
              }
            })
        .when(service1)
        .getTracks(Mockito.any());
    Mockito.doThrow(new RuntimeException()).when(service2).getTracks(Mockito.any());

    api = new TimeFormAPIMultiplexer(api1, api2);
    TimeFormService service = doLogin();

    service.getTracks(dataCallback);

    ArgumentCaptor<List> captor = ArgumentCaptor.forClass(List.class);
    Mockito.verify(dataCallback, Mockito.timeout(WAIT_TIMEOUT)).onError(Mockito.any());
  }

  @Test
  public void testSetPageSize() {
    TimeFormAPI api1 = Mockito.mock(TimeFormAPI.class);
    TimeFormAPI api2 = Mockito.mock(TimeFormAPI.class);
    TimeFormService service1 = Mockito.mock(TimeFormService.class);
    TimeFormService service2 = Mockito.mock(TimeFormService.class);
    Mockito.when(api1.login(Mockito.anyString(), Mockito.anyString())).thenReturn(service1);
    Mockito.when(api2.login(Mockito.anyString(), Mockito.anyString())).thenReturn(service2);

    api = new TimeFormAPIMultiplexer(api1, api2);
    TimeFormService service = doLogin();

    int pageSize = 25;
    service.setPageSize(pageSize);

    Mockito.verify(service1).setPageSize(pageSize);
    Mockito.verify(service2).setPageSize(pageSize);
  }

  @Test
  public void testGetPageSize() {
    TimeFormAPI api1 = Mockito.mock(TimeFormAPI.class);
    TimeFormAPI api2 = Mockito.mock(TimeFormAPI.class);
    TimeFormService service1 = Mockito.mock(TimeFormService.class);
    TimeFormService service2 = Mockito.mock(TimeFormService.class);
    Mockito.when(api1.login(Mockito.anyString(), Mockito.anyString())).thenReturn(service1);
    Mockito.when(api2.login(Mockito.anyString(), Mockito.anyString())).thenReturn(service2);

    int pageSize = 105;
    Mockito.when(service1.getPageSize()).thenReturn(pageSize);

    api = new TimeFormAPIMultiplexer(api1, api2);
    TimeFormService service = doLogin();

    int actualSize = service.getPageSize();

    Mockito.verify(service1).getPageSize();
    Assert.assertEquals(pageSize, actualSize);
  }

  private TimeFormService doLogin() {
    interceptor1.setDelegate(
        chain -> {
          Request request = chain.request();
          return makeResponse(200, "access_token.json", request);
        });
    interceptor2.setDelegate(interceptor1);
    TimeFormService service = api.login(USER_NAME, PASSWORD);
    interceptor1.setDelegate(null);
    interceptor1.resetCallsCount();
    interceptor2.setDelegate(null);
    interceptor2.resetCallsCount();
    return service;
  }

  private static class DelegateInterceptor implements Interceptor {
    private Interceptor delegate;

    private int callsCount = 0;

    public void resetCallsCount() {
      callsCount = 0;
    }

    public void setDelegate(Interceptor delegate) {
      this.delegate = delegate;
    }

    public int getCallsCount() {
      return callsCount;
    }

    @Override
    public Response intercept(Chain chain) throws IOException {
      callsCount++;
      return delegate.intercept(chain);
    }
  }

  private Map<String, String> parseRequestParams(Request request) {
    Map<String, String> result = new HashMap<>();
    if (request.body() instanceof FormBody) {
      FormBody body = (FormBody) request.body();
      for (int i = 0; i < body.size(); i++) {
        result.put(body.name(i), body.value(i));
      }
    }
    return result;
  }

  private String readResponse(String name) throws IOException {
    InputStream resource = getClass().getClassLoader().getResourceAsStream("responses/" + name);
    Scanner scanner = new Scanner(resource);
    StringBuilder stringBuilder = new StringBuilder();
    while (scanner.hasNextLine()) {
      stringBuilder.append(scanner.nextLine()).append("\n");
    }
    scanner.close();
    return stringBuilder.toString();
  }

  private Response makeResponse(int code, String name, Request request) throws IOException {
    Buffer buffer = new Buffer();
    buffer.writeUtf8(readResponse(name));
    return new Response.Builder() //
        .code(code) //
        .request(request) //
        .protocol(Protocol.HTTP_1_1)
        .body(new RealResponseBody(Headers.of(), buffer)) //
        .build();
  }
}
