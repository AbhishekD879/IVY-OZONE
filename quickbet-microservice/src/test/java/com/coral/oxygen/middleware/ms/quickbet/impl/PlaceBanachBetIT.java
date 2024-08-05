package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.ADD_BANACH_SELECTION;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.ADD_BANACH_SELECTION_SUCCESS;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.BANACH_PLACE_BET;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.BANACH_PLACE_BET_ERROR;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.BANACH_PLACE_BET_SUCCESS;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.ERROR_CODE;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.UNAUTHORIZED_ACCESS;
import static com.ladbrokescoral.oxygen.byb.banach.dto.external.GetPriceResponseDto.ResponseCodeEnum.OK;
import static java.util.Arrays.asList;
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.verify;
import static org.mockito.Mockito.when;

import com.coral.bpp.api.model.bet.api.request.UserDataDto;
import com.coral.bpp.api.model.bet.api.response.GeneralResponse;
import com.coral.bpp.api.model.bet.api.response.UserDataResponse;
import com.coral.bpp.api.service.BppService;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.FreeBetRequest;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachPlaceBetRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachSelectionRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.BanachSelectionResponse;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.DataResponseWrapper;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.banach.BanachPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.banach.BetPlacementItem;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse.Error;
import com.coral.oxygen.middleware.ms.quickbet.utils.WebSocketTestClient;
import com.fasterxml.jackson.core.type.TypeReference;
import com.ladbrokescoral.oxygen.byb.banach.client.BanachTimeoutException;
import com.ladbrokescoral.oxygen.byb.banach.client.BlockingBanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.BetPlacementResponseDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetPriceRequestDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetPriceResponseDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.OxiReturnStatus;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.PlaceBetRequestDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.PlaceBetResponseDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.PlaceBetResponse;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.PriceResponse;
import java.util.Arrays;
import org.assertj.core.api.SoftAssertions;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.ArgumentCaptor;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@IntegrationTest
public class PlaceBanachBetIT {

  private static final int USER_STAKE = 10;
  private static final int FREEBET_STAKE = 20;
  private static final String OXI_TOKEN = "v8ad0s9v70av7";
  private static final String BPP_TOKEN = "80asd5y23hh9f";

  @Autowired private WebSocketTestClient client;

  @MockBean private BppService bppService;

  @MockBean private BlockingBanachClient<GetPriceRequestDto, PriceResponse> selectionClient;

  @MockBean private BlockingBanachClient<PlaceBetRequestDto, PlaceBetResponse> banachClient;

  private static final TypeReference<DataResponseWrapper<BanachPlaceBetResponse>>
      BANACH_PLACE_BET_RESPONSE_TYPE_REF =
          new TypeReference<DataResponseWrapper<BanachPlaceBetResponse>>() {};

  @Test
  public void shouldPlaceBanachBet() {
    // given
    BetPlacementResponseDto responseDto = createBetPlacementResponseDto();

    // when
    BetPlacementItem placementItem =
        addSelectionAndPlaceBanachBet(banachPlaceBetRequest(), responseDto);

    ArgumentCaptor<PlaceBetRequestDto> argument = ArgumentCaptor.forClass(PlaceBetRequestDto.class);
    verify(banachClient).execute(any(), argument.capture());

    // then
    assertPlacementsEquality(placementItem, responseDto);
    assertThat(argument.getValue().getStake()).isEqualTo(String.valueOf(USER_STAKE));
  }

  @Test
  public void shouldPlaceBanachBetWithFreebet() {
    // given
    BetPlacementResponseDto banachClientResponse = createBetPlacementResponseDto();

    // when
    BetPlacementItem item =
        addSelectionAndPlaceBanachBet(banachPlaceBetRequestWithFreebet(), banachClientResponse);

    // then
    ArgumentCaptor<PlaceBetRequestDto> argument = ArgumentCaptor.forClass(PlaceBetRequestDto.class);
    verify(banachClient).execute(any(), argument.capture());

    assertPlacementsEquality(item, banachClientResponse);
    assertThat(argument.getValue().getStake())
        .isEqualTo(String.valueOf(USER_STAKE + FREEBET_STAKE));
  }

  private BetPlacementResponseDto createBetPlacementResponseDto() {
    BetPlacementResponseDto responseDto = new BetPlacementResponseDto();
    responseDto.setBetId(1L);
    responseDto.setNumLines(222);
    responseDto.setBetNo(333);
    responseDto.setTotalStake("444");
    responseDto.setDate("2019-01-01");
    responseDto.setReceipt("receipt");

    return responseDto;
  }

  private BetPlacementItem addSelectionAndPlaceBanachBet(
      BanachPlaceBetRequestData requestData, BetPlacementResponseDto banachClientResponse) {
    // given
    addBanachSelection();

    when(banachClient.execute(any(), any(PlaceBetRequestDto.class)))
        .thenReturn(placeBetResponse(banachClientResponse));
    when(bppService.userData(new UserDataDto(BPP_TOKEN)))
        .thenReturn(generalResponseForUserData(OXI_TOKEN));

    // when
    DataResponseWrapper<BanachPlaceBetResponse> res =
        client.emitWithWaitForResponse(
            BANACH_PLACE_BET,
            requestData,
            BANACH_PLACE_BET_SUCCESS,
            BANACH_PLACE_BET_RESPONSE_TYPE_REF);

    return res.getData().getBetPlacement().get(0);
  }

