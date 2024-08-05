package com.entain.oxygen.promosandbox.service;

import com.entain.oxygen.promosandbox.dto.UserRankRequestDto;
import com.entain.oxygen.promosandbox.dto.UserRankResponseDto;
import com.entain.oxygen.promosandbox.exception.PromoSandboxException;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
@Slf4j
public class UserRankService {

  private final PromoConfigService promoConfigService;

  private final UserAuthenticationService authenticationService;

  private final UserRankServiceHelper userRankServiceHelper;

  private static final String ERROR_MSG =
      "Error while fetching data from spark cluster. customerId : {} ,promotionId : {},leaderboardId:{} : error: {} ";

  @Autowired
  public UserRankService(
      PromoConfigService promoConfigService,
      UserAuthenticationService authenticationService,
      UserRankServiceHelper userRankServiceHelper) {
    this.promoConfigService = promoConfigService;
    this.authenticationService = authenticationService;
    this.userRankServiceHelper = userRankServiceHelper;
  }

  public UserRankResponseDto fetchUserRankDetails(UserRankRequestDto requestDto, String token) {
    UserRankResponseDto userRankResponse = new UserRankResponseDto();
    try {
      authenticationService.validateToken(token, requestDto.getCustomerId());
      long fetchUserRankDetails = System.currentTimeMillis();
      CompletableFuture<List<Map<Object, Object>>> topXList =
          CompletableFuture.supplyAsync(() -> userRankServiceHelper.fetchTopXRank(requestDto));
      CompletableFuture<Map<Object, Object>> individualRank =
          CompletableFuture.supplyAsync(
              () -> userRankServiceHelper.fetchIndividualRank(requestDto));
      CompletableFuture<Optional<Instant>> lastUpdatedTime =
          CompletableFuture.supplyAsync(
              () ->
                  promoConfigService.getLastFileModified(
                      requestDto.getPromotionId(), requestDto.getLeaderboardId()));
      userRankResponse.setTopXRank(topXList.get());
      userRankResponse.setUserRank(individualRank.get());
      lastUpdatedTime.get().ifPresent(userRankResponse::setLastFileModified);
      log.debug(
          "fetchUserRankDetails total time taken(MS) : {}  ",
          System.currentTimeMillis() - fetchUserRankDetails);
    } catch (InterruptedException e) {
      Thread.currentThread().interrupt(); // Restore interrupted state...
      log.error(
          ERROR_MSG,
          requestDto.getCustomerId(),
          requestDto.getPromotionId(),
          requestDto.getLeaderboardId(),
          e.getMessage());
      throw new PromoSandboxException("Exception while fetching data from spark ");
    } catch (ExecutionException ex) {
      log.error(
          ERROR_MSG,
          requestDto.getCustomerId(),
          requestDto.getPromotionId(),
          requestDto.getLeaderboardId(),
          ex.getMessage());
      throw new PromoSandboxException("Error while processing data from spark cluster");
    }
    return userRankResponse;
  }
}
