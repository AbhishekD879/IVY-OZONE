package com.ladbrokescoral.reactions.health;

import static com.ladbrokescoral.reactions.util.ReactionHelper.*;
import static org.springframework.boot.actuate.health.Status.DOWN;
import static org.springframework.boot.actuate.health.Status.UP;

import com.fasterxml.jackson.databind.JsonNode;
import com.ladbrokescoral.reactions.client.cms.CMSClient;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.actuate.health.AbstractReactiveHealthIndicator;
import org.springframework.boot.actuate.health.Health;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

/**
 * @author PBalarangakumar 23-06-2023
 */
@Slf4j
@Component
public class CMSHealthIndicator extends AbstractReactiveHealthIndicator {

  private final CMSClient cmsClient;

  public CMSHealthIndicator(final CMSClient cmsClient) {
    this.cmsClient = cmsClient;
  }

  @Override
  protected Mono<Health> doHealthCheck(Health.Builder healthBuilder) {
    final long startTime = System.currentTimeMillis();

    return cmsClient
        .getCmsHealth()
        .map(
            (JsonNode jsonNode) -> {
              try {
                if (jsonNode.get(STATUS).asText().equalsIgnoreCase(UP_STATUS)) {
                  return healthBuilder
                      .status(UP)
                      .withDetail(ADDITIONAL_STATUS, HealthStatus.HEALTHY.name())
                      .withDetail(MESSAGE, trace("Successfully connected to CMS."))
                      .withDetail(PING, System.currentTimeMillis() - startTime)
                      .build();
                } else {
                  return healthBuilder
                      .status(DOWN)
                      .withDetail(ADDITIONAL_STATUS, HealthStatus.UNHEALTHY.name())
                      .withDetail(MESSAGE, trace("Unable to connect CMS."))
                      .withDetail(PING, System.currentTimeMillis() - startTime)
                      .build();
                }
              } catch (final RuntimeException exception) {
                return healthBuilder
                    .status(DOWN)
                    .withDetail(ADDITIONAL_STATUS, HealthStatus.NO_CONNECTION.name())
                    .withDetail(MESSAGE, error("Could not ping CMS.", exception.getMessage()))
                    .withDetail(PING, System.currentTimeMillis() - startTime)
                    .build();
              }
            });
  }
}