  @Test
  public void shouldReturnErrorWhenThereWasNoBanachSelectionBefore() {
    // given
    when(bppService.userData(new UserDataDto(BPP_TOKEN)))
        .thenReturn(generalResponseForUserData(OXI_TOKEN));

    // when
    Error error =
        client
            .emitWithWaitForResponse(
                BANACH_PLACE_BET,
                banachPlaceBetRequest(),
                BANACH_PLACE_BET_ERROR,
                RegularPlaceBetResponse.class)
            .getData()
            .getError();

    // then
    assertThat(error.getCode()).isEqualTo(ERROR_CODE.code());
    assertThat(error.getDescription())
        .isEqualTo("Exception on placing Banach Bet: Selection should be added first");
  }

  @Test
  public void shouldReturnErrorWhenBppReturnsResponseWithoutOxiToken() {
    // given
    String oxiToken = null;
    when(bppService.userData(new UserDataDto(BPP_TOKEN)))
        .thenReturn(generalResponseForUserData(oxiToken));

    // when
    Error error =
        client
            .emitWithWaitForResponse(
                BANACH_PLACE_BET,
                banachPlaceBetRequest(),
                BANACH_PLACE_BET_ERROR,
                RegularPlaceBetResponse.class)
            .getData()
            .getError();

    // then
    assertThat(error.getCode()).isEqualTo(UNAUTHORIZED_ACCESS.code());
    assertThat(error.getDescription()).isEqualTo("Token expired or user does not exist");
  }

  @Test
  public void shouldReturnErrorWhenBanachClientThrowsTimeoutException() {
    // given
    addBanachSelection();

    when(banachClient.execute(any(), any(PlaceBetRequestDto.class)))
        .thenThrow(new BanachTimeoutException("timeout"));
    when(bppService.userData(new UserDataDto(BPP_TOKEN)))
        .thenReturn(generalResponseForUserData(OXI_TOKEN));

    // when
    Error error =
        client
            .emitWithWaitForResponse(
                BANACH_PLACE_BET,
                banachPlaceBetRequest(),
                BANACH_PLACE_BET_ERROR,
                RegularPlaceBetResponse.class)
            .getData()
            .getError();

    // then
    assertThat(error.getCode()).isEqualTo(ERROR_CODE.code());
    assertThat(error.getDescription()).isEqualTo("Connection timeout");
  }

  private void addBanachSelection() {
    PriceResponse priceResponse = priceResponse(OK);
    when(selectionClient.execute(any(), any(GetPriceRequestDto.class))).thenReturn(priceResponse);
    client.emitWithWaitForResponse(
        ADD_BANACH_SELECTION,
        priceRequest(),
        ADD_BANACH_SELECTION_SUCCESS,
        BanachSelectionResponse.class);
  }

  private BanachPlaceBetRequestData banachPlaceBetRequest() {
    BanachPlaceBetRequestData banachPlaceBetRequestData = new BanachPlaceBetRequestData();
    banachPlaceBetRequestData.setToken(BPP_TOKEN);
    banachPlaceBetRequestData.setPrice("1/3");
    banachPlaceBetRequestData.setStake(String.valueOf(USER_STAKE));

    return banachPlaceBetRequestData;
  }

  private BanachPlaceBetRequestData banachPlaceBetRequestWithFreebet() {
    FreeBetRequest freeBetRequest = new FreeBetRequest();
    freeBetRequest.setStake(String.valueOf(FREEBET_STAKE));
    freeBetRequest.setId(1L);

    BanachPlaceBetRequestData banachPlaceBetRequestData = banachPlaceBetRequest();
    banachPlaceBetRequestData.setFreebet(freeBetRequest);

    return banachPlaceBetRequestData;
  }

  private PriceResponse priceResponse(GetPriceResponseDto.ResponseCodeEnum code) {
    GetPriceResponseDto getPriceResponseDto = new GetPriceResponseDto();
    getPriceResponseDto.setResponseCode(code);
    getPriceResponseDto.setPriceNum(1);
    getPriceResponseDto.setPriceDen(1);

    return new PriceResponse(getPriceResponseDto);
  }

  private BanachSelectionRequestData priceRequest() {
    BanachSelectionRequestData request = new BanachSelectionRequestData();
    request.setObEventId(1);
    request.setSelectionIds(asList(1L));

    return request;
  }

  private PlaceBetResponse placeBetResponse(BetPlacementResponseDto betPlacementResponseDto) {
    OxiReturnStatus oxiReturnStatus = new OxiReturnStatus();
    oxiReturnStatus.setCode("200");
    PlaceBetResponseDto placeBetResponseDto = new PlaceBetResponseDto();
    placeBetResponseDto.setOxiReturnStatus(oxiReturnStatus);
    placeBetResponseDto.setBetPlacement(Arrays.asList(betPlacementResponseDto));
    placeBetResponseDto.setResponseCode(PlaceBetResponseDto.ResponseCodeEnum.ACCEPTED);
    return new PlaceBetResponse(placeBetResponseDto);
  }

  private GeneralResponse<UserDataResponse> generalResponseForUserData(String oxiToken) {
    UserDataResponse userDataResponse = new UserDataResponse();
    userDataResponse.setOxiApiToken(oxiToken);

    return new GeneralResponse<>(userDataResponse, null);
  }

  private void assertPlacementsEquality(BetPlacementItem actual, BetPlacementResponseDto expected) {
    SoftAssertions softly = new SoftAssertions();
    softly.assertThat(actual.getBetId()).isEqualTo(expected.getBetId());
    softly.assertThat(actual.getBetNo()).isEqualTo(expected.getBetNo());
    softly.assertThat(actual.getDate()).isEqualTo(expected.getDate());
    softly.assertThat(actual.getNumLines()).isEqualTo(expected.getNumLines());
    softly.assertThat(actual.getTotalStake()).isEqualTo(expected.getTotalStake());
    softly.assertThat(actual.getReceipt()).isEqualTo(expected.getReceipt());
    softly.assertAll();
  }
}
