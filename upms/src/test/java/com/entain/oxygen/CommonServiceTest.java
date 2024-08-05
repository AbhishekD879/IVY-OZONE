package com.entain.oxygen;

import com.entain.oxygen.service.CommonService;
import java.lang.reflect.InvocationTargetException;
import java.lang.reflect.Method;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.web.reactive.function.server.ServerResponse;
import reactor.core.publisher.Mono;
import reactor.test.StepVerifier;

class CommonServiceTest {

  private CommonService commonService;

  @BeforeEach
  public void init() {
    commonService = new CommonService();
  }

  @Test
  void testServerResponse()
      throws NoSuchMethodException, InvocationTargetException, IllegalAccessException {

    String text = "test response";

    Method method =
        commonService.getClass().getDeclaredMethod("success", Object.class, boolean.class);

    method.setAccessible(true);

    Mono<ServerResponse> responseMono =
        (Mono<ServerResponse>) method.invoke(commonService, text, false);

    Assertions.assertNotNull(responseMono);

    StepVerifier.create(responseMono).expectNextCount(1).expectComplete().verify();
  }
}
