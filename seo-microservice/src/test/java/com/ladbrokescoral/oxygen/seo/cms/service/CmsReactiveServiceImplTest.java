package com.ladbrokescoral.oxygen.seo.cms.service;

import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.api.SiteServerApiAsync;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.seo.configuration.CmsReactiveClient;
import com.ladbrokescoral.oxygen.seo.configuration.CmsWebClientConfig;
import com.ladbrokescoral.oxygen.seo.dto.InitialDataDto;
import com.ladbrokescoral.oxygen.seo.dto.SportTabConfigListDto;
import com.ladbrokescoral.oxygen.seo.siteserver.service.SeoSiteServerService;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.util.Optional;
import java.util.stream.Collectors;
import okhttp3.mockwebserver.MockResponse;
import okhttp3.mockwebserver.MockWebServer;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.CsvFileSource;
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
@SpringBootTest(classes = {CmsReactiveServiceImpl.class, CmsWebClientConfig.class})
class CmsReactiveServiceImplTest {

  @Autowired CmsReactiveServiceImpl cmsReactiveServiceImpl;
  @MockBean SeoSiteServerService seoSiteServerService;
  @MockBean SiteServerApiAsync siteServerApiAsync;
  @MockBean CmsReactiveClient cmsReactiveClient;
  @Autowired CmsWebClientConfig cmsWebClientConfig;
  private final MockWebServer mockWebServer = new MockWebServer();

  @BeforeEach
  public void setup() {
    WebClient build =
        this.cmsWebClientConfig
            .cmsWebClient()
            .mutate()
            .baseUrl(mockWebServer.url("localhost/").toString())
            .build();
    when(cmsReactiveClient.getCMSWebClient()).thenReturn(build);
  }

