package com.ladbrokescoral.oxygen.seo.showdown.service;

import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.seo.configuration.ShowdownReactiveClient;
import com.ladbrokescoral.oxygen.seo.configuration.ShowdownWebClientConfig;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.stream.Collectors;
import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.MockWebServer;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.HttpHeaders;
import org.springframework.http.MediaType;
import org.springframework.web.reactive.function.client.WebClient;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

@ExtendWith(MockitoExtension.class)
@SpringBootTest(classes = {ShowdownReactiveServiceImpl.class, ShowdownWebClientConfig.class})
class ShowdownReactiveServiceImplTest {

  @Autowired ShowdownReactiveServiceImpl showdownReactiveServiceImpl;
  @MockBean ShowdownReactiveClient showdownReactiveClient;
  @Autowired ShowdownWebClientConfig showdownWebClientConfig;
  private final MockWebServer mockWebServer = new MockWebServer();

  @BeforeEach
  public void setup() {
    WebClient build =
        this.showdownWebClientConfig
            .showdownWebClient()
            .mutate()
            .baseUrl(mockWebServer.url("localhost/").toString())
            .build();
    when(showdownReactiveClient.getClient()).thenReturn(build);
  }

  @Test
  void getCompetitionsReactiveTest() {

    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("Contest.json")));

    Mono<Boolean> bigCompFlag =
        showdownReactiveServiceImpl.getContestInfo("YUhSR0FsQWd2OHFpSmFtK2xqNmE3Zz09");
    StepVerifier.create(bigCompFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertTrue(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getCompetitionsReactiveErrorTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(400)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("Contest.json")));

    Mono<Boolean> bigCompFlag =
        showdownReactiveServiceImpl.getContestInfo("YUhSR0FsQWd2OHFpSmFtK2xqNmE3Zz09");
    StepVerifier.create(bigCompFlag).expectError().verify();
  }

  protected String getResourceFileAsString(String resourceFileName) {
    InputStream is = getClass().getClassLoader().getResourceAsStream(resourceFileName);
    BufferedReader reader = new BufferedReader(new InputStreamReader(is));
    return reader.lines().collect(Collectors.joining("\n"));
  }

  @AfterEach
  public void tearDown() throws IOException {
    mockWebServer.shutdown();
  }
}
