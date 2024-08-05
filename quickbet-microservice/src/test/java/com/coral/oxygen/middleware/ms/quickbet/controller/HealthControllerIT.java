package com.coral.oxygen.middleware.ms.quickbet.controller;

import static org.assertj.core.api.Assertions.assertThat;

import com.coral.oxygen.middleware.ms.quickbet.impl.IntegrationTest;
import org.junit.jupiter.api.Test;
import org.springframework.boot.web.server.LocalServerPort;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.client.RestTemplate;

@IntegrationTest
class HealthControllerIT {

  @LocalServerPort private int port;

  private RestTemplate restTemplate = new RestTemplate();

  @Test
  void shouldReturnOKIfAppIsRunning() {
    ResponseEntity<String> response =
        restTemplate.getForEntity("http://localhost:" + port + "/health", String.class);
    assertThat(response.getStatusCode()).isEqualTo(HttpStatus.OK);
    assertThat(response.getBody()).isEqualTo("Health check status");
  }
}
