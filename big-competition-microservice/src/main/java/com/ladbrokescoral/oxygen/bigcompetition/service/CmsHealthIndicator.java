package com.ladbrokescoral.oxygen.bigcompetition.service;

import com.fasterxml.jackson.databind.JsonNode;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.actuate.health.AbstractHealthIndicator;
import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.Status;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Component;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;

// @Slf4j
@Component
public class CmsHealthIndicator extends AbstractHealthIndicator {

  private final String cmsEndpoint;
  private final RestTemplate restTemplate;

  public CmsHealthIndicator(@Value("${cms.base.url}") String cmsEndpoint) {
    this.cmsEndpoint = cmsEndpoint;
    this.restTemplate = new RestTemplate();
  }

  @Override
  protected void doHealthCheck(Health.Builder builder) throws Exception {
    try {
      final ResponseEntity<JsonNode> entity =
          restTemplate.getForEntity(this.cmsEndpoint + "health", JsonNode.class);
      if (entity.getStatusCode().isError()) {
        builder.down().withDetail(this.cmsEndpoint, Status.DOWN);
      }
      if ("UP".equalsIgnoreCase(entity.getBody().get("status").asText())) {
        builder.up().withDetail(this.cmsEndpoint, Status.UP);
      } else {
        builder.down().withDetail(this.cmsEndpoint, Status.UNKNOWN);
      }
    } catch (RestClientException restClientException) {
      builder.down().withDetail(this.cmsEndpoint, Status.OUT_OF_SERVICE);
    }
  }
}
