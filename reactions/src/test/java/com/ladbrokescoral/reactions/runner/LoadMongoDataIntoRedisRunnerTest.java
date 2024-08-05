package com.ladbrokescoral.reactions.runner;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.*;
import static org.mockito.Mockito.mock;

import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import com.ladbrokescoral.reactions.client.bpp.dto.BppTokenRequest;
import com.ladbrokescoral.reactions.client.bpp.dto.UserData;
import com.ladbrokescoral.reactions.exception.ServiceExecutionException;
import com.ladbrokescoral.reactions.scheduler.ReactionsCleanupScheduledTask;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.springframework.boot.ApplicationArguments;
import reactor.core.publisher.Mono;

class LoadMongoDataIntoRedisRunnerTest {
  private LoadMongoDataIntoRedisRunner runner;
  private MasterSlaveExecutor masterSlaveMock;

  @BeforeEach
  void setUp() {
    masterSlaveMock = mock(MasterSlaveExecutor.class);
    runner =
        new LoadMongoDataIntoRedisRunner(
            mock(ReactionsCleanupScheduledTask.class), this.masterSlaveMock);
  }

  @Test
  void testProcess() {
    ApplicationArguments args = mock(ApplicationArguments.class);
    MasterSlaveExecutor executor = (runnable, runnable1) -> runnable.run();
    LoadMongoDataIntoRedisRunner localTask =
        new LoadMongoDataIntoRedisRunner(mock(ReactionsCleanupScheduledTask.class), executor);
    assertThrows(ServiceExecutionException.class, () -> localTask.run(args));
  }

  @Test
  void testProcess1() {
    ReactionsCleanupScheduledTask reactionsCleanupScheduledTask =
        mock(ReactionsCleanupScheduledTask.class);
    ApplicationArguments args = mock(ApplicationArguments.class);
    MasterSlaveExecutor executor = (runnable, runnable1) -> runnable.run();
    LoadMongoDataIntoRedisRunner localTask =
        new LoadMongoDataIntoRedisRunner(reactionsCleanupScheduledTask, executor);
    when(reactionsCleanupScheduledTask.cleanupProcess()).thenReturn(Mono.just(true));
    localTask.run(args);
    UserData userData = new UserData("test", "test", true);
    BppTokenRequest bppTokenRequest = new BppTokenRequest("test");
    verify(reactionsCleanupScheduledTask).cleanupProcess();
  }

  @Test
  void testProcess2() {
    ReactionsCleanupScheduledTask reactionsCleanupScheduledTask =
        mock(ReactionsCleanupScheduledTask.class);
    ApplicationArguments args = mock(ApplicationArguments.class);
    MasterSlaveExecutor executor = (runnable, runnable1) -> runnable1.run();
    LoadMongoDataIntoRedisRunner localTask =
        new LoadMongoDataIntoRedisRunner(reactionsCleanupScheduledTask, executor);
    localTask.run(args);
    verify(reactionsCleanupScheduledTask, times(0)).cleanupProcess();
  }
}
