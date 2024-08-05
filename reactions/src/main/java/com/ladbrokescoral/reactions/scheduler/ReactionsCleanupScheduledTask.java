package com.ladbrokescoral.reactions.scheduler;

import static com.ladbrokescoral.reactions.util.ReactionHelper.NO_OF_RETRIES;

import com.ladbrokescoral.lib.masterslave.executor.MasterSlaveExecutor;
import com.ladbrokescoral.reactions.client.cms.CMSClient;
import com.ladbrokescoral.reactions.config.ReactionPropertiesConfig;
import com.ladbrokescoral.reactions.exception.ServiceExecutionException;
import com.ladbrokescoral.reactions.repository.redis.RedisOperations;
import com.ladbrokescoral.reactions.repository.redis.RedisReactionRepository;
import com.ladbrokescoral.reactions.service.DefaultMongoReactionService;
import com.ladbrokescoral.reactions.service.ReactionService;
import lombok.extern.slf4j.Slf4j;
import org.springframework.data.domain.PageRequest;
import org.springframework.scheduling.annotation.Scheduled;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;

/**
 * @author PBalarangakumar 21-06-2023
 */
@Slf4j
@Component
@SuppressWarnings("java:S2142")
public class ReactionsCleanupScheduledTask {

  private final CMSClient cmsClient;
  private final DefaultMongoReactionService mongoReactionService;
  private final RedisOperations redisOperations;
  private final RedisReactionRepository redisReactionRepository;
  private final ReactionService reactionService;

  private final ReactionPropertiesConfig reactionPropertiesConfig;

  private final MasterSlaveExecutor masterSlaveExecutor;

  public ReactionsCleanupScheduledTask(
      final CMSClient cmsClient,
      final DefaultMongoReactionService mongoReactionService,
      final RedisOperations redisOperations,
      final RedisReactionRepository redisReactionRepository,
      final ReactionService reactionService,
      final ReactionPropertiesConfig reactionPropertiesConfig,
      final MasterSlaveExecutor masterSlaveExecutor) {

    this.cmsClient = cmsClient;
    this.mongoReactionService = mongoReactionService;
    this.redisOperations = redisOperations;
    this.redisReactionRepository = redisReactionRepository;
    this.reactionService = reactionService;
    this.reactionPropertiesConfig = reactionPropertiesConfig;
    this.masterSlaveExecutor = masterSlaveExecutor;
  }

  @Scheduled(cron = "${reactions.cron.expression}", zone = "${reactions.time.zone}")
  public void process() {

    masterSlaveExecutor.executeIfMaster(
        () -> {
          try {
            log.info("Mongo Cleanup & Redis Reload scheduler Job started.");
            cleanupProcess().retry(NO_OF_RETRIES).toFuture().get();
          } catch (final Exception ex) {
            throw new ServiceExecutionException(
                "Mongo Cleanup & Redis Reload scheduler job failed", ex);
          }
        },
        () -> log.info("SLAVE"));
  }

  public Mono<Boolean> cleanupProcess() {

    final long startTime = System.currentTimeMillis();

    return mongoReactionService
        .getAllUserDeleteKeys()
        .filterWhen(
            deleteKey ->
                cmsClient
                    .getActiveSelectionIdAndSurfaceBetIdKeys()
                    .flatMapMany(Flux::fromIterable)
                    .hasElement(deleteKey)
                    .map(response -> !response))
        .collectList()
        .flatMap(mongoReactionService::deleteUsers)
        .then(redisOperations.cleanUpAllRedisKeys())
        .then(loadMongoDataToRedis())
        .doOnSuccess(
            res ->
                log.info(
                    "Mongo Cleanup & Redis Reload Finished and the total execution time is: "
                        + (System.currentTimeMillis() - startTime)))
        .onErrorResume(
            (Throwable throwable) -> {
              final String errorMsg =
                  "Error while executing Mongo Cleanup & Redis Reload: " + throwable.getMessage();
              if (throwable instanceof IllegalArgumentException) {
                log.info(
                    "Mongo Cleanup & Redis Reload Finished and the total execution time is: "
                        + (System.currentTimeMillis() - startTime));
                return Mono.empty();
              }
              throw new ServiceExecutionException(errorMsg);
            })
        .doOnError(
            (Throwable throwable) -> {
              final String errorMsg =
                  "Error while executing Mongo Cleanup & Redis Reload: " + throwable.getMessage();
              log.error(errorMsg);

              throw new ServiceExecutionException(errorMsg);
            });
  }

  public Mono<Boolean> loadMongoDataToRedis() {

    final int max = reactionPropertiesConfig.getBatchSize();
    return mongoReactionService
        .getUsersCount()
        .flatMap(
            (Long count) -> {
              final int integerCount = count.intValue();
              final int iteration = (integerCount / max + (integerCount % max > 0 ? 1 : 0));
              return Flux.range(0, iteration)
                  .flatMap(
                      num ->
                          mongoReactionService
                              .findAllPaginatedUsers(PageRequest.of(num, max))
                              .flatMap(redisReactionRepository::saveMongoUserDataIntoRedis))
                  .collectList()
                  .map(res -> Boolean.TRUE);
            })
        .then(
            reactionService
                .collectGlobalCountFromMongo()
                .flatMap(redisReactionRepository::saveMongoGlobalCountDataIntoRedis));
  }
}
