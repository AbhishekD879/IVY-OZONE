package com.egalacoral.spark.timeform.api;

import com.egalacoral.spark.timeform.api.tools.Tools;
import com.egalacoral.spark.timeform.model.greyhound.Performance;
import com.egalacoral.spark.timeform.model.greyhound.Track;
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
import org.mockito.runners.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class TimeFormApiIntegrationTest {

  private final int WAIT_TIMEOUT = 500;

  private final String USER_NAME = "user123";
  private final String PASSWORD = "password123";

  private final String LOGIN_URL = "http://127.0.0.1";
  private final String DATA_URL = "http://127.0.0.2/";
  private final String IMG_URL = "http://127.0.0.3/";
  private final String GH_SUFFIX = "gh";
  private final String HR_SUFFIX = "hr";

  private DelegateInterceptor interceptor;

  private TimeFormAPI api;

  @Mock private DataCallback dataCallback;

  @Before
  public void setUp() {
    interceptor = new DelegateInterceptor();
    api =
        new TimeFormAPIBuilder(LOGIN_URL, DATA_URL, GH_SUFFIX, HR_SUFFIX, IMG_URL) //
            .setTestInterceptor(interceptor)
            .build();
  }

  @Test
  public void testLogin() {
    interceptor.setDelegate(
        chain -> {
          Request request = chain.request();
          Assert.assertEquals("POST", request.method());
          Map<String, String> params = parseRequestParams(request);
          Assert.assertEquals(USER_NAME, params.get("username"));
          Assert.assertEquals(PASSWORD, params.get("password"));
          return makeResponse(200, "access_token.json", request);
        });

    TimeFormService service = api.login(USER_NAME, PASSWORD);

    Assert.assertNotNull(service);
    Assert.assertTrue(interceptor.getCallsCount() > 0);
  }

  @Test
  public void testUseToken() {
    Date d = new Date();
    TimeFormService service = doLogin();

    interceptor.setDelegate(
        chain -> {
          Request request = chain.request();
          Assert.assertEquals("Bearer ACCESSTOKEN123", request.header("Authorization"));
          return makeResponse(200, "gh_meetings.json", request);
        });

    service.getMeetingsForDate(d, dataCallback);

    Mockito.verify(dataCallback, Mockito.timeout(WAIT_TIMEOUT)).onResponse(Mockito.any());
    Assert.assertTrue(interceptor.getCallsCount() > 0);
  }

  @Test
  public void testGetGHTracks() {
    Date d = new Date();
    TimeFormService service = doLogin();

    interceptor.setDelegate(
        chain -> {
          Request request = chain.request();
          Assert.assertTrue(request.url().toString().startsWith(DATA_URL + GH_SUFFIX + "/tracks"));
          return makeResponse(200, "gh_tracks.json", request);
        });

    service.getTracks(dataCallback);

    ArgumentCaptor<List> captor = ArgumentCaptor.forClass(List.class);
    Mockito.verify(dataCallback, Mockito.timeout(WAIT_TIMEOUT)).onResponse(captor.capture());
    Assert.assertTrue(interceptor.getCallsCount() > 0);
    Assert.assertEquals(3, captor.getValue().size());
    Assert.assertTrue(captor.getValue().get(0) instanceof Track);
  }

  @Test
  public void testGetGHPerformancesByMeetingDate() {
    Date d = new Date();
    TimeFormService service = doLogin();

    interceptor.setDelegate(
        chain -> {
          Request request = chain.request();
          Assert.assertTrue(
              request.url().toString().startsWith(DATA_URL + GH_SUFFIX + "/performances"));
          System.out.println(request.url().toString());
          Assert.assertTrue(
              request
                  .url()
                  .toString()
                  .contains(
                      "race/meeting/meeting_date%20eq%20datetime%27"
                          + Tools.simpleDateFormat("yyyy-MM-dd").format(d)
                          + "%27"));
          return makeResponse(200, "gh_performances.json", request);
        });

    service.getPerformancesByMeetingDate(d, dataCallback);

    ArgumentCaptor<List> captor = ArgumentCaptor.forClass(List.class);
    Mockito.verify(dataCallback, Mockito.timeout(WAIT_TIMEOUT)).onResponse(captor.capture());
    Assert.assertTrue(interceptor.getCallsCount() > 0);
    Assert.assertEquals(4, captor.getValue().size());
    Assert.assertTrue(captor.getValue().get(0) instanceof Performance);
  }

  private TimeFormService doLogin() {
    interceptor.setDelegate(
        chain -> {
          Request request = chain.request();
          return makeResponse(200, "access_token.json", request);
        });
    TimeFormService service = api.login(USER_NAME, PASSWORD);
    interceptor.setDelegate(null);
    interceptor.resetCallsCount();
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
