package com.coral.oxygen.middleware.ms.quickbet.impl;

import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

import com.coral.bpp.api.model.bet.api.response.UserDataResponse;
import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.configuration.BanachResponseProcessorConfiguration;
import com.coral.oxygen.middleware.ms.quickbet.connector.BanachSelection;
import com.coral.oxygen.middleware.ms.quickbet.connector.BanachSelectionTest;
import com.coral.oxygen.middleware.ms.quickbet.connector.BppComponent;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.FreeBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachPlaceBetRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachSelectionRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.BanachSelectionResponse;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.DataResponseWrapper;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.ErrorMessage;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.FractionalPriceDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.banach.BanachPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.banach.BetErrorItem;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.banach.BetFailure;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.banach.BetPlacementItem;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.PriceDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.processor.BanachResponseProcessor;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachTimeoutException;
import com.ladbrokescoral.oxygen.byb.banach.client.BlockingBanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.*;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.PlaceBetResponse;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.PriceResponse;
import io.vavr.control.Try;
import java.util.Arrays;
import java.util.Collections;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.mockito.Mockito;

class BanachBetsOperationsTest {
  private Session session;
  private BanachBetsOperations ops;
  private BlockingBanachClient banachClient;
  private BppComponent bppComponent;

  @BeforeEach
  void setUp() throws Exception {
    session = Mockito.mock(Session.class);
    when(session.sessionId()).thenReturn("123");
    banachClient = Mockito.mock(BlockingBanachClient.class);
    bppComponent = Mockito.mock(BppComponent.class);
    BanachResponseProcessor processor =
        new BanachResponseProcessorConfiguration().configBanachResponseProcessor();
    ops = new BanachBetsOperations(banachClient, banachClient, processor, bppComponent);
  }

  @Test
  void testSuccessIsSentToClientIfResponseCodeIsOk() {
    GetPriceResponseDto priceResponse = new GetPriceResponseDto();
    priceResponse.setResponseCode(GetPriceResponseDto.ResponseCodeEnum.OK);
    priceResponse.setPriceNum(2);
    priceResponse.setPriceDen(1);
    when(banachClient.execute(anyString(), any(GetPriceRequestDto.class)))
        .thenReturn(new PriceResponse(priceResponse));

    BanachSelection selection =
        new BanachSelection(
            BanachSelectionTest.banachSelectionRequest(123L, Arrays.asList(1L, 2L), null));
    ops.addSelection(session, selection);

    verify(session)
        .sendData(
            Messages.ADD_BANACH_SELECTION_SUCCESS.code(),
            BanachSelectionResponse.builder()
                .data(new FractionalPriceDto(2, 1))
                .roomName(selection.selectionHash())
                .build());
  }

  @Test
  void testBanachSelectionCanBeAddedJustWithPlayerSelections() {
    GetPriceResponseDto priceResponse = new GetPriceResponseDto();
    priceResponse.setResponseCode(GetPriceResponseDto.ResponseCodeEnum.OK);
    priceResponse.setPriceNum(2);
    priceResponse.setPriceDen(1);
    when(banachClient.execute(anyString(), any(GetPriceRequestDto.class)))
        .thenReturn(new PriceResponse(priceResponse));

    BanachSelectionRequestData selectionData =
        BanachSelectionTest.banachSelectionRequest(
            123L,
            null,
            Collections.singletonList(BanachSelectionTest.virtualSelection(1L, 2L, 20L)));
    BanachSelection selection = new BanachSelection(selectionData);
    ops.addSelection(session, selection);

    verify(session)
        .sendData(
            Messages.ADD_BANACH_SELECTION_SUCCESS.code(),
            BanachSelectionResponse.builder()
                .data(new FractionalPriceDto(2, 1))
                .roomName(selection.selectionHash())
                .build());
  }

  @Test
  void testResponseCodeIsNotOkResultsInError() {
    GetPriceResponseDto.ResponseCodeEnum responseCode =
        GetPriceResponseDto.ResponseCodeEnum.COMPONENT_SUSPENDED;
    returnResponseCode(responseCode);
    verify(session)
        .sendData(
            Messages.ADD_BANACH_SELECTION_ERROR.code(),
            new ErrorMessage(
                "COMPONENT_SUSPENDED",
                responseCode.ordinal(),
                "One or more of the selection component(s) are suspended"));
  }

