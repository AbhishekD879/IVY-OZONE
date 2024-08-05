package com.ladbrokescoral.reactions.util;

import com.ladbrokescoral.reactions.dto.Reaction;
import com.ladbrokescoral.reactions.dto.UserReactionDTO;
import com.ladbrokescoral.reactions.repository.mongo.entity.MongoUserEntity;
import java.util.List;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.web.util.HtmlUtils;

/**
 * @author PBalarangakumar 14-06-2023
 */
@Slf4j
@SuppressWarnings({"StringBufferReplaceableByString", "OptionalUsedAsFieldOrParameterType"})
public class ReactionHelper {

  public static final String HASH = "#";
  public static final String ADDITIONAL_STATUS = "additionalStatus";
  public static final String MESSAGE = "message";
  public static final String PING = "ping";
  public static final String STATUS = "status";
  public static final String UP_STATUS = "UP";
  public static final String TOKEN = "token";
  public static final String USER_NAME = "userName";
  public static final int NO_OF_RETRIES = 2;
  public static final int ZERO = 0;
  public static final int ONE = 1;
  public static final int TWO = 2;
  public static final int THREE = 3;

  private ReactionHelper() {}

  public static String getUserReactionKey(final UserReactionDTO userReactionDTO) {

    final StringBuilder userReactionKey = new StringBuilder();
    userReactionKey.append(userReactionDTO.custId());
    userReactionKey.append(HASH);
    userReactionKey.append(userReactionDTO.selectionId());
    userReactionKey.append(HASH);
    userReactionKey.append(userReactionDTO.surfaceBetId());

    return userReactionKey.toString();
  }

  public static String getGlobalIncrementOrDecrementReactionKey(
      final UserReactionDTO userReactionDTO, final Optional<String> oldReaction) {

    final StringBuilder globalCountReactionKey = new StringBuilder();
    globalCountReactionKey.append(userReactionDTO.selectionId());
    globalCountReactionKey.append(HASH);
    globalCountReactionKey.append(userReactionDTO.surfaceBetId());
    globalCountReactionKey.append(HASH);
    globalCountReactionKey.append(oldReaction.orElse(userReactionDTO.reactionId().name()));

    return globalCountReactionKey.toString();
  }

  public static MongoUserEntity getMongoUserEntity(
      final String redisKey, final String redisValue, final String deleteKey) {

    return new MongoUserEntity(redisKey, redisValue, deleteKey);
  }

  public static String getDeleteKey(final String selectionId, final String surfaceBetId) {

    final StringBuilder deleteKey = new StringBuilder();
    deleteKey.append(selectionId);
    deleteKey.append(HASH);
    deleteKey.append(surfaceBetId);

    return deleteKey.toString();
  }

  public static List<String> getReactionKeys(
      final String custId, final String selectionId, final String surfaceBetId) {

    final String reaction1Key =
        getGlobalReactionKey(selectionId, surfaceBetId, Reaction.REACTION1.name());
    final String reaction2Key =
        getGlobalReactionKey(selectionId, surfaceBetId, Reaction.REACTION2.name());
    final String reaction3Key =
        getGlobalReactionKey(selectionId, surfaceBetId, Reaction.REACTION3.name());
    final String userReactionKey = getUserReactionKey(custId, selectionId, surfaceBetId);

    return List.of(reaction1Key, reaction2Key, reaction3Key, userReactionKey);
  }

  private static String getGlobalReactionKey(
      final String selectionId, final String surfaceBetId, final String reactionId) {

    final StringBuilder globalCountReactionKey = new StringBuilder();
    globalCountReactionKey.append(selectionId);
    globalCountReactionKey.append(HASH);
    globalCountReactionKey.append(surfaceBetId);
    globalCountReactionKey.append(HASH);
    globalCountReactionKey.append(reactionId);

    return globalCountReactionKey.toString();
  }

  private static String getUserReactionKey(
      final String custId, final String selectionId, final String surfaceBetId) {

    final StringBuilder userReactionKey = new StringBuilder();
    userReactionKey.append(custId);
    userReactionKey.append(HASH);
    userReactionKey.append(selectionId);
    userReactionKey.append(HASH);
    userReactionKey.append(surfaceBetId);

    return userReactionKey.toString();
  }

  public static String trace(final String message) {
    log.trace(message);
    return message;
  }

  public static String error(final String message, final String ex) {
    log.error(message, ex);
    return message;
  }

  public static String sanitizeInput(String input) {
    return HtmlUtils.htmlEscape(input);
  }
}
