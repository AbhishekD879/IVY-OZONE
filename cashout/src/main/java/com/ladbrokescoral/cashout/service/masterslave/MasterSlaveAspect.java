package com.ladbrokescoral.cashout.service.masterslave;

import lombok.RequiredArgsConstructor;
import lombok.SneakyThrows;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.aspectj.lang.ProceedingJoinPoint;
import org.aspectj.lang.annotation.Around;
import org.aspectj.lang.annotation.Aspect;
import org.springframework.stereotype.Component;

@Aspect
@Component
@RequiredArgsConstructor
public class MasterSlaveAspect {
  private final MasterSlave masterSlave;
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  @SneakyThrows
  @Around("@annotation(com.ladbrokescoral.cashout.service.masterslave.ExecuteOnMaster)")
  public void executeIfMasterInstance(ProceedingJoinPoint proceedingJoinPoint) {
    if (masterSlave.isMaster()) {
      proceedingJoinPoint.proceed();
    } else {
      ASYNC_LOGGER.debug("Instance not master, not proceeding with {}", proceedingJoinPoint);
    }
  }
}