  @Test
  void testUnknown() {
    GetPriceResponseDto.ResponseCodeEnum responseCode =
        GetPriceResponseDto.ResponseCodeEnum.UNKNOWN;
    returnResponseCode(responseCode);
    verify(session)
        .sendData(
            Messages.ADD_BANACH_SELECTION_ERROR.code(),
            new ErrorMessage(
                "UNKNOWN_SELECTION_ERROR", responseCode.ordinal(), "Unknown selection error"));
  }

  @Test
  void testInvalidCombo() {
    GetPriceResponseDto.ResponseCodeEnum responseCode =
        GetPriceResponseDto.ResponseCodeEnum.INVALID_COMBINATION;
    returnResponseCode(responseCode);
    verify(session)
        .sendData(
            Messages.ADD_BANACH_SELECTION_ERROR.code(),
            new ErrorMessage(
                "INVALID_COMBINATION",
                responseCode.ordinal(),
                "Selection components cannot be combined"));
  }

  @Test
  void testInvalidMarginatedPrice() {
    GetPriceResponseDto.ResponseCodeEnum responseCode =
        GetPriceResponseDto.ResponseCodeEnum.INVALID_MARGINATED_PRICE;
    returnResponseCode(responseCode);
    verify(session)
        .sendData(
            Messages.ADD_BANACH_SELECTION_ERROR.code(),
            new ErrorMessage(
                "INVALID_MARGINATED_PRICE",
                responseCode.ordinal(),
                "Selection price has imposibly low probability"));
  }

  @Test
  void testBanachTimeoutOnPlaceBet() {
    mockBppUserData();
    mockSelections();

    BanachPlaceBetRequestData clientRequest = new BanachPlaceBetRequestData();
    clientRequest.setChannel("e");
    clientRequest.setCurrency("USD");
    clientRequest.setStake("2");
    clientRequest.setToken("bpptoken");
    clientRequest.setPrice("2/1");

    when(banachClient.execute(anyString(), any(PlaceBetRequestDto.class)))
        .thenThrow(new BanachTimeoutException("Banach timeout"));

    ops.placeBet(session, clientRequest);

    verify(session)
        .sendData(
            Messages.BANACH_PLACE_BET_ERROR.code(),
            RegularPlaceBetResponse.errorResponse(
                RegularPlaceBetResponse.Error.builder()
                    .code(Messages.ERROR_CODE.code())
                    .subErrorCode(Messages.SERVICE_ERROR.code())
                    .description("Connection timeout")
                    .build()));
  }

  @Test
  void testBanachTimeoutOnAddSelection() {
    when(banachClient.execute(anyString(), any(GetPriceRequestDto.class)))
        .thenThrow(new BanachTimeoutException("Banach timeout"));

    ops.addSelection(session, new BanachSelection(new BanachSelectionRequestData()));

    verify(session)
        .sendData(
            Messages.ADD_BANACH_SELECTION_ERROR.code(),
            new ErrorMessage("ERROR", "Failed to get price on Banach selection: Banach timeout"));
  }

