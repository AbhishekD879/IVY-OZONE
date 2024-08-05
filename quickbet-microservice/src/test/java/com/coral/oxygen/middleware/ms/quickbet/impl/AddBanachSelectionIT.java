package com.coral.oxygen.middleware.ms.quickbet.impl;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.ADD_BANACH_SELECTION;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.ADD_BANACH_SELECTION_ERROR;
import static com.coral.oxygen.middleware.ms.quickbet.Messages.ADD_BANACH_SELECTION_SUCCESS;
import static com.coral.oxygen.middleware.ms.quickbet.util.BanachUtils.COMPONENT_SUSPENDED_ERROR_CODE;
import static com.coral.oxygen.middleware.ms.quickbet.util.BanachUtils.COMPONENT_SUSPENDED_ERROR_MESSAGE;
import static com.coral.oxygen.middleware.ms.quickbet.util.BanachUtils.INVALID_COMBINATION_ERROR_CODE;
import static com.coral.oxygen.middleware.ms.quickbet.util.BanachUtils.INVALID_COMBINATION_ERROR_MESSAGE;
import static com.coral.oxygen.middleware.ms.quickbet.util.BanachUtils.INVALID_MARGINATED_PRICE_ERROR_CODE;
import static com.coral.oxygen.middleware.ms.quickbet.util.BanachUtils.INVALID_MARGINATED_PRICE_ERROR_MESSAGE;
import static com.coral.oxygen.middleware.ms.quickbet.util.BanachUtils.UNKNOWN_ERROR_CODE;
import static com.coral.oxygen.middleware.ms.quickbet.util.BanachUtils.UNKNOWN_ERROR_MESSAGE;
import static com.ladbrokescoral.oxygen.byb.banach.dto.external.GetPriceResponseDto.ResponseCodeEnum.COMPONENT_SUSPENDED;
import static com.ladbrokescoral.oxygen.byb.banach.dto.external.GetPriceResponseDto.ResponseCodeEnum.INVALID_COMBINATION;
import static com.ladbrokescoral.oxygen.byb.banach.dto.external.GetPriceResponseDto.ResponseCodeEnum.INVALID_MARGINATED_PRICE;
import static com.ladbrokescoral.oxygen.byb.banach.dto.external.GetPriceResponseDto.ResponseCodeEnum.OK;
import static com.ladbrokescoral.oxygen.byb.banach.dto.external.GetPriceResponseDto.ResponseCodeEnum.UNKNOWN;
import static java.util.Arrays.asList;
import static org.assertj.core.api.Assertions.assertThat;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachSelectionRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.BanachSelectionResponse;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.ErrorMessage;
import com.coral.oxygen.middleware.ms.quickbet.utils.WebSocketTestClient;
import com.ladbrokescoral.oxygen.byb.banach.client.BlockingBanachClient;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetPriceRequestDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetPriceResponseDto;
import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetPriceResponseDto.ResponseCodeEnum;
import com.ladbrokescoral.oxygen.byb.banach.dto.internal.PriceResponse;
import java.util.function.Consumer;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.stubbing.OngoingStubbing;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@IntegrationTest
public class AddBanachSelectionIT {

  private static final String BANACH_CLIENT_ERROR = "banach client error";

  @Autowired private WebSocketTestClient client;

  @MockBean private BlockingBanachClient<GetPriceRequestDto, PriceResponse> priceClient;

  @Test
  public void shouldAddBanachSelection() throws Exception {
    // given
    int priceNum = 1;
    int priceDen = 3;
    long eventId = 555;
    long selectionId = 666;

    PriceResponse priceResponse = priceResponse(OK, priceNum, priceDen);
    when(priceClient.execute(any(), any(GetPriceRequestDto.class))).thenReturn(priceResponse);

    // when
    client.emit(ADD_BANACH_SELECTION, getPriceRequest(eventId, selectionId));
    BanachSelectionResponse response =
        client.wait(ADD_BANACH_SELECTION_SUCCESS, BanachSelectionResponse.class);

    // then
    assertThat(response.getRoomName()).isNotBlank();
    assertThat(response.getData().getPriceNum()).isEqualTo(priceNum);
    assertThat(response.getData().getPriceDen()).isEqualTo(priceDen);
  }

