package com.entain.oxygen.betbuilder_middleware.config;

import com.fasterxml.jackson.core.JsonProcessingException;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.Signature;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
class LoggingTest {

  private Logging loggingMock = new Logging();

  @Mock private JoinPoint joinPoint;

  @Mock private Signature signature;

  @BeforeEach
  public void init() {
    Mockito.when(joinPoint.getSignature()).thenReturn(signature);
    Mockito.when(joinPoint.getSignature().getName()).thenReturn("TESTMETHOD");
    Mockito.when(joinPoint.getArgs()).thenReturn(null);
    Mockito.when(joinPoint.getSignature().getDeclaringTypeName()).thenReturn("TESTCLASS");
  }

  @Test
  void testLogBefore() {
    loggingMock.logBefore(joinPoint);
    Assertions.assertNotNull(loggingMock);
  }

  @Test
  void testMainPointcut() {
    loggingMock.mainPointcut();
    Assertions.assertNotNull(loggingMock);
  }

  @Test
  void testAnyHandlerMethod() {
    loggingMock.anyApiMethod();
    Assertions.assertNotNull(loggingMock);
  }

  @Test
  void testAnyRouterConfigMethod() {
    loggingMock.anyRedissonMethod();
    Assertions.assertNotNull(loggingMock);
  }

  @Test
  void testAnyServiceMethod() {
    loggingMock.anyServiceMethod();
    Assertions.assertNotNull(loggingMock);
  }

  @Test
  void testLogAfter() throws JsonProcessingException {
    Object result = "RESULT";
    loggingMock.logAfter(joinPoint, result);
    Assertions.assertNotNull(loggingMock);
  }

  @Test
  void testLogAfterWithoutResult() throws JsonProcessingException {
    loggingMock.logAfter(joinPoint, null);
    Assertions.assertNotNull(loggingMock);
  }
}
