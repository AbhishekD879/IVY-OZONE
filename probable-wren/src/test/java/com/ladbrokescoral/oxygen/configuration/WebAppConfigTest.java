package com.ladbrokescoral.oxygen.configuration;

import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.reactive.WebFluxTest;
import org.springframework.context.annotation.Import;
import org.springframework.test.web.reactive.server.WebTestClient;

@WebFluxTest
@Import(WebAppConfig.class)
@ExtendWith(MockitoExtension.class)
public class WebAppConfigTest {

  @Autowired private WebTestClient webTestClient;

  @Test
  public void swaggerRouterTest() {
    this.webTestClient.get().uri("/").exchange().expectStatus().isTemporaryRedirect();
  }

  @Test
  public void healthRouterTest() {
    this.webTestClient.get().uri("/health").exchange().expectStatus().isTemporaryRedirect();
  }

  @Test
  public void infoRouterTest() {
    this.webTestClient.get().uri("/info").exchange().expectStatus().isTemporaryRedirect();
  }
}
