package com.ladbrokescoral.reactions.health;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;
import static org.springframework.boot.actuate.health.Status.UP;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.reactions.client.cms.CMSClient;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.Status;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

class CMSHealthIndicatorTest {

  @InjectMocks private CMSHealthIndicator cmsHealthIndicator;

  @Mock private CMSClient cmsClient;

  @BeforeEach
  public void setUp() {
    MockitoAnnotations.openMocks(this);
  }

  @Test
  void testDoHealthCheckWhenCMSIsUp() {
    JsonNode upResponse = createUpResponse();
    when(cmsClient.getCmsHealth()).thenReturn(Mono.just(upResponse));
    Mono<Health> healthMono = cmsHealthIndicator.doHealthCheck(Health.up());
    StepVerifier.create(healthMono)
        .expectNextMatches(
            health -> {
              assertEquals(
                  HealthStatus.HEALTHY.name(), health.getDetails().get("additionalStatus"));
              assertEquals("Successfully connected to CMS.", health.getDetails().get("message"));
              assertEquals(UP, health.getStatus());
              return true;
            })
        .expectComplete()
        .verify();
  }

  @Test
  void testDoHealthCheckWhenCMSIsDown() {
    JsonNode downResponse = createDownResponse();
    when(cmsClient.getCmsHealth()).thenReturn(Mono.just(downResponse));
    Mono<Health> healthMono = cmsHealthIndicator.doHealthCheck(Health.up());
    StepVerifier.create(healthMono)
        .expectNextMatches(
            health -> {
              assertEquals(
                  HealthStatus.UNHEALTHY.name(), health.getDetails().get("additionalStatus"));
              assertEquals("Unable to connect CMS.", health.getDetails().get("message"));
              assertEquals(Status.DOWN, health.getStatus());
              return true;
            })
        .expectComplete()
        .verify();
  }

  @Test
  void testDoHealthCheckWhenNoConnectionToCMS() {
    when(cmsClient.getCmsHealth())
        .thenReturn(
            Mono.error(new RuntimeException("Could not ping CMS. Error: Connection error")));
    Mono<Health> healthMono = cmsHealthIndicator.doHealthCheck(Health.up());
    StepVerifier.create(healthMono)
        .expectErrorMatches(
            error -> {
              assertEquals("Could not ping CMS. Error: Connection error", error.getMessage());
              return true;
            })
        .verify();
  }

  private JsonNode createUpResponse() {
    String upResponseJson =
        "{"
            + "\"status\": \"UP\","
            + "\"components\": {"
            + "\"CMS\": {"
            + "\"status\": \"UP\","
            + "\"details\": {"
            + "\"additionalStatus\": \"HEALTHY\","
            + "\"message\": \"Successfully connected to CMS.\","
            + "\"ping\": 38"
            + "}"
            + "}"
            + "}"
            + "}";

    try {
      ObjectMapper objectMapper = new ObjectMapper();
      return objectMapper.readTree(upResponseJson);
    } catch (Exception e) {
      throw new RuntimeException("Error parsing JSON response", e);
    }
  }

  private JsonNode createDownResponse() {
    String downResponseJson =
        "{"
            + "\"status\": \"DOWN\","
            + "\"components\": {"
            + "\"CMS\": {"
            + "\"status\": \"DOWN\","
            + "\"details\": {"
            + "\"additionalStatus\": \"UNHEALTHY\","
            + "\"message\": \"Unable to connect CMS.\","
            + "\"ping\": 0"
            + "}"
            + "}"
            + "}"
            + "}";

    try {
      ObjectMapper objectMapper = new ObjectMapper();
      return objectMapper.readTree(downResponseJson);
    } catch (Exception e) {
      throw new RuntimeException("Error parsing JSON response", e);
    }
  }
}