  @Test
  public void shouldReturnErrorWhenBanachClientThrowsException() throws Exception {
    shouldReturnErrorByThrowingException(
        "ERROR", "Failed to get price on Banach selection: " + BANACH_CLIENT_ERROR);
  }

  @Test
  public void shouldReturnErrorWhenBanachClientReturnsUnknown() throws Exception {
    shouldReturnErrorForStatus(UNKNOWN, UNKNOWN_ERROR_CODE, UNKNOWN_ERROR_MESSAGE);
  }

  @Test
  public void shouldReturnErrorWhenBanachClientReturnsInvalidCombination() throws Exception {
    shouldReturnErrorForStatus(
        INVALID_COMBINATION, INVALID_COMBINATION_ERROR_CODE, INVALID_COMBINATION_ERROR_MESSAGE);
  }

  @Test
  public void shouldReturnErrorWhenBanachClientReturnsInvalidComponentSuspended() throws Exception {
    shouldReturnErrorForStatus(
        COMPONENT_SUSPENDED, COMPONENT_SUSPENDED_ERROR_CODE, COMPONENT_SUSPENDED_ERROR_MESSAGE);
  }

  @Test
  public void shouldReturnErrorWhenBanachClientReturnsInvalidInvalidMarginatedPrice()
      throws Exception {
    shouldReturnErrorForStatus(
        INVALID_MARGINATED_PRICE,
        INVALID_MARGINATED_PRICE_ERROR_CODE,
        INVALID_MARGINATED_PRICE_ERROR_MESSAGE);
  }

  private void shouldReturnErrorByThrowingException(String errorCode, String errorMessage)
      throws Exception {
    shouldReturnError(
        errorCode,
        errorMessage,
        priceExecutionStubbing ->
            priceExecutionStubbing.thenThrow(new RuntimeException(BANACH_CLIENT_ERROR)));
  }

  private void shouldReturnErrorForStatus(
      ResponseCodeEnum responseCodeEnum, String errorCode, String errorMessage) throws Exception {
    shouldReturnError(
        errorCode,
        errorMessage,
        priceExecutionStubbing ->
            priceExecutionStubbing.thenReturn(priceResponse(responseCodeEnum)));
  }

  private void shouldReturnError(
      String errorCode,
      String errorMessage,
      Consumer<OngoingStubbing<PriceResponse>> priceExecutionStubbing)
      throws Exception {
    // given
    priceExecutionStubbing.accept(when(priceClient.execute(any(), any(GetPriceRequestDto.class))));

    // when
    client.emit(ADD_BANACH_SELECTION, getPriceRequest());
    ErrorMessage response = client.wait(ADD_BANACH_SELECTION_ERROR, ErrorMessage.class);

    // then
    assertThat(response.getCode()).isEqualTo(errorCode);
    assertThat(response.getMessage()).isEqualTo(errorMessage);
  }

  private PriceResponse priceResponse(ResponseCodeEnum code) {
    return priceResponse(code, 1, 1);
  }

  private PriceResponse priceResponse(ResponseCodeEnum code, int priceNum, int priceDen) {
    GetPriceResponseDto getPriceResponseDto = new GetPriceResponseDto();
    getPriceResponseDto.setResponseCode(code);
    getPriceResponseDto.setPriceNum(priceNum);
    getPriceResponseDto.setPriceDen(priceDen);

    return new PriceResponse(getPriceResponseDto);
  }

  private BanachSelectionRequestData getPriceRequest() {
    return getPriceRequest(1, 1);
  }

  private BanachSelectionRequestData getPriceRequest(long eventId, long selectionId) {
    BanachSelectionRequestData request = new BanachSelectionRequestData();
    request.setObEventId(eventId);
    request.setSelectionIds(asList(selectionId));

    return request;
  }
}
