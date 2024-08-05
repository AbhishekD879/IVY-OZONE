package com.ladbrokescoral.reactions.health;

import static com.ladbrokescoral.reactions.util.ReactionHelper.*;
import static org.springframework.boot.actuate.health.Status.DOWN;
import static org.springframework.boot.actuate.health.Status.UP;

import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.actuate.health.AbstractReactiveHealthIndicator;
import org.springframework.boot.actuate.health.Health;
import org.springframework.data.redis.connection.ReactiveRedisConnectionFactory;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Mono;

/**
 * @author PBalarangakumar 23-06-2023
 */
@Slf4j
@Component
public class RedisHealthIndicator extends AbstractReactiveHealthIndicator {

  private final ReactiveRedisConnectionFactory redisConnectionFactory;

  public RedisHealthIndicator(final ReactiveRedisConnectionFactory redisConnectionFactory) {
    this.redisConnectionFactory = redisConnectionFactory;
  }

  @Override
  protected Mono<Health> doHealthCheck(Health.Builder healthBuilder) {
    final long startTime = System.currentTimeMillis();

    return redisConnectionFactory
        .getReactiveConnection()
        .serverCommands()
        .info()
        .map(
            info ->
                healthBuilder
                    .status(UP)
                    .withDetail(ADDITIONAL_STATUS, HealthStatus.HEALTHY.name())
                    .withDetail(MESSAGE, trace("Successfully connected to Redis."))
                    .withDetail(PING, System.currentTimeMillis() - startTime)
                    .build())
        .switchIfEmpty(
            Mono.just(
                healthBuilder
                    .status(DOWN)
                    .withDetail(ADDITIONAL_STATUS, HealthStatus.UNHEALTHY.name())
                    .withDetail(MESSAGE, trace("Unable to connect Redis."))
                    .withDetail(PING, System.currentTimeMillis() - startTime)
                    .build()))
        .onErrorResume(
            exception ->
                Mono.just(
                    healthBuilder
                        .status(DOWN)
                        .withDetail(ADDITIONAL_STATUS, HealthStatus.NO_CONNECTION.name())
                        .withDetail(MESSAGE, error("Could not ping Redis.", exception.getMessage()))
                        .withDetail(PING, System.currentTimeMillis() - startTime)
                        .build()));
  }
}
