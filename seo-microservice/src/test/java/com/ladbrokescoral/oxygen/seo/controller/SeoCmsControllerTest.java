package com.ladbrokescoral.oxygen.seo.controller;

import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.seo.cms.service.CmsReactiveService;
import com.ladbrokescoral.oxygen.seo.siteserver.service.SeoSiteServerService;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.reactive.WebFluxTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.MediaType;
import org.springframework.test.web.reactive.server.WebTestClient;
import reactor.core.publisher.Mono;

@ExtendWith(MockitoExtension.class)
@WebFluxTest(controllers = SeoCmsController.class)
class SeoCmsControllerTest {
  @MockBean CmsReactiveService cmsReactiveService;
  @MockBean SeoSiteServerService seoSiteServerService;
  @Autowired WebTestClient webTestClient;

  @Test
  void TestgetInplaySport() {
    when(cmsReactiveService.isInplaySport("ladbrokes", "horse-racing"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/in-play/horse-racing")
        .header("userAgent", "googlebot")
        .header("brand", "ladbrokes")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void TestgetInplaySportfalse() {
    when(cmsReactiveService.isInplaySport("ladbrokes", "horse-racing"))
        .thenReturn(Mono.just(Boolean.FALSE));
    this.webTestClient
        .get()
        .uri("/in-play/horse-racing")
        .header("userAgent", "")
        .header("brand", "ladbrokes")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void TestgetFanzones() {
    when(cmsReactiveService.isFanzone("boat", "AstonVilla", "now-next"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/fanzone/sport-football/AstonVilla/now-next")
        .header("userAgent", "googlebot")
        .header("brand", "ladbrokes")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void getFanzonesFalseTest() {
    when(cmsReactiveService.isFanzone("boat", "AstonVilla", "now-next"))
        .thenReturn(Mono.just(Boolean.FALSE));
    this.webTestClient
        .get()
        .uri("/fanzone/sport-football/AstonVilla/now-next")
        .header("userAgent", "")
        .header("brand", "ladbrokes")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void getSportTabTest() {
    when(cmsReactiveService.isSportTab("boat", "AstonVilla", "now-next", "future", "desktop"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/sport/football/matches/future")
        .header("userAgent", "googlebot")
        .header("brand", "ladbrokes")
        .header("deviceType", "android")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void getSportTabFalseTest() {
    when(cmsReactiveService.isSportTab("boat", "AstonVilla", "now-next", "future", "desktop"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/sport/football/matches/future")
        .header("userAgent", "")
        .header("brand", "ladbrokes")
        .header("deviceType", "android")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void getVirtualSportTest() {
    when(cmsReactiveService.isVirtualSport(
            "boat", "horse-racing", "horse-racing-flat", "237945501"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/virtual-sports/football/euro-cup")
        .header("userAgent", "googlebot")
        .header("brand", "ladbrokes")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void TestgetVirtualSportFalse() {
    when(cmsReactiveService.isVirtualSport(
            "boat", "horse-racing", "horse-racing-flat", "237945501"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/virtual-sports/football/euro-cup")
        .header("userAgent", "")
        .header("brand", "ladbrokes")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void TestgetPromotion() {
    when(cmsReactiveService.isPromotion("boat", "27")).thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/promotions/details/1-2-FREE")
        .header("userAgent", "googlebot")
        .header("brand", "ladbrokes")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void TestgetPromotionFalse() {
    when(cmsReactiveService.isPromotion("boat", "27")).thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/promotions/details/1-2-FREE")
        .header("userAgent", "")
        .header("brand", "ladbrokes")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void TestgetEventHubData() {
    when(cmsReactiveService.isEventHubData("boat", "AstonVilla", 4))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/home/eventhub/4")
        .header("userAgent", "googlebot")
        .header("brand", "ladbrokes")
        .header("deviceType", "android")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void TestgetEventHubDataFalse() {
    when(cmsReactiveService.isEventHubData("boat", "AstonVilla", 4))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/home/eventhub/4")
        .header("userAgent", "")
        .header("brand", "ladbrokes")
        .header("deviceType", "android")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void getSportNameTest() {
    when(cmsReactiveService.isSportName("boat", "AstonVilla", "desktop"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/sport/football")
        .header("userAgent", "googlebot")
        .header("brand", "ladbrokes")
        .header("deviceType", "android")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void getSportNameTestFalse() {
    when(cmsReactiveService.isSportName("boat", "AstonVilla", "desktop"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/sport/football")
        .header("userAgent", "")
        .header("brand", "ladbrokes")
        .header("deviceType", "android")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void getCompetitionByBrandAndUriTest() {
    when(cmsReactiveService.isCompetition("boat", "AstonVilla", "desktop"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/big-competition/world-cup/results")
        .header("userAgent", "googlebot")
        .header("brand", "ladbrokes")
        .header("deviceType", "android")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void getCompetitionByBrandAndUriFalse() {
    when(cmsReactiveService.isCompetition("ladbrokes", "AstonVilla", "desktop"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/big-competition/world-cup/results")
        .header("userAgent", "")
        .header("brand", "ladbrokes")
        .header("deviceType", "android")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }
}
