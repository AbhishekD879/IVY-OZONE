package com.ladbrokescoral.oxygen.seo.controller;

import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.seo.dto.ContestRequest;
import com.ladbrokescoral.oxygen.seo.showdown.service.ShowdownReactiveService;
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
@WebFluxTest(controllers = SeoShowdownController.class)
class SeoShowdownControllerTest {

  @MockBean ShowdownReactiveService showdownReactiveService;
  @Autowired WebTestClient webTestClient;

  @Test
  void getContestInfoTest() {
    ContestRequest contestRequest = new ContestRequest();
    contestRequest.setContestId("test");
    contestRequest.setEventId("237945501");
    contestRequest.setBrand("boat");
    contestRequest.setUserId("test123");
    contestRequest.setToken("test");
    when(showdownReactiveService.getContestInfo("YUhSR0FsQWd2OHFpSmFtK2xqNmE3Zz09"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/5-a-side/leaderboard/YUhSR0FsQWd2OHFpSmFtK2xqNmE3Zz09")
        .header("userAgent", "googlebot")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }

  @Test
  void getContestInfoFalseTest() {
    ContestRequest contestRequest = new ContestRequest();
    contestRequest.setContestId("test");
    contestRequest.setEventId("237945501");
    contestRequest.setBrand("boat");
    contestRequest.setUserId("test123");
    contestRequest.setToken("test");
    when(showdownReactiveService.getContestInfo("YUhSR0FsQWd2OHFpSmFtK2xqNmE3Zz09"))
        .thenReturn(Mono.just(Boolean.TRUE));
    this.webTestClient
        .get()
        .uri("/5-a-side/leaderboard/YUhSR0FsQWd2OHFpSmFtK2xqNmE3Zz09")
        .header("userAgent", "")
        .accept(MediaType.APPLICATION_JSON)
        .exchange()
        .expectStatus()
        .isOk();
  }
}