  @Test
  void testPlaceBet() {
    mockBppUserData();
    mockSelections();

    BanachPlaceBetRequestData clientRequest = new BanachPlaceBetRequestData();
    clientRequest.setChannel("e");
    clientRequest.setCurrency("USD");
    clientRequest.setStake("2");
    clientRequest.setToken("bpptoken");
    clientRequest.setPrice("2/1");

    PlaceBetRequestDto expectedRequest =
        PlaceBetRequestDto.builder()
            .obEventId(123L)
            .obUserToken("abc")
            .channel("e")
            .userPriceNum(2)
            .userPriceDen(1)
            .stake("2")
            .selectionId(1L)
            .selectionId(2L)
            .currency("USD")
            .obUserId("test")
            .build();

    PlaceBetResponseDto banachResponseData = new PlaceBetResponseDto();
    BetPlacementResponseDto betPlacement = new BetPlacementResponseDto();
    betPlacement.setBetId(321L);
    betPlacement.setBetNo(0);
    betPlacement.setDate("date");
    betPlacement.setNumLines(1);
    betPlacement.setReceipt("receipt");
    betPlacement.setTotalStake("2");
    betPlacement.setBetPotentialWin("4");
    banachResponseData.setBetPlacement(Collections.singletonList(betPlacement));
    banachResponseData.setResponseCode(PlaceBetResponseDto.ResponseCodeEnum.ACCEPTED);
    PlaceBetResponse banachResponse = new PlaceBetResponse(banachResponseData);

    when(banachClient.execute(anyString(), any(PlaceBetRequestDto.class)))
        .thenReturn(banachResponse);

    ops.placeBet(session, clientRequest);

    verify(banachClient).execute("123", expectedRequest);
    BanachPlaceBetResponse expectedResponse =
        BanachPlaceBetResponse.builder()
            .responseCode(1)
            .betPlacementItem(
                BetPlacementItem.builder()
                    .betPotentialWin("4")
                    .receipt("receipt")
                    .date("date")
                    .betNo(0)
                    .betId(321L)
                    .numLines(1)
                    .totalStake("2")
                    .build())
            .build();
    DataResponseWrapper<BanachPlaceBetResponse> response =
        new DataResponseWrapper<>(expectedResponse);
    verify(session).sendData(Messages.BANACH_PLACE_BET_SUCCESS.code(), response);
  }

  @Test
  void testTryProcessResponse() {
    BanachResponseProcessor processor =
        new BanachResponseProcessorConfiguration().configBanachResponseProcessor();
    processor.setNextProcessor(null);
    PlaceBetResponseDto dto = new PlaceBetResponseDto();
    dto.setResponseCode(PlaceBetResponseDto.ResponseCodeEnum.UNKNOWN);
    Assertions.assertThrows(
        IllegalStateException.class,
        () -> {
          processor.tryProcessResponse(null, dto);
        });
  }

  private void mockBppUserData() {
    UserDataResponse userDataResponse = new UserDataResponse();
    userDataResponse.setOxiApiToken("abc");
    userDataResponse.setSportBookUserName("test");
    when(bppComponent.fetchUserData(any())).thenReturn(Try.ofSupplier(() -> userDataResponse));
  }

  @Test
  void testPlaceBetWithFreebet() {
    mockBppUserData();
    mockSelections();

    BanachPlaceBetRequestData clientRequest = new BanachPlaceBetRequestData();
    clientRequest.setChannel("e");
    clientRequest.setCurrency("USD");
    clientRequest.setStake("2");
    clientRequest.setToken("bpptoken");
    clientRequest.setFreebet(FreeBetRequest.builder().id(555L).stake("10.99").build());
    clientRequest.setPrice("2/1");

    PlaceBetRequestDto expectedRequest =
        PlaceBetRequestDto.builder()
            .obEventId(123L)
            .obUserToken("abc")
            .channel("e")
            .userPriceNum(2)
            .userPriceDen(1)
            .stake("12.99")
            .selectionId(1L)
            .selectionId(2L)
            .currency("USD")
            .freeBetId(555L)
            .obUserId("test")
            .build();

    PlaceBetResponseDto banachResponseData = new PlaceBetResponseDto();
    BetPlacementResponseDto betPlacement = new BetPlacementResponseDto();
    betPlacement.setBetId(321L);
    betPlacement.setBetNo(0);
    betPlacement.setDate("date");
    betPlacement.setNumLines(1);
    betPlacement.setReceipt("receipt");
    betPlacement.setTotalStake("2");
    betPlacement.setBetPotentialWin("4");
    banachResponseData.setBetPlacement(Collections.singletonList(betPlacement));
    banachResponseData.setResponseCode(PlaceBetResponseDto.ResponseCodeEnum.ACCEPTED);
    PlaceBetResponse banachResponse = new PlaceBetResponse(banachResponseData);

    when(banachClient.execute(anyString(), any(PlaceBetRequestDto.class)))
        .thenReturn(banachResponse);

    ops.placeBet(session, clientRequest);

    verify(banachClient).execute("123", expectedRequest);
    BanachPlaceBetResponse expectedResponse =
        BanachPlaceBetResponse.builder()
            .responseCode(1)
            .betPlacementItem(
                BetPlacementItem.builder()
                    .betPotentialWin("4")
                    .receipt("receipt")
                    .date("date")
                    .betNo(0)
                    .betId(321L)
                    .numLines(1)
                    .totalStake("2")
                    .build())
            .build();
    DataResponseWrapper<BanachPlaceBetResponse> response =
        new DataResponseWrapper<>(expectedResponse);
    verify(session).sendData(Messages.BANACH_PLACE_BET_SUCCESS.code(), response);
  }

