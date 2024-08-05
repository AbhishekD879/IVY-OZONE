package com.entain.oxygen;

import com.entain.oxygen.router.OptionsHandler;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.http.HttpMethod;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

class OptionsHandlerTest {

  private OptionsHandler optionsHandler;

  @BeforeEach
  public void init() {
    optionsHandler = new OptionsHandler();
  }

  @Test
  void testForOptionsHandlerTest() {

    Mono<ServerResponse> responseMono = optionsHandler.handle(HttpMethod.OPTIONS);

    Assertions.assertNotNull(responseMono);

    StepVerifier.create(responseMono).expectNextCount(1).expectComplete().verify();
  }
}
