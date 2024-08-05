package com.ladbrokescoral.reactions.controller;

import static com.ladbrokescoral.reactions.util.ReactionHelper.*;

import com.ladbrokescoral.reactions.dto.SurfaceBetInfoRequestDTO;
import com.ladbrokescoral.reactions.dto.UserGlobalCountResponseDTO;
import com.ladbrokescoral.reactions.dto.UserReactionDTO;
import com.ladbrokescoral.reactions.exception.ServiceExecutionException;
import com.ladbrokescoral.reactions.repository.redis.RedisOperations;
import com.ladbrokescoral.reactions.scheduler.ReactionsCleanupScheduledTask;
import com.ladbrokescoral.reactions.service.ReactionService;
import io.swagger.v3.oas.annotations.Operation;
import java.util.List;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.bind.annotation.*;
import reactor.core.publisher.Mono;

/**
 * @author PBalarangakumar 14-06-2023
 */
@RestController
@RequestMapping("/reactions")
@Slf4j
public class ReactionController {

  private final ReactionService reactionService;
  private final ReactionsCleanupScheduledTask reactionsCleanupScheduledTask;
  private final RedisOperations redisOperations;

  public ReactionController(
      final ReactionService reactionService,
      final ReactionsCleanupScheduledTask reactionsCleanupScheduledTask,
      final RedisOperations redisOperations) {

    this.reactionService = reactionService;
    this.reactionsCleanupScheduledTask = reactionsCleanupScheduledTask;
    this.redisOperations = redisOperations;
  }

  @PostMapping
  public Mono<Boolean> saveReaction(
      @RequestHeader(value = TOKEN) final String token,
      @RequestHeader(value = USER_NAME) final String userName,
      @RequestBody final UserReactionDTO userReactionDTO) {

    return reactionService.saveReaction(token, userName, userReactionDTO);
  }

  @PutMapping
  public Mono<String> updateReaction(
      @RequestHeader(value = TOKEN) final String token,
      @RequestHeader(value = USER_NAME) final String userName,
      @RequestBody final UserReactionDTO userReactionDTO) {

    return reactionService.updateReaction(token, userName, userReactionDTO);
  }

  @PostMapping("/{custId}")
  public Mono<UserGlobalCountResponseDTO> getGlobalCount(
      @PathVariable("custId") final String custId,
      @RequestBody final List<SurfaceBetInfoRequestDTO> userGlobalCountRequest) {
    String sanitizedCustId = sanitizeInput(custId);
    return reactionService.getGlobalCount(sanitizedCustId, userGlobalCountRequest);
  }

  @Operation(summary = "Please use this api when you faced any issues with scheduler job.")
  @DeleteMapping
  public Mono<Boolean> cleanupMongoOldRecords() {

    log.info("Mongo Cleanup & Redis Reload called explicitly through rest api.");

    try {
      return reactionsCleanupScheduledTask.cleanupProcess().retry(NO_OF_RETRIES);
    } catch (Exception ex) {
      throw new ServiceExecutionException("rest api Mongo Cleanup & Redis Reload failed", ex);
    }
  }

  @DeleteMapping("redis/cleanup")
  public Mono<String> redisCleanUp() {

    return redisOperations.cleanUpAllRedisKeys();
  }
}