  private void mockSelections() {
    when(session.getBanachSelectionData())
        .thenReturn(BanachSelectionTest.banachSelectionRequest(123L, Arrays.asList(1L, 2L), null));
  }

  @Test
  void testPlaceBetPriceChangeError() {
    mockBppUserData();
    mockSelections();

    PlaceBetResponseDto banachResponseData = new PlaceBetResponseDto();
    GetPriceResponseDto validPrice = new GetPriceResponseDto();
    validPrice.setPriceNum(12);
    validPrice.setPriceDen(10);
    validPrice.setHundredPcLine("1.24");
    validPrice.setResponseMessage("ok");
    validPrice.setResponseCode(GetPriceResponseDto.ResponseCodeEnum.OK);
    banachResponseData.setValidPrice(validPrice);
    banachResponseData.setResponseCode(PlaceBetResponseDto.ResponseCodeEnum.PRICE_NOT_AVAILABLE);

    PlaceBetResponse banachResponse = new PlaceBetResponse(banachResponseData);
    when(banachClient.execute(anyString(), any(PlaceBetRequestDto.class)))
        .thenReturn(banachResponse);

    ops.placeBet(session, BanachPlaceBetRequestData.builder().price("1/1").build());

    RegularPlaceBetResponse expectedResponse = new RegularPlaceBetResponse();
    RegularPlaceBetResponse.Data expectedResponseData = new RegularPlaceBetResponse.Data();
    RegularPlaceBetResponse.Error error = new RegularPlaceBetResponse.Error();
    error.setCode("CHANGE_ERROR");
    error.setPrice(new PriceDto("12", "10", "BANACH"));
    error.setSubErrorCode("PRICE_CHANGED");
    expectedResponseData.setError(error);
    expectedResponse.setData(expectedResponseData);
    verify(session).sendData(Messages.BANACH_PLACE_BET_ERROR.code(), expectedResponse);
  }

  @Test
  void testPtAuthErrorReturnedOn9516() {
    mockBppUserData();
    mockSelections();

    PlaceBetResponseDto banachResponseData = new PlaceBetResponseDto();
    BetErrorDto betError = new BetErrorDto();
    betError.setBetFailureCode(9516);
    betError.setBetFailureReason("Playtech Error: Session Invalid");
    BetFailureResponseDto betFailure = new BetFailureResponseDto();
    betFailure.setBetNo(0);
    betFailure.setBetError(Collections.singletonList(betError));
    banachResponseData.setBetFailure(betFailure);

    banachResponseData.setResponseCode(PlaceBetResponseDto.ResponseCodeEnum.DOWNSTREAM_REJECTED);

    PlaceBetResponse banachResponse = new PlaceBetResponse(banachResponseData);
    when(banachClient.execute(anyString(), any(PlaceBetRequestDto.class)))
        .thenReturn(banachResponse);

    ops.placeBet(session, BanachPlaceBetRequestData.builder().price("1/1").build());

    verify(session)
        .sendData(
            Messages.BANACH_PLACE_BET_ERROR.code(),
            RegularPlaceBetResponse.unauthorizedAccessError());
  }

