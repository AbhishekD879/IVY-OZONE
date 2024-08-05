package com.ladbrokescoral.reactions.service;

import static com.ladbrokescoral.reactions.util.ReactionHelper.*;

import com.ladbrokescoral.reactions.client.bpp.BppClient;
import com.ladbrokescoral.reactions.client.bpp.dto.UserData;
import com.ladbrokescoral.reactions.dto.*;
import com.ladbrokescoral.reactions.exception.ServiceExecutionException;
import com.ladbrokescoral.reactions.exception.UserNotFoundException;
import com.ladbrokescoral.reactions.repository.redis.RedisReactionRepository;
import java.util.*;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;
import reactor.core.publisher.Flux;
import reactor.core.publisher.Mono;
import reactor.util.function.Tuple2;
import reactor.util.function.Tuples;

/**
 * @author PBalarangakumar 14-06-2023
 */
@Slf4j
@Service
public class DefaultReactionService implements ReactionService {

  private final RedisReactionRepository redisRepository;
  private final MongoReactionService mongoReactionService;
  private final BppClient bppClient;

  public DefaultReactionService(
      final RedisReactionRepository redisRepository,
      final MongoReactionService mongoReactionService,
      final BppClient bppClient) {

    this.redisRepository = redisRepository;
    this.mongoReactionService = mongoReactionService;
    this.bppClient = bppClient;
  }

  @Override
  public Mono<Boolean> saveReaction(
      final String token, final String userName, final UserReactionDTO userReactionDTO) {

    final String reactionId = userReactionDTO.reactionId().name();
    final String userReactionKey = getUserReactionKey(userReactionDTO);
    final String globalIncrementReactionKey =
        getGlobalIncrementOrDecrementReactionKey(userReactionDTO, Optional.empty());
    final String deleteKey =
        getDeleteKey(userReactionDTO.selectionId(), userReactionDTO.surfaceBetId());

    return validateUserName(token, userName)
        .flatMap(
            response ->
                redisRepository
                    .saveReaction(userReactionKey, globalIncrementReactionKey, reactionId)
                    .flatMap(
                        increment ->
                            mongoReactionService.saveUser(
                                getMongoUserEntity(userReactionKey, reactionId, deleteKey)))
                    .map(entity -> response)
                    .doOnError(
                        (Throwable throwable) -> {
                          final String errorMsg =
                              "Error while saving reaction in db because of: "
                                  + throwable.getMessage();
                          log.error(errorMsg);
                          throw new ServiceExecutionException(errorMsg);
                        }));
  }

  @Override
  public Mono<String> updateReaction(
      final String token, final String userName, final UserReactionDTO userReactionDTO) {

    final String reactionId = userReactionDTO.reactionId().name();
    final String userReactionKey = getUserReactionKey(userReactionDTO);
    final String globalIncrementReactionKey =
        getGlobalIncrementOrDecrementReactionKey(userReactionDTO, Optional.empty());
    final String deleteKey =
        getDeleteKey(userReactionDTO.selectionId(), userReactionDTO.surfaceBetId());

    return validateUserName(token, userName)
        .flatMap(
            response ->
                redisRepository
                    .updateReaction(
                        userReactionDTO, userReactionKey, globalIncrementReactionKey, reactionId)
                    .flatMap(
                        increment ->
                            mongoReactionService.updateUser(
                                getMongoUserEntity(userReactionKey, reactionId, deleteKey)))
                    .map(entity -> reactionId)
                    .doOnError(
                        (Throwable throwable) -> {
                          final String errorMsg =
                              "Error while updating reaction in db because of: "
                                  + throwable.getMessage();
                          log.error(errorMsg);
                          throw new ServiceExecutionException(errorMsg);
                        }));
  }

  @Override
  public Mono<UserGlobalCountResponseDTO> getGlobalCount(
      final String custId, final List<SurfaceBetInfoRequestDTO> requestDTO) {

    return Flux.fromIterable(requestDTO)
        .flatMap(
            (SurfaceBetInfoRequestDTO request) -> {
              final String selectionId = request.selectionId();
              final String surfaceBetId = request.surfaceBetId();

              return redisRepository
                  .getReactions(getReactionKeys(custId, selectionId, surfaceBetId))
                  .map(
                      reactions ->
                          Tuples.of(
                              surfaceBetId,
                              new UserGlobalCountInfo(
                                  getReactionCount(reactions, ZERO),
                                  getReactionCount(reactions, ONE),
                                  getReactionCount(reactions, TWO),
                                  getUserReactedReaction(reactions))));
            })
        .collectMap(Tuple2::getT1, Tuple2::getT2)
        .map(
            userGlobalCountInfoMap ->
                new UserGlobalCountResponseDTO(custId, userGlobalCountInfoMap))
        .doOnError(
            (Throwable throwable) -> {
              final String errorMsg =
                  "Error while getting reactions from db because of: " + throwable.getMessage();
              log.error(errorMsg);
              throw new ServiceExecutionException(errorMsg);
            });
  }

  @Override
  public Mono<Map<String, Long>> collectGlobalCountFromMongo() {

    return mongoReactionService
        .getReactionGlobalCount()
        .collectMap(
            globalCount -> globalCount._id().deleteKey() + HASH + globalCount._id().redisValue(),
            GlobalCount::count);
  }

  private Long getReactionCount(final List<String> reactions, final int index) {

    try {
      return Optional.ofNullable(reactions.get(index))
          .filter(count -> !count.isEmpty())
          .map(Long::parseLong)
          .orElse(null);
    } catch (Exception ex) {
      throw new IllegalArgumentException("error occurred: " + ex.getMessage());
    }
  }

  private String getUserReactedReaction(final List<String> reactions) {

    return Optional.ofNullable(reactions.get(THREE)).filter(count -> !count.isEmpty()).orElse(null);
  }

  private Mono<Boolean> validateUserName(final String token, final String userName) {

    return bppClient
        .getValidUser(token)
        .retry(THREE)
        .flatMap(
            (UserData userData) -> {
              if (!userName.equals(userData.userName())) {
                return Mono.error(
                    new UserNotFoundException(
                        "userName didn't match with bpp api call response username."));
              }
              return Mono.just(true);
            });
  }
}
