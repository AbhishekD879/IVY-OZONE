package com.ladbrokescoral.oxygen.seo.controller;

import static org.mockito.Mockito.when;

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
@WebFluxTest(controllers = SeoSiteServerController.class)
class SeoSiteServerControllerTest {

  @MockBean SeoSiteServerService seoSiteServerService;
  @Autowired WebTestClient webTestClient;

  @Test
  void TestgetCompetitions() {
    when(seoSiteServerService.getCompetitionReactive("football", "international", "world-cup-2022"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/competitions/football/english/fa-cup")
        .header("userAgent", "googlebot")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void TestgetCompetitionsFalse() {
    when(seoSiteServerService.getCompetitionReactive("football", "international", "world-cup-2022"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/competitions/football/english/fa-cup")
        .header("userAgent", "")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void TestgetTierEdpEvent() {
    when(seoSiteServerService.getEventToOutcomeForEventReactive(
            "football",
            "international",
            "international-friendlies",
            "panama-v-saudi-arabia",
            "237766317",
            "all-markets",
            null,
            null))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri(
            "/event/football/international/international-friendlies/panama-v-saudi-arabia/237766317/all-markets")
        .header("userAgent", "googlebot")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .is2xxSuccessful();
  }

  @Test
  void TestgetTierEdpEventFalse() {
    when(seoSiteServerService.getEventToOutcomeForEventReactive(
            "football",
            "international",
            "international-friendlies",
            "panama-v-saudi-arabia",
            "237766317",
            "all-markets",
            null,
            null))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri(
            "/event/football/international/international-friendlies/panama-v-saudi-arabia/237766317/all-markets")
        .header("userAgent", "")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .is2xxSuccessful();
  }

  @Test
  void Testget5AsideEvent() {
    when(seoSiteServerService.get5ASideEvent(
            "football", "football-england", "fa-cup", "leeds-vs-cardiff", "238549826"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/event/football/football-england/fa-cup/leeds-vs-cardiff/238549826/5-a-side/pitch")
        .header("userAgent", "googlebot")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void Testget5AsideEventFalse() {
    when(seoSiteServerService.get5ASideEvent(
            "football", "football-england", "fa-cup", "leeds-vs-cardiff", "238549826"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/event/football/football-england/fa-cup/leeds-vs-cardiff/238549826/5-a-side/pitch")
        .header("userAgent", "")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void TestgetHRAndGHEdpEvents() {
    when(seoSiteServerService.getEventToOutcomeForEventReactive(
            "horse-racing",
            "horse-racing-live",
            "cagnes-sur",
            "4-places",
            "238170846",
            "win-or-each-way",
            null,
            null))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/horse-racing/horse-racing-live/kempton/16-20-kempton/237837292/win-or-each-way")
        .header("userAgent", "googlebot")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void TestgetHRAndGHEdpEventsFalse() {
    when(seoSiteServerService.getEventToOutcomeForEventReactive(
            "horse-racing",
            "horse-racing-live",
            "cagnes-sur",
            "4-places",
            "238170846",
            "win-or-each-way",
            null,
            null))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/horse-racing/horse-racing-live/kempton/16-20-kempton/237837292/win-or-each-way")
        .header("userAgent", "")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void TestgetLotto() {
    when(seoSiteServerService.getLotto("daily-millions")).thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/lotto/daily-millions")
        .header("userAgent", "googlebot")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .is2xxSuccessful();
  }

  @Test
  void TestgetLottoFalse() {
    when(seoSiteServerService.getLotto("daily-millions")).thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/lotto/daily-millions")
        .header("userAgent", "")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .is2xxSuccessful();
  }

  @Test
  void TestgetCoupons() {
    when(seoSiteServerService.getCoupons("football", "weekend-matches", "112"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/coupons/football/bankers-coupon/44")
        .header("userAgent", "googlebot")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void TestgetCouponsFalse() {
    when(seoSiteServerService.getCoupons("football", "weekend-matches", "112"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/coupons/football/bankers-coupon/44")
        .header("userAgent", "")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }
}