  @Test
  void testPtAuthErrorReturnedOn9518() {
    mockBppUserData();
    mockSelections();

    PlaceBetResponseDto banachResponseData = new PlaceBetResponseDto();
    BetErrorDto betError = new BetErrorDto();
    betError.setBetFailureCode(9518);
    betError.setBetFailureReason("PT_ERR_USER_NOT_FOUND");
    BetFailureResponseDto betFailure = new BetFailureResponseDto();
    betFailure.setBetNo(0);
    betFailure.setBetError(Collections.singletonList(betError));
    banachResponseData.setBetFailure(betFailure);

    banachResponseData.setResponseCode(PlaceBetResponseDto.ResponseCodeEnum.DOWNSTREAM_REJECTED);

    PlaceBetResponse banachResponse = new PlaceBetResponse(banachResponseData);
    when(banachClient.execute(anyString(), any(PlaceBetRequestDto.class)))
        .thenReturn(banachResponse);

    ops.placeBet(session, BanachPlaceBetRequestData.builder().price("1/1").build());

    verify(session)
        .sendData(
            Messages.BANACH_PLACE_BET_ERROR.code(),
            RegularPlaceBetResponse.unauthorizedAccessError());
  }

  @Test
  void testHighStakeError() {
    mockBppUserData();
    mockSelections();

    PlaceBetResponseDto banachResponseData = new PlaceBetResponseDto();
    BetErrorDto betError = new BetErrorDto();
    betError.setBetFailureCode(538);
    betError.setBetFailureReason("STK_HIGH");
    betError.setBetFailureDebug("The maximum stake per line for this bet is 667.00");
    BetFailureResponseDto betFailure = new BetFailureResponseDto();
    betFailure.setBetNo(0);
    betFailure.setBetError(Collections.singletonList(betError));
    betFailure.setBetMaxStake("667");
    betFailure.setBetMinStake("0.01");
    banachResponseData.setBetFailure(betFailure);

    banachResponseData.setResponseCode(PlaceBetResponseDto.ResponseCodeEnum.DOWNSTREAM_REJECTED);

    PlaceBetResponse banachResponse = new PlaceBetResponse(banachResponseData);
    when(banachClient.execute(anyString(), any(PlaceBetRequestDto.class)))
        .thenReturn(banachResponse);

    ops.placeBet(session, BanachPlaceBetRequestData.builder().price("1/1").build());

    verify(session)
        .sendData(
            Messages.BANACH_PLACE_BET_ERROR.code(),
            RegularPlaceBetResponse.errorResponse(
                RegularPlaceBetResponse.Error.builder()
                    .code("ERROR")
                    .subErrorCode("STAKE_HIGH")
                    .description("The maximum stake per line for this bet is 667.00")
                    .maxStake(betFailure.getBetMaxStake())
                    .build()));
  }

  @Test
  void testEventStartedError() {
    mockBppUserData();
    mockSelections();

    PlaceBetResponseDto banachResponseData = new PlaceBetResponseDto();
    BetErrorDto betError = new BetErrorDto();
    betError.setBetFailureCode(537);
    betError.setBetFailureReason("event has started");
    betError.setBetFailureDesc("START");
    BetFailureResponseDto betFailure = new BetFailureResponseDto();
    betFailure.setBetNo(0);
    betFailure.setBetError(Collections.singletonList(betError));
    banachResponseData.setBetFailure(betFailure);

    banachResponseData.setResponseCode(PlaceBetResponseDto.ResponseCodeEnum.DOWNSTREAM_REJECTED);

    PlaceBetResponse banachResponse = new PlaceBetResponse(banachResponseData);
    when(banachClient.execute(anyString(), any(PlaceBetRequestDto.class)))
        .thenReturn(banachResponse);

    ops.placeBet(session, BanachPlaceBetRequestData.builder().price("1/1").build());

    verify(session)
        .sendData(
            Messages.BANACH_PLACE_BET_ERROR.code(),
            RegularPlaceBetResponse.errorResponse(
                RegularPlaceBetResponse.Error.builder()
                    .code("ERROR")
                    .subErrorCode("EVENT_STARTED")
                    .description("event has started")
                    .build()));
  }

