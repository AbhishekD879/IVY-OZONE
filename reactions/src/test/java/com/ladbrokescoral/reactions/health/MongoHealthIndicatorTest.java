package com.ladbrokescoral.reactions.health;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;
import static org.springframework.boot.actuate.health.Status.DOWN;
import static org.springframework.boot.actuate.health.Status.UP;

import com.ladbrokescoral.reactions.exception.ServiceUnavailableException;
import com.mongodb.MongoException;
import org.bson.Document;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;
import org.springframework.boot.actuate.health.Health;
import org.springframework.boot.actuate.health.Status;
import org.springframework.data.mongodb.core.ReactiveMongoTemplate;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

class MongoHealthIndicatorTest {
  private ReactiveMongoTemplate reactiveMongoTemplate;
  private MongoHealthIndicator mongoHealthIndicator;

  @BeforeEach
  void setUp() {
    reactiveMongoTemplate = Mockito.mock(ReactiveMongoTemplate.class);
    mongoHealthIndicator = new MongoHealthIndicator(reactiveMongoTemplate);
  }

  @Test
  void testMongoIsUp() {
    when(reactiveMongoTemplate.executeCommand("{ buildInfo: 1 }"))
        .thenReturn(Mono.just(new Document("", "")));
    Health health = mongoHealthIndicator.health().block();
    assertEquals(UP, health.getStatus());
    assertEquals("HEALTHY", health.getDetails().get("additionalStatus"));
  }

  @Test
  void testMongoIsDown() {
    when(reactiveMongoTemplate.executeCommand("{ buildInfo: 1 }")).thenReturn(Mono.empty());
    Health health = mongoHealthIndicator.health().block();
    assertEquals(DOWN, health.getStatus());
    assertEquals("UNHEALTHY", health.getDetails().get("additionalStatus"));
  }

  @Test
  void testMongoError() {
    when(reactiveMongoTemplate.executeCommand("{ buildInfo: 1 }"))
        .thenThrow(new ServiceUnavailableException(""));
    Mono<Health> healthMono = mongoHealthIndicator.health();

    StepVerifier.create(healthMono)
        .expectNextMatches(health -> health.getStatus() == Status.DOWN)
        .verifyComplete();
  }

  @Test
  void testMongoErrorHandling() {
    when(reactiveMongoTemplate.executeCommand("{ buildInfo: 1 }"))
        .thenReturn(Mono.error(new RuntimeException("Connection error")));
    Mono<Health> healthMono =
        mongoHealthIndicator.doHealthCheck(Health.down(new MongoException("cghc")));
    StepVerifier.create(healthMono)
        .expectNextMatches(health -> health.getStatus() == Status.DOWN)
        .verifyComplete();
  }
}
