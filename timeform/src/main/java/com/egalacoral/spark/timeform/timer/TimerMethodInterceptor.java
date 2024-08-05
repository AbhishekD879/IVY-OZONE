package com.egalacoral.spark.timeform.timer;

import etm.core.monitor.EtmPoint;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.Signature;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Pointcut;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Aspect
@Component
public class TimerMethodInterceptor {

  @Autowired private TimerService timerService;

  @Pointcut(value = "execution(public * *(..))")
  public void anyPublicMethod() {}

  @Around("anyPublicMethod() && @annotation(logAction)")
  public Object logAction(ProceedingJoinPoint pjp, Timer logAction) throws Throwable {

    Signature signature = pjp.getSignature();

    StringBuilder stringBuilder = new StringBuilder();
    stringBuilder.append(signature.getDeclaringTypeName());
    stringBuilder.append(".");
    stringBuilder.append(signature.getName());
    EtmPoint perfPoint = timerService.createPoint(stringBuilder.toString());
    Object proceed = null;
    try {
      proceed = pjp.proceed();
    } finally {
      timerService.submit(perfPoint);
    }
    return proceed;
  }
}
