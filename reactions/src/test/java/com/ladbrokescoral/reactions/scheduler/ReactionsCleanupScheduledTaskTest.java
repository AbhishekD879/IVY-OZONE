package com.ladbrokescoral.reactions.scheduler;

import static org.junit.jupiter.api.Assertions.assertThrows;
import static org.mockito.Mockito.*;

import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import com.ladbrokescoral.reactions.client.cms.CMSClient;
import com.ladbrokescoral.reactions.config.ReactionPropertiesConfig;
import com.ladbrokescoral.reactions.exception.ServiceExecutionException;
import com.ladbrokescoral.reactions.repository.redis.RedisOperations;
import com.ladbrokescoral.reactions.repository.redis.RedisReactionRepository;
import com.ladbrokescoral.reactions.service.DefaultMongoReactionService;
import com.ladbrokescoral.reactions.service.ReactionService;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Collections;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.InjectMocks;
import org.mockito.MockitoAnnotations;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

class ReactionsCleanupScheduledTaskTest {

  @InjectMocks private ReactionsCleanupScheduledTask task;
  private CMSClient cmsClient = mock(CMSClient.class);

  private DefaultMongoReactionService mongoReactionService =
      mock(DefaultMongoReactionService.class);

  private RedisOperations redisOperations = mock(RedisOperations.class);

  private RedisReactionRepository redisReactionRepository = mock(RedisReactionRepository.class);

  private ReactionService reactionService = mock(ReactionService.class);

  private ReactionPropertiesConfig reactionPropertiesConfig = mock(ReactionPropertiesConfig.class);
  private MasterSlaveExecutor masterSlaveMock;

  @BeforeEach
  void setUp() {
    masterSlaveMock = mock(MasterSlaveExecutor.class);
    task =
        new ReactionsCleanupScheduledTask(
            cmsClient,
            mongoReactionService,
            redisOperations,
            redisReactionRepository,
            reactionService,
            reactionPropertiesConfig,
            this.masterSlaveMock);
    MockitoAnnotations.openMocks(this);
  }

  @Test
  void testCleanupProcess() throws Exception {
    MasterSlaveExecutor executor = (runnable, runnable1) -> runnable.run();
    ReactionsCleanupScheduledTask localTask =
        new ReactionsCleanupScheduledTask(
            cmsClient,
            mongoReactionService,
            redisOperations,
            redisReactionRepository,
            reactionService,
            reactionPropertiesConfig,
            executor);
    MockitoAnnotations.openMocks(this);
    assertThrows(ServiceExecutionException.class, () -> localTask.process());
  }

  @Test
  void testCleanupProcess1() throws Exception {
    MasterSlaveExecutor executor = (runnable, runnable1) -> runnable1.run();
    ReactionsCleanupScheduledTask localTask =
        new ReactionsCleanupScheduledTask(
            cmsClient,
            mongoReactionService,
            redisOperations,
            redisReactionRepository,
            reactionService,
            reactionPropertiesConfig,
            executor);
    MockitoAnnotations.openMocks(this);
    localTask.process();
    verify(mongoReactionService, times(0)).getAllUserDeleteKeys();
  }

  @Test
  void testCleanupProcess2() throws Exception {
    MasterSlaveExecutor executor = (runnable, runnable1) -> runnable.run();
    ReactionsCleanupScheduledTask localTask =
        new ReactionsCleanupScheduledTask(
            cmsClient,
            mongoReactionService,
            redisOperations,
            redisReactionRepository,
            reactionService,
            reactionPropertiesConfig,
            executor);
    MockitoAnnotations.openMocks(this);
    when(reactionPropertiesConfig.getBatchSize()).thenReturn(2);
    when(mongoReactionService.getAllUserDeleteKeys()).thenReturn(Flux.just("1"));
    when(reactionService.collectGlobalCountFromMongo())
        .thenReturn(Mono.just(Collections.singletonMap("key", 123L)));
    when(cmsClient.getActiveSelectionIdAndSurfaceBetIdKeys())
        .thenReturn(Mono.just(Arrays.asList("1")));
    when(mongoReactionService.getUsersCount()).thenReturn(Mono.just(10L));
    when(mongoReactionService.deleteUsers(any())).thenReturn(Mono.empty());
    when(mongoReactionService.findAllPaginatedUsers(any())).thenReturn(Mono.empty());
    when(redisOperations.cleanUpAllRedisKeys()).thenReturn(Mono.empty());
    when(task.loadMongoDataToRedis()).thenReturn(Mono.empty());
    localTask.process();
    verify(mongoReactionService, times(1)).getAllUserDeleteKeys();
  }

  @Test
  void testCleanupProcess3() throws Exception {
    MasterSlaveExecutor executor = (runnable, runnable1) -> runnable.run();
    ReactionsCleanupScheduledTask localTask =
        new ReactionsCleanupScheduledTask(
            cmsClient,
            mongoReactionService,
            redisOperations,
            redisReactionRepository,
            reactionService,
            reactionPropertiesConfig,
            executor);
    MockitoAnnotations.openMocks(this);
    when(reactionPropertiesConfig.getBatchSize()).thenReturn(2);
    when(mongoReactionService.getAllUserDeleteKeys()).thenReturn(Flux.just("1"));
    when(reactionService.collectGlobalCountFromMongo())
        .thenReturn(Mono.just(Collections.singletonMap("key", 123L)));
    when(cmsClient.getActiveSelectionIdAndSurfaceBetIdKeys())
        .thenReturn(Mono.just(Arrays.asList("1")));
    when(mongoReactionService.getUsersCount()).thenReturn(Mono.just(10L));
    when(mongoReactionService.deleteUsers(any())).thenReturn(Mono.empty());
    when(mongoReactionService.findAllPaginatedUsers(any()))
        .thenReturn(Mono.error(IllegalArgumentException::new));
    when(redisOperations.cleanUpAllRedisKeys()).thenReturn(Mono.empty());
    when(task.loadMongoDataToRedis()).thenReturn(Mono.empty());
    localTask.process();
    verify(mongoReactionService, times(1)).getAllUserDeleteKeys();
    when(mongoReactionService.findAllPaginatedUsers(any())).thenReturn(Mono.error(Exception::new));
    assertThrows(ServiceExecutionException.class, () -> localTask.process());
    when(reactionPropertiesConfig.getBatchSize()).thenReturn(3);
    assertThrows(ServiceExecutionException.class, () -> localTask.process());
    when(cmsClient.getActiveSelectionIdAndSurfaceBetIdKeys())
        .thenReturn(Mono.just(new ArrayList<>()));
    assertThrows(ServiceExecutionException.class, () -> localTask.process());
  }
}