  @Test
  void testDefaultBanachError() {
    mockBppUserData();
    mockSelections();
    PlaceBetResponseDto placeBetResponseDto = new PlaceBetResponseDto();
    placeBetResponseDto.setResponseCode(PlaceBetResponseDto.ResponseCodeEnum.COMPONENT_SUSPENDED);
    PlaceBetResponse banachResponse = new PlaceBetResponse(placeBetResponseDto);
    when(banachClient.execute(anyString(), any(PlaceBetRequestDto.class)))
        .thenReturn(banachResponse);

    ops.placeBet(session, BanachPlaceBetRequestData.builder().price("1/1").build());

    verify(session)
        .sendData(
            Messages.BANACH_PLACE_BET_ERROR.code(),
            RegularPlaceBetResponse.errorResponse(
                RegularPlaceBetResponse.Error.builder()
                    .code("ERROR")
                    .description(String.format("Banach response code: %s", 3))
                    .subErrorCode("DEFAULT")
                    .build()));
  }

  @Test
  void testSuccessIsReturnedIfItsBetFailure() {
    mockBppUserData();
    mockSelections();
    PlaceBetResponseDto banachResponseData = new PlaceBetResponseDto();
    BetErrorDto betError = new BetErrorDto();
    betError.setBetFailureCode(554);
    betError.setBetFailureReason("bet.invalidChannel");
    BetFailureResponseDto betFailure = new BetFailureResponseDto();
    betFailure.setBetNo(0);
    betFailure.setBetError(Collections.singletonList(betError));
    OxiReturnStatus oxiReturnStatus = new OxiReturnStatus();
    oxiReturnStatus.setCode("1");
    banachResponseData.setOxiReturnStatus(oxiReturnStatus);
    banachResponseData.setBetFailure(betFailure);

    banachResponseData.setResponseCode(PlaceBetResponseDto.ResponseCodeEnum.DOWNSTREAM_REJECTED);

    PlaceBetResponse banachResponse = new PlaceBetResponse(banachResponseData);

    when(banachClient.execute(anyString(), any(PlaceBetRequestDto.class)))
        .thenReturn(banachResponse);

    ops.placeBet(session, BanachPlaceBetRequestData.builder().price("1/1").build());

    BanachPlaceBetResponse banachPlaceBetResponse =
        BanachPlaceBetResponse.builder()
            .betFailure(
                BetFailure.builder()
                    .betErrorItem(
                        BetErrorItem.builder()
                            .betFailureCode(554)
                            .betFailureReason("bet.invalidChannel")
                            .build())
                    .betNo(0)
                    .build())
            .responseCode(6)
            .build();
    DataResponseWrapper<BanachPlaceBetResponse> response =
        new DataResponseWrapper<>(banachPlaceBetResponse);
    verify(session).sendData(Messages.BANACH_PLACE_BET_SUCCESS.code(), response);
  }

  @Test
  void testDefaultErrorIsReturnedIfNoBetErrorAndBetPlacement() {
    mockBppUserData();
    mockSelections();

    PlaceBetResponseDto placeBetResponseDto = new PlaceBetResponseDto();
    placeBetResponseDto.setResponseCode(PlaceBetResponseDto.ResponseCodeEnum.UNABLE_TO_PLACE_BET);
    OxiReturnStatus oxiReturnStatus = new OxiReturnStatus();
    oxiReturnStatus.setCode("1");
    oxiReturnStatus.setMessage("success");
    placeBetResponseDto.setOxiReturnStatus(oxiReturnStatus);
    PlaceBetResponse banachResponse = new PlaceBetResponse(placeBetResponseDto);
    when(banachClient.execute(anyString(), any(PlaceBetRequestDto.class)))
        .thenReturn(banachResponse);

    ops.placeBet(session, BanachPlaceBetRequestData.builder().price("1/1").build());

    verify(session)
        .sendData(
            Messages.BANACH_PLACE_BET_ERROR.code(),
            RegularPlaceBetResponse.errorResponse(
                RegularPlaceBetResponse.Error.builder()
                    .code("ERROR")
                    .description(String.format("Banach response code: %s", 8))
                    .subErrorCode("DEFAULT")
                    .build()));
  }

  private void returnResponseCode(GetPriceResponseDto.ResponseCodeEnum responseCode) {
    GetPriceResponseDto priceResponse = new GetPriceResponseDto();
    priceResponse.setResponseCode(responseCode);
    when(banachClient.execute(anyString(), any(GetPriceRequestDto.class)))
        .thenReturn(new PriceResponse(priceResponse));

    ops.addSelection(session, new BanachSelection(new BanachSelectionRequestData()));
  }

