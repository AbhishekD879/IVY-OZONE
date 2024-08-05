package com.ladbrokescoral.oxygen.buildyourbetms.util;

import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.boot.autoconfigure.condition.ConditionalOnProperty;
import org.springframework.stereotype.Component;

@Aspect
@Component
@ConditionalOnProperty(name = "byb.log.execution.time.enabled", havingValue = "true")
public class LogExecutionTimeAspect {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @Around("@annotation(LogExecutionTime)")
  public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
    final long start = System.currentTimeMillis();

    final Object proceed = joinPoint.proceed();

    final long executionTime = System.currentTimeMillis() - start;

    ASYNC_LOGGER.info(
        "Class Name: {}. Method Name: {}. Time taken for execution is: {}ms",
        joinPoint.getSignature().getDeclaringTypeName(),
        joinPoint.getSignature().getName(),
        executionTime);

    return proceed;
  }
}
