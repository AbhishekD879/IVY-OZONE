package com.ladbrokescoral.oxygen.questionengine.aspect;

import com.newrelic.api.agent.NewRelic;
import lombok.RequiredArgsConstructor;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

@Aspect
@Component
@RequiredArgsConstructor
public class TraceAspect {

  @Around("@annotation(com.newrelic.api.agent.Trace)")
  public Object setNewRelicTransactionName(ProceedingJoinPoint proceedingJoinPoint) throws Throwable {
    NewRelic.setTransactionName(null, proceedingJoinPoint.getTarget().getClass().getSimpleName() + "#" + proceedingJoinPoint.getSignature().getName());

    return proceedingJoinPoint.proceed(proceedingJoinPoint.getArgs());
  }
}