  @Test
  void selectionIdsIsEmptyArraysWhenNotPresent() {
    mockBppUserData();
    when(session.getBanachSelectionData())
        .thenReturn(
            BanachSelectionTest.banachSelectionRequest(
                123L, null, Arrays.asList(BanachSelectionTest.virtualSelection(1L, 1L, 12L))));

    BanachPlaceBetRequestData clientRequest = new BanachPlaceBetRequestData();
    clientRequest.setChannel("e");
    clientRequest.setCurrency("USD");
    clientRequest.setStake("2");
    clientRequest.setToken("bpptoken");
    clientRequest.setPrice("2/1");

    PlaceBetRequestDto expectedRequest =
        PlaceBetRequestDto.builder()
            .obEventId(123L)
            .obUserToken("abc")
            .channel("e")
            .userPriceNum(2)
            .userPriceDen(1)
            .stake("2")
            .virtualSelectionDetail(BanachSelectionTest.virtualSelection(1L, 1L, 12L))
            .currency("USD")
            .obUserId("test")
            .build();

    // Precondition, not actual assertion
    assertThat(expectedRequest.getSelectionIds()).isEmpty();

    PlaceBetResponseDto banachResponseData = new PlaceBetResponseDto();
    BetPlacementResponseDto betPlacement = new BetPlacementResponseDto();
    betPlacement.setBetId(321L);
    betPlacement.setBetNo(0);
    betPlacement.setDate("date");
    betPlacement.setNumLines(1);
    betPlacement.setReceipt("receipt");
    betPlacement.setTotalStake("2");
    betPlacement.setBetPotentialWin("4");
    banachResponseData.setBetPlacement(Collections.singletonList(betPlacement));
    banachResponseData.setResponseCode(PlaceBetResponseDto.ResponseCodeEnum.ACCEPTED);
    PlaceBetResponse banachResponse = new PlaceBetResponse(banachResponseData);

    when(banachClient.execute(anyString(), any(PlaceBetRequestDto.class)))
        .thenReturn(banachResponse);

    ops.placeBet(session, clientRequest);

    verify(banachClient).execute("123", expectedRequest);
    BanachPlaceBetResponse expectedResponse =
        BanachPlaceBetResponse.builder()
            .responseCode(1)
            .betPlacementItem(
                BetPlacementItem.builder()
                    .betPotentialWin("4")
                    .receipt("receipt")
                    .date("date")
                    .betNo(0)
                    .betId(321L)
                    .numLines(1)
                    .totalStake("2")
                    .build())
            .build();
    DataResponseWrapper<BanachPlaceBetResponse> response =
        new DataResponseWrapper<>(expectedResponse);
    verify(session).sendData(Messages.BANACH_PLACE_BET_SUCCESS.code(), response);
  }

  @Test
  void testRestoreState() {
    when(banachClient.execute(anyString(), any(GetPriceRequestDto.class)))
        .thenThrow(new BanachTimeoutException("Banach timeout"));
    BanachSelectionRequestData banachSelection = new BanachSelectionRequestData();
    banachSelection.setSelectionIds(Arrays.asList(1231111L));
    when(session.getBanachSelectionData()).thenReturn(banachSelection);
    ops.restoreState(session);
    verify(session, times(2)).save();
  }

  @Test
  void testBppError() {
    ops.handleBppFailure(session, new Throwable());
    verify(session).sendData(Mockito.any(), Mockito.any());
  }

  @Test
  void testTryPlaceBet() {
    UserDataResponse userDataResponse = new UserDataResponse();
    userDataResponse.setOxiApiToken("abc");
    userDataResponse.setSportBookUserName("test");
    when(bppComponent.fetchUserData(any())).thenReturn(Try.ofSupplier(() -> userDataResponse));
    BanachPlaceBetRequestData requestData = new BanachPlaceBetRequestData();
    requestData.setToken("ehwgdjhegdjged");
    ops.placeBet(session, requestData);
    verify(bppComponent).fetchUserData(Mockito.any());
  }
}
