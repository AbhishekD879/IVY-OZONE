package com.ladbrokescoral.cashout.service.updates;

import static com.ladbrokescoral.cashout.config.InternalKafkaTopics.BET_UDPATES;
import static com.ladbrokescoral.cashout.config.InternalKafkaTopics.BET_UPDATES_ERRORS;
import static org.junit.jupiter.api.Assertions.assertFalse;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.argThat;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.after;
import static org.mockito.Mockito.timeout;

import com.coral.bpp.api.exception.BppUnauthorizedException;
import com.coral.bpp.api.model.bet.api.request.GetBetDetailRequest;
import com.coral.bpp.api.model.bet.api.response.oxi.base.Bet;
import com.ladbrokescoral.cashout.model.response.UpdateDto;
import com.ladbrokescoral.cashout.service.BppService;
import java.io.IOException;
import java.time.Duration;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import org.junit.jupiter.api.AfterEach;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Disabled;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.kafka.core.reactive.ReactiveKafkaProducerTemplate;
import reactor.core.publisher.Mono;

@ExtendWith(MockitoExtension.class)
@Disabled
class AsyncBetDetailThrottledServiceTest {

  private AsyncBetDetailThrottledService service;

  @Mock
  private ReactiveKafkaProducerTemplate<String, UpdateDto> betUpdateReactiveKafkaProducerTemplate;

  @Mock
  private ReactiveKafkaProducerTemplate<String, Throwable>
      betUpdatesErrorReactiveKafkaProducerTemplate;

  private BetUpdatesTopic betUpdatesTopic;
  private BppService bppServiceMock;
  private static final int TIME_TO_WAIT = 500;

  @BeforeEach
  public void setUp() throws Exception {
    betUpdatesTopic =
        new ReactiveKafkaBetUpdatesTopic(
            betUpdateReactiveKafkaProducerTemplate, betUpdatesErrorReactiveKafkaProducerTemplate);
    bppServiceMock = Mockito.mock(BppService.class);
    service =
        new AsyncBetDetailThrottledService(
            bppServiceMock, betUpdatesTopic, Duration.ofMillis(10), 1, "BUFFER");
    Thread.sleep(20);
  }

  @AfterEach
  public void tearDown() throws Exception {
    service.getDisposable().dispose();
  }

  @Test
  void exceptionShouldBeSerializedAndSentToKafka() {
    BppUnauthorizedException unAuthException = new BppUnauthorizedException("Unauthorized");
    Mockito.when(bppServiceMock.getBetDetail(any())).thenReturn(Mono.error(unAuthException));

    service.acceptBetDetailRequest(buildReq("123", Arrays.asList("1")));

    Mockito.verify(betUpdatesErrorReactiveKafkaProducerTemplate, timeout(TIME_TO_WAIT))
        .send(BET_UPDATES_ERRORS.getTopicName(), "123", unAuthException);
  }

  @Test
  void exceptionInFluxDoesNotTerminateIt() {
    service.getSink().error(new RuntimeException());
    assertFalse(service.getDisposable().isDisposed());
  }

  @Test
  void ioExceptionsAreNotSentToKafka() {
    IOException ioException = new IOException();
    Mockito.when(bppServiceMock.getBetDetail(any())).thenReturn(Mono.error(ioException));

    service.acceptBetDetailRequest(buildReq("123", Arrays.asList("1")));

    Mockito.verify(betUpdatesErrorReactiveKafkaProducerTemplate, after(500).never())
        .send(BET_UPDATES_ERRORS.getTopicName(), "1", ioException);
  }

  @Test
  void betUpdateIsSentToKafka() {
    Bet bet = bet("1");
    UpdateDto betUpdate = UpdateDto.builder().bet(bet).build();
    Mockito.when(bppServiceMock.getBetDetail(any(GetBetDetailRequest.class)))
        .thenReturn(Mono.just(Collections.singletonList(bet)));

    service.acceptBetDetailRequest(buildReq("123", Arrays.asList("1")));

    Mockito.verify(betUpdateReactiveKafkaProducerTemplate, timeout(TIME_TO_WAIT))
        .send(BET_UDPATES.getTopicName(), "123", betUpdate);
  }

  @Test
  void betUpdateIsSentWithTheNewestTokenIfMultipleTokenForSingleUser() {
    Bet bet = bet("1");
    UpdateDto betUpdate = UpdateDto.builder().bet(bet).build();
    Mockito.when(
            bppServiceMock.getBetDetail(
                argThat(req -> Arrays.asList("333", "456").contains(req.getToken()))))
        .thenReturn(Mono.just(Collections.singletonList(bet)));

    service.acceptBetDetailRequest(
        BetDetailRequestCtx.builder()
            .userId("user1")
            .timeToTokenExpirationLeft(Duration.ofMinutes(10))
            .request(GetBetDetailRequest.builder().token("123").betIds(Arrays.asList("1")).build())
            .build());

    service.acceptBetDetailRequest(
        BetDetailRequestCtx.builder()
            .userId("user1")
            .timeToTokenExpirationLeft(Duration.ofMinutes(10))
            .request(GetBetDetailRequest.builder().token("123").betIds(Arrays.asList("1")).build())
            .build());

    service.acceptBetDetailRequest(
        BetDetailRequestCtx.builder()
            .userId("user1")
            .timeToTokenExpirationLeft(Duration.ofMinutes(50))
            .request(GetBetDetailRequest.builder().token("456").betIds(Arrays.asList("1")).build())
            .build());

    service.acceptBetDetailRequest(
        BetDetailRequestCtx.builder()
            .userId("user2")
            .timeToTokenExpirationLeft(Duration.ofMinutes(30))
            .request(GetBetDetailRequest.builder().token("333").betIds(Arrays.asList("1")).build())
            .build());

    Mockito.verify(betUpdateReactiveKafkaProducerTemplate, timeout(TIME_TO_WAIT).times(1))
        .send(BET_UDPATES.getTopicName(), "123", betUpdate);

    Mockito.verify(betUpdateReactiveKafkaProducerTemplate, timeout(TIME_TO_WAIT).times(1))
        .send(BET_UDPATES.getTopicName(), "456", betUpdate);

    Mockito.verify(betUpdateReactiveKafkaProducerTemplate, timeout(TIME_TO_WAIT).times(1))
        .send(BET_UDPATES.getTopicName(), "333", betUpdate);
  }

