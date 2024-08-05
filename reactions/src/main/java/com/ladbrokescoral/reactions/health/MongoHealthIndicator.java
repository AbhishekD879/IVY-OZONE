package com.ladbrokescoral.reactions.health;

import static com.ladbrokescoral.reactions.util.ReactionHelper.*;
import static org.springframework.boot.actuate.health.Status.DOWN;
import static org.springframework.boot.actuate.health.Status.UP;

import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.actuate.health.AbstractReactiveHealthIndicator;
import org.springframework.boot.actuate.health.Health;
import org.springframework.data.mongodb.core.ReactiveMongoTemplate;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

/**
 * @author PBalarangakumar 23-06-2023
 */
@Slf4j
@Component
public class MongoHealthIndicator extends AbstractReactiveHealthIndicator {

  private final ReactiveMongoTemplate reactiveMongoTemplate;

  public MongoHealthIndicator(final ReactiveMongoTemplate reactiveMongoTemplate) {
    this.reactiveMongoTemplate = reactiveMongoTemplate;
  }

  @Override
  protected Mono<Health> doHealthCheck(Health.Builder healthBuilder) {
    final long startTime = System.currentTimeMillis();

    return reactiveMongoTemplate
        .executeCommand("{ buildInfo: 1 }")
        .map(
            document ->
                healthBuilder
                    .status(UP)
                    .withDetail(ADDITIONAL_STATUS, HealthStatus.HEALTHY.name())
                    .withDetail(MESSAGE, trace("Successfully connected to Mongo."))
                    .withDetail(PING, System.currentTimeMillis() - startTime)
                    .build())
        .switchIfEmpty(
            Mono.just(
                healthBuilder
                    .status(DOWN)
                    .withDetail(ADDITIONAL_STATUS, HealthStatus.UNHEALTHY.name())
                    .withDetail(MESSAGE, trace("Unable to connect Mongo."))
                    .withDetail(PING, System.currentTimeMillis() - startTime)
                    .build()))
        .onErrorResume(
            exception ->
                Mono.just(
                    healthBuilder
                        .status(DOWN)
                        .withDetail(ADDITIONAL_STATUS, HealthStatus.NO_CONNECTION.name())
                        .withDetail(MESSAGE, error("Could not ping Mongo.", exception.getMessage()))
                        .withDetail(PING, System.currentTimeMillis() - startTime)
                        .build()));
  }
}
