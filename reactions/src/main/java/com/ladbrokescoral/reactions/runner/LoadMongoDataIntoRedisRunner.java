package com.ladbrokescoral.reactions.runner;

import static com.ladbrokescoral.reactions.util.ReactionHelper.NO_OF_RETRIES;

import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import com.ladbrokescoral.reactions.exception.ServiceExecutionException;
import com.ladbrokescoral.reactions.scheduler.ReactionsCleanupScheduledTask;
import lombok.extern.slf4j.Slf4j;
import org.springframework.boot.ApplicationArguments;
import org.springframework.boot.ApplicationRunner;
import org.springframework.stereotype.Component;

/**
 * @author PBalarangakumar 13-07-2023
 */
@Slf4j
@Component
@SuppressWarnings("java:S2142")
public class LoadMongoDataIntoRedisRunner implements ApplicationRunner {

  private final ReactionsCleanupScheduledTask reactionsCleanupScheduledTask;
  private final MasterSlaveExecutor masterSlaveExecutor;

  public LoadMongoDataIntoRedisRunner(
      final ReactionsCleanupScheduledTask reactionsCleanupScheduledTask,
      final MasterSlaveExecutor masterSlaveExecutor) {
    this.reactionsCleanupScheduledTask = reactionsCleanupScheduledTask;
    this.masterSlaveExecutor = masterSlaveExecutor;
  }

  public void run(ApplicationArguments args) {

    masterSlaveExecutor.executeIfMaster(
        () -> {
          try {
            log.info("Mongo Cleanup & Redis Reload started while server startup.");
            reactionsCleanupScheduledTask.cleanupProcess().retry(NO_OF_RETRIES).toFuture().get();
          } catch (final Exception ex) {
            throw new ServiceExecutionException(
                "Mongo Cleanup & Redis Reload failed while server startup.", ex);
          }
        },
        () -> log.info("SLAVE"));
  }
}