  @Test
  void betRequestsAreMergedIntoOne() {
    Bet bet1 = bet("1");
    UpdateDto betUpdate1 = UpdateDto.builder().bet(bet1).build();
    Bet bet2 = bet("2");
    UpdateDto updateDto2 = UpdateDto.builder().bet(bet2).build();
    Mockito.when(bppServiceMock.getBetDetail(any(GetBetDetailRequest.class)))
        .thenReturn(Mono.just(Arrays.asList(bet1, bet2)));

    service.acceptBetDetailRequest(buildReq("123", Arrays.asList("1")));
    service.acceptBetDetailRequest(buildReq("123", Arrays.asList("1")));
    service.acceptBetDetailRequest(buildReq("123", Arrays.asList("2")));

    Mockito.verify(bppServiceMock, Mockito.timeout(TIME_TO_WAIT).times(1)).getBetDetail(any());
    Mockito.verify(betUpdateReactiveKafkaProducerTemplate, timeout(TIME_TO_WAIT))
        .send(BET_UDPATES.getTopicName(), "123", betUpdate1);
    Mockito.verify(betUpdateReactiveKafkaProducerTemplate, timeout(TIME_TO_WAIT))
        .send(BET_UDPATES.getTopicName(), "123", updateDto2);
  }

  @Test
  void separateTokensAreNotMerged() {
    Bet bet1 = bet("1");
    Bet bet2 = bet("2");

    Mockito.when(bppServiceMock.getBetDetail(any(GetBetDetailRequest.class)))
        .thenAnswer(
            invocation -> {
              GetBetDetailRequest request = invocation.getArgument(0);
              if (request.getToken().equals("123")) {
                return Mono.just(Arrays.asList(bet1));
              } else if (request.getToken().equals("321")) {
                return Mono.just(Arrays.asList(bet2));
              }
              throw new AssertionError();
            });

    service.acceptBetDetailRequest(buildReq("123", Arrays.asList("1")));
    service.acceptBetDetailRequest(buildReq("321", Arrays.asList("2")));

    Mockito.verify(bppServiceMock, Mockito.timeout(TIME_TO_WAIT).times(1))
        .getBetDetail(
            argThat(req -> req.getToken().equals("123") && req.getBetIds().get(0).equals("1")));
    Mockito.verify(bppServiceMock, Mockito.timeout(TIME_TO_WAIT).times(1))
        .getBetDetail(
            argThat(req -> req.getToken().equals("321") && req.getBetIds().get(0).equals("2")));

    Mockito.verify(betUpdateReactiveKafkaProducerTemplate, timeout(TIME_TO_WAIT))
        .send(BET_UDPATES.getTopicName(), "123", UpdateDto.builder().bet(bet1).build());
    Mockito.verify(betUpdateReactiveKafkaProducerTemplate, timeout(TIME_TO_WAIT))
        .send(BET_UDPATES.getTopicName(), "321", UpdateDto.builder().bet(bet2).build());
  }

  @Test
  void testMoreThen256Groups() {
    mockGetBetDetailToReturnBetIdsSameAsToken();

    int numberOfGroups = 1_000;
    for (int i = 1; i <= numberOfGroups; i++) {
      service.acceptBetDetailRequest(buildReq(String.valueOf(i), Arrays.asList(String.valueOf(i))));
    }

    Mockito.verify(betUpdateReactiveKafkaProducerTemplate, timeout(2_000).times(numberOfGroups))
        .send(eq(BET_UDPATES.getTopicName()), anyString(), any(UpdateDto.class));
  }

  private void mockGetBetDetailToReturnBetIdsSameAsToken() {
    Mockito.when(bppServiceMock.getBetDetail(any(GetBetDetailRequest.class)))
        .thenAnswer(
            invocation -> {
              GetBetDetailRequest request = invocation.getArgument(0);
              return Mono.just(Arrays.asList(bet(request.getToken())));
            });
  }

  private Bet bet(String s) {
    Bet bet1 = new Bet();
    bet1.setBetId(s);
    return bet1;
  }

  private BetDetailRequestCtx buildReq(String token, List<String> betIds) {
    return BetDetailRequestCtx.builder()
        .userId(token)
        .timeToTokenExpirationLeft(Duration.ZERO)
        .request(GetBetDetailRequest.builder().token(token).betIds(betIds).build())
        .build();
  }
}
