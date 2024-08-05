package com.entain.oxygen.betbuilder_middleware.config;

import com.fasterxml.jackson.core.JsonProcessingException;
import com.fasterxml.jackson.databind.ObjectMapper;
import java.util.Objects;
import org.aspectj.lang.JoinPoint;
import org.aspectj.lang.annotation.AfterReturning;
import org.aspectj.lang.annotation.Aspect;
import org.aspectj.lang.annotation.Before;
import org.aspectj.lang.annotation.Pointcut;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.boot.autoconfigure.condition.ConditionalOnExpression;
import org.springframework.stereotype.Component;

@Aspect
@Component
@ConditionalOnExpression("${centralised.logging:false}")
public class Logging {
  /*
   * Added AspectJ to log all classes in the packages that mentioned in below pointcuts as part of BYB
   * */
  private final Logger logger = LoggerFactory.getLogger(this.getClass());
  long time;
  String finalResult;

  ObjectMapper mapper = new ObjectMapper();

  @Pointcut("execution(* com.entain.oxygen.betbuilder_middleware.api.PriceApi..*(..))")
  public void anyApiMethod() {}

  @Pointcut("execution(* com.entain.oxygen.betbuilder_middleware.repository.*..*(..))")
  public void anyRedissonMethod() {}

  @Pointcut("execution(* com.entain.oxygen.betbuilder_middleware.service.*..*(..))")
  public void anyServiceMethod() {}

  @Pointcut("anyApiMethod() || anyServiceMethod() || anyRedissonMethod()")
  public void mainPointcut() {}

  @Before("mainPointcut()")
  public void logBefore(JoinPoint joinPoint) {
    time = System.currentTimeMillis();
    logger.info(
        "Entering method: {} with arguments: {} ,Class Name:{}",
        joinPoint.getSignature().getName(),
        joinPoint.getArgs(),
        joinPoint.getSignature().getDeclaringTypeName());
  }

  @AfterReturning(pointcut = "mainPointcut()", returning = "result")
  public void logAfter(JoinPoint joinPoint, Object result) throws JsonProcessingException {
    if (Objects.nonNull(result))
      finalResult = mapper.writerWithDefaultPrettyPrinter().writeValueAsString(result);
    logger.info(
        "Exiting method: {}, with result {} Class Name:{}",
        joinPoint.getSignature().getName(),
        finalResult,
        joinPoint.getSignature().getDeclaringTypeName());
    logger.info(
        "Total Time taken by the method: {} in className {} is {} milliseconds",
        joinPoint.getSignature().getName(),
        joinPoint.getSignature().getDeclaringTypeName(),
        System.currentTimeMillis() - time);
  }
}
