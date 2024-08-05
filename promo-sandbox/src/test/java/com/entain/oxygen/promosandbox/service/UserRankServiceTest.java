package com.entain.oxygen.promosandbox.service;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.when;

import com.entain.oxygen.promosandbox.dto.UserRankRequestDto;
import com.entain.oxygen.promosandbox.dto.UserRankResponseDto;
import com.entain.oxygen.promosandbox.exception.PromoSandboxException;
import com.entain.oxygen.promosandbox.utils.IConstantsTest;
import java.time.Instant;
import java.util.*;
import java.util.concurrent.CompletableFuture;
import java.util.concurrent.ExecutionException;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@SuppressWarnings("java:S5778")
class UserRankServiceTest {

  @Mock private PromoConfigService promoConfigService;
  @Mock private UserRankServiceHelper userRankServiceHelper;
  @Mock private UserAuthenticationService authenticationService;
  @InjectMocks private UserRankService userRankService;

  @BeforeEach
  void setUp() {
    when(userRankServiceHelper.fetchTopXRank(any(UserRankRequestDto.class)))
        .thenReturn(new ArrayList<>());
    when(userRankServiceHelper.fetchIndividualRank(any(UserRankRequestDto.class)))
        .thenReturn(new HashMap<>());
    when(promoConfigService.getLastFileModified(anyString(), anyString()))
        .thenReturn(Optional.of(Instant.now()));
  }

  @Test
  void fetchUserRankDetailsTest() {
    UserRankRequestDto userRankRequestDto = new UserRankRequestDto();
    userRankRequestDto.setPromotionId(IConstantsTest.PROMOTION_ID);
    userRankRequestDto.setCustomerId("3432");
    userRankRequestDto.setLeaderboardId(IConstantsTest.LEADERBOARD_ID);
    userRankRequestDto.setNoOfPosition(1);
    userRankRequestDto.setCustomerRanking(true);
    List<Map<Object, Object>> topXListResult = new ArrayList<>();
    Map<Object, Object> userRankData = new HashMap<>();
    userRankData.put("customerId", "2345678");
    userRankData.put("rank", 1);
    topXListResult.add(userRankData);
    when(userRankServiceHelper.fetchTopXRank(any(UserRankRequestDto.class)))
        .thenReturn(topXListResult);

    Map<Object, Object> individualRankResult = new HashMap<>();
    individualRankResult.put("rank", 1);
    when(userRankServiceHelper.fetchIndividualRank(any(UserRankRequestDto.class)))
        .thenReturn(individualRankResult);

    when(promoConfigService.getLastFileModified(anyString(), anyString()))
        .thenReturn(Optional.of(Instant.now()));
    UserRankResponseDto response =
        userRankService.fetchUserRankDetails(userRankRequestDto, "test123");
    assertNotNull(response);
  }

  @Test
  void fetchUserRankDetailsInterruptedExceptionTest() {
    UserRankRequestDto userRankRequestDto = Mockito.mock(UserRankRequestDto.class);
    Thread task =
        new Thread(
            () ->
                assertThrows(
                    PromoSandboxException.class,
                    () -> userRankService.fetchUserRankDetails(userRankRequestDto, "test123")));
    task.start();
    task.interrupt();
  }

  @Test
  void fetchUserRankDetailsExecutionExceptionTest() {
    UserRankRequestDto userRankRequestDto = new UserRankRequestDto();
    userRankRequestDto.setPromotionId(IConstantsTest.PROMOTION_ID);
    userRankRequestDto.setCustomerId("3432");
    userRankRequestDto.setLeaderboardId(IConstantsTest.LEADERBOARD_ID);
    userRankRequestDto.setNoOfPosition(1);
    userRankRequestDto.setCustomerRanking(true);

    when(userRankServiceHelper.fetchTopXRank(any(UserRankRequestDto.class)))
        .thenAnswer(
            invocation -> {
              CompletableFuture<List<Map<Object, Object>>> future = new CompletableFuture<>();
              future.completeExceptionally(new ExecutionException("Caught exception", null));
              return future;
            });
    PromoSandboxException exception =
        assertThrows(
            PromoSandboxException.class,
            () -> userRankService.fetchUserRankDetails(userRankRequestDto, "test123"));

    assertEquals("Error while processing data from spark cluster", exception.getMessage());
  }
}
