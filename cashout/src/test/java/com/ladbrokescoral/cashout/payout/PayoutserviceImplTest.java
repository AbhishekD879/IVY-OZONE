package com.ladbrokescoral.cashout.payout;

import static org.junit.jupiter.api.Assertions.assertEquals;

import com.google.common.reflect.TypeToken;
import com.ladbrokescoral.cashout.config.PayoutConfig;
import com.ladbrokescoral.cashout.util.GsonUtil;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.lang.reflect.Type;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.MockWebServer;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.test.context.junit.jupiter.SpringExtension;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.reactive.function.client.WebClient;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = {PayoutServiceImpl.class, WebClient.class, PayoutConfig.class})
class PayoutserviceImplTest {

  @Autowired PayoutServiceImpl payoutServiceImpl;
  @Autowired WebClient webClient;
  private final MockWebServer mockWebServer = new MockWebServer();

  @AfterEach
  public void tearDown() throws IOException {
    mockWebServer.shutdown();
  }

  @Test
  void testPotentialReturns() {
    ReflectionTestUtils.setField(
        payoutServiceImpl, "baseUrl", mockWebServer.url("localhost/").toString());
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("PayoutResponseReturns.json")));
    List<PotentialReturns> returns =
        payoutServiceImpl.getPotentialReturns(getReturns("PayoutRequest.json"));
    assertEquals(Collections.emptyList(), returns);
  }

  @Test
  void testPotentialReturns_Error() {
    ReflectionTestUtils.setField(
        payoutServiceImpl, "baseUrl", mockWebServer.url("localhost/").toString());
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(500)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(""));
    List<PotentialReturns> returns =
        payoutServiceImpl.getPotentialReturns(getReturns("PayoutRequest.json"));
    assertEquals(Collections.emptyList(), returns);
  }

  private List<PayoutRequest> getReturns(String fileName) {
    Type type =
        new TypeToken<List<PayoutRequest>>() {
          private static final long serialVersionUID = 1L;
        }.getType();
    List<PayoutRequest> returns = GsonUtil.fromJson(fileName, type);
    return returns;
  }

  protected String getResourceFileAsString(String resourceFileName) {
    InputStream is = getClass().getClassLoader().getResourceAsStream(resourceFileName);
    BufferedReader reader = new BufferedReader(new InputStreamReader(is));
    return reader.lines().collect(Collectors.joining("\n"));
  }
}
