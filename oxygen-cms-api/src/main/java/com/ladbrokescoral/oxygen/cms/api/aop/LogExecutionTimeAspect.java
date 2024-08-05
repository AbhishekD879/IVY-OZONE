package com.ladbrokescoral.oxygen.cms.api.aop;

import lombok.extern.slf4j.Slf4j;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

@Aspect
@Component
@Slf4j
public class LogExecutionTimeAspect {

  @Around("@annotation(com.ladbrokescoral.oxygen.cms.api.aop.LogExecutionTime)")
  public Object logExecutionTime(ProceedingJoinPoint joinPoint) throws Throwable {
    final long start = System.currentTimeMillis();

    final Object proceed = joinPoint.proceed();

    final long executionTime = System.currentTimeMillis() - start;

    log.info("{} executed in {} ms", joinPoint.getSignature(), executionTime);

    return proceed;
  }
}
