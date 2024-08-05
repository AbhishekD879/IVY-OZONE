package com.ladbrokescoral.oxygen.cms.api.scheduler;

import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import lombok.AllArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Component;

@Component
@AllArgsConstructor
@Slf4j
public class ScheduledTaskExecutor {
  private final MasterSlaveExecutor masterSlaveExecutor;

  public void execute(Runnable runnable) {
    try {
      masterSlaveExecutor.executeIfMaster(
          () -> {
            log.debug("Executing master job");
            runnable.run();
          },
          () -> log.debug("Slave"));
    } catch (Exception e) {
      log.error("Caught exception in masterSlaveExecutor", e);
    }
  }
}