  @Test
  void getVirtualSportTest() {
    Event event = new Event();
    event.setName("football");
    event.setId("132568");
    when(siteServerApiAsync.getEventToOutcomeForEvent("237945501"))
        .thenReturn(Mono.just(Optional.of(event)));
    when(seoSiteServerService.getEvent("237945501")).thenReturn(Mono.just(true));
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("virtualsport.json")));
    Mono<Boolean> cmsReactiveFlag =
        cmsReactiveServiceImpl.isVirtualSport("BMA", "Football", "UK Football", "237945501");
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertTrue(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getVirtualSportEventExceptionTest() {
    Event event = new Event();
    event.setName("football");
    event.setId("132568");
    when(siteServerApiAsync.getEventToOutcomeForEvent("237945501"))
        .thenReturn(Mono.just(Optional.of(event)));
    when(seoSiteServerService.getEvent("237945501")).thenThrow(RuntimeException.class);
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("virtualsport.json")));
    Mono<Boolean> cmsReactiveFlag =
        cmsReactiveServiceImpl.isVirtualSport("BMA", "Football", "UK Football", "237945501");
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getVirtualSportemptyDataTest() {
    Event event = new Event();
    event.setName("footballs");
    event.setId("132568");
    when(siteServerApiAsync.getEventToOutcomeForEvent("237945501"))
        .thenReturn(Mono.just(Optional.of(event)));
    when(seoSiteServerService.getEvent("237945501")).thenReturn(Mono.just(true));
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("virtualsportempty.json")));
    Mono<Boolean> cmsReactiveFlag =
        cmsReactiveServiceImpl.isVirtualSport("BMA", "Football", "UK Football", "");
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getVirtualSportFalseTest() {
    Event event = new Event();
    event.setName("football");
    event.setId("132568");
    when(siteServerApiAsync.getEventToOutcomeForEvent("237945501"))
        .thenReturn(Mono.just(Optional.of(event)));
    when(seoSiteServerService.getEvent("237945501")).thenReturn(Mono.just(true));
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(500)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("virtualsport.json")));
    Mono<Boolean> cmsReactiveFlag =
        cmsReactiveServiceImpl.isVirtualSport(
            "BMA", "horse-racing", "horse-racing-flat", "237945501");
    StepVerifier.create(cmsReactiveFlag).expectError().verify();
  }

  @Test
  void getFanzoneTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("fanzone.json")));
    Mono<Boolean> cmsReactiveFlag = cmsReactiveServiceImpl.isFanzone("BMA", "Football", "now-next");
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertTrue(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getFanzoneNegativeTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("fanzone.json")));
    Mono<Boolean> cmsReactiveFlag =
        cmsReactiveServiceImpl.isFanzone("coral", "Footballs", "now-nexts");
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getFanzoneNegativetabTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("fanzone.json")));
    Mono<Boolean> cmsReactiveFlag =
        cmsReactiveServiceImpl.isFanzone("BMA", "Football", "now-nexts");
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getFanzoneErrorTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(500)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("fanzone.json")));
    Mono<Boolean> cmsReactiveFlag =
        cmsReactiveServiceImpl.isFanzone("BMA", "Footballs", "now-nexts");
    StepVerifier.create(cmsReactiveFlag).expectError().verify();
  }

  @Test
  void getEventHubDataTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("initialData.json")));
    Mono<Boolean> cmsReactiveFlag = cmsReactiveServiceImpl.isEventHubData("bma", "tablet", 101);
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertTrue(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getSportNameTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("initialData.json")));
    Mono<Boolean> cmsReactiveFlag =
        cmsReactiveServiceImpl.isSportName("bma", "sport-football", "desktop");
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getEventHubDataErrorTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(500)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("initialData.json")));
    Mono<Boolean> cmsReactiveFlag = cmsReactiveServiceImpl.isEventHubData("bma", "ios", 101);
    StepVerifier.create(cmsReactiveFlag).expectError().verify();
  }

  @Test
  void getEventHubDataNegativeTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("initialData.json")));
    Mono<Boolean> cmsReactiveFlag = cmsReactiveServiceImpl.isEventHubData("bma", "ios", 102);
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getPromotionTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("promotion.json")));
    Mono<Boolean> cmsReactiveFlag = cmsReactiveServiceImpl.isPromotion("bma", "56");
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertTrue(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getPromotionErrorTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(500)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("promotion.json")));
    Mono<Boolean> cmsReactiveFlag = cmsReactiveServiceImpl.isPromotion("bma", "56");
    StepVerifier.create(cmsReactiveFlag).expectError().verify();
  }

  @Test
  void getSportTabTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("initialData.json")));
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("SportTabConfig.json")));

    Mono<Boolean> cmsReactiveFlag =
        cmsReactiveServiceImpl.isSportTab(
            "Bma", "sport-football", "now-nexts", "tomorrow", "desktop");
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertTrue(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getSportSubtabEmptyTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("initialData.json")));
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("SportTabConfig.json")));
    Mono<Boolean> cmsReactiveFlag =
        cmsReactiveServiceImpl.isSportTab("Bma", "sport-football", "now-nexts", null, "desktop");
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertTrue(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  /*

    @Test
    void getSportTabTest() {
      mockWebServer.enqueue(
          new MockResponse()
              .setResponseCode(200)
              .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
              .setBody(this.getResourceFileAsString("initialData.json")));
      mockWebServer.enqueue(
          new MockResponse()
              .setResponseCode(200)
              .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
              .setBody(this.getResourceFileAsString("SportTabConfig.json")));

      Mono<Boolean> cmsReactiveFlag =
          cmsReactiveServiceImpl.getSportTab(
              "Bma", "sport-football", "now-nexts", "tomorrow", "desktop");
      StepVerifier.create(cmsReactiveFlag)
          .assertNext(
              aBoolean -> {
                Assertions.assertTrue(aBoolean);
              })
          .expectComplete()
          .verify();
    }

    @Test
    void getSportTabInitCallTest() {
      mockWebServer.enqueue(
          new MockResponse()
              .setResponseCode(200)
              .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
              .setBody(this.getResourceFileAsString("initialData.json")));
      mockWebServer.enqueue(
          new MockResponse()
              .setResponseCode(200)
              .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
              .setBody(this.getResourceFileAsString("SportTabConfig.json")));

      Mono<Boolean> cmsReactiveFlag =
          cmsReactiveServiceImpl.getSportTab(
              "Bma", "sport-football", "now-nexts", "tomorrow", "desktop");
      StepVerifier.create(cmsReactiveFlag)
          .assertNext(
              aBoolean -> {
                Assertions.assertTrue(aBoolean);
              })
          .expectComplete()
          .verify();
    }

    @Test
    void getSportSubtabEmptyTest() {
      mockWebServer.enqueue(
          new MockResponse()
              .setResponseCode(200)
              .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
              .setBody(this.getResourceFileAsString("initialData.json")));
      mockWebServer.enqueue(
          new MockResponse()
              .setResponseCode(200)
              .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
              .setBody(this.getResourceFileAsString("SportTabConfig.json")));
      Mono<Boolean> cmsReactiveFlag =
          cmsReactiveServiceImpl.getSportTab("Bma", "sport-football", "now-nexts", null, "desktop");
      StepVerifier.create(cmsReactiveFlag)
          .assertNext(
              aBoolean -> {
                Assertions.assertTrue(aBoolean);
              })
          .expectComplete()
          .verify();
    }
  */

  /*@ParameterizedTest(
      name = "{index} => brand={0}, categoryName={1}, tabName={2}, subTabName={3},deviceType={4}")
  @CsvFileSource(resources = "/sportstab-data.csv")
  void getSportSubTabInitParameterizedTest(
      String brand, String categoryName, String tabName, String subTabName, String deviceType) {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("initialData.json")));
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("SportTabConfig.json")));

    Mono<Boolean> cmsReactiveFlag =
        cmsReactiveServiceImpl.getSportTab(brand, categoryName, tabName, subTabName, deviceType);
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }*/

  @ParameterizedTest(name = "{index} => categoryName={0}, tabName={1}, subTabName={2}")
  @CsvFileSource(resources = "/test-data.csv")
  void getSportsubTabParameterizedTest(String categoryName, String tabName, String subTabName) {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("initialData.json")));

    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("SportTabConfig.json")));
    Mono<Boolean> cmsReactiveFlag =
        cmsReactiveServiceImpl.isSportTab("Bma", categoryName, tabName, subTabName, "desktop");
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getinitialDataApiRespErrorTest() {
    /*mockWebServer.enqueue(
    new MockResponse()
        .setResponseCode(200)
        .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
        .setBody(""));*/
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(500)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(""));
    Mono<InitialDataDto> initialDataApiResp =
        cmsReactiveServiceImpl.getInitialDataApiResp("bma", "desktop");

    StepVerifier.create(initialDataApiResp).expectError().verify();
  }

  @Test
  void getSportTabErrorTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(500)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(""));
    Mono<SportTabConfigListDto> sportTabResp =
        cmsReactiveServiceImpl.getSportTabResp("bma", "desktop");

    StepVerifier.create(sportTabResp).expectError().verify();
  }

  @Test
  void getInplaySportTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("inplay.json")));
    Mono<Boolean> cmsReactiveFlag = cmsReactiveServiceImpl.isInplaySport("bma", "56");
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertTrue(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getInplaySportfalseTests() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("inplayfalse.json")));
    Mono<Boolean> cmsReactiveFlag = cmsReactiveServiceImpl.isInplaySport("bma", "58");
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getInplaySportfalseTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("inplay.json")));
    Mono<Boolean> cmsReactiveFlag = cmsReactiveServiceImpl.isInplaySport("bma", "58");
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getInplaySportErrorTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(500)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("inplay.json")));
    Mono<Boolean> cmsReactiveFlag = cmsReactiveServiceImpl.isInplaySport("bma", "56");
    StepVerifier.create(cmsReactiveFlag).expectError().verify();
  }

  @AfterEach
  public void tearDown() throws IOException {
    mockWebServer.shutdown();
  }

  protected String getResourceFileAsString(String resourceFileName) {
    InputStream is = getClass().getClassLoader().getResourceAsStream(resourceFileName);
    BufferedReader reader = new BufferedReader(new InputStreamReader(is));
    return reader.lines().collect(Collectors.joining("\n"));
  }

  @Test
  void getIsCompetitionTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("competition.json")));
    Mono<Boolean> cmsReactiveFlag =
        cmsReactiveServiceImpl.isCompetition("bma", "world-cup", "highlights");
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertTrue(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getIsCompetitionEmptyTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(200)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("competition.json")));
    Mono<Boolean> cmsReactiveFlag =
        cmsReactiveServiceImpl.isCompetition("bma", "world-cup", "hlights");
    StepVerifier.create(cmsReactiveFlag)
        .assertNext(
            aBoolean -> {
              Assertions.assertFalse(aBoolean);
            })
        .expectComplete()
        .verify();
  }

  @Test
  void getIsCompetitionFalseTest() {
    mockWebServer.enqueue(
        new MockResponse()
            .setResponseCode(500)
            .setHeader(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
            .setBody(this.getResourceFileAsString("competition.json")));
    Mono<Boolean> cmsReactiveFlag =
        cmsReactiveServiceImpl.isCompetition("bma", "world-cup", "highlights");
    StepVerifier.create(cmsReactiveFlag).expectError().verify();
  }
}
