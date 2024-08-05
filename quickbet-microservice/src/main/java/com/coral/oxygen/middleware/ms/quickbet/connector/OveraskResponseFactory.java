package com.coral.oxygen.middleware.ms.quickbet.connector;

import static com.coral.oxygen.middleware.ms.quickbet.Messages.OVERASK_TIMEOUT_ERROR;

import com.coral.oxygen.middleware.ms.quickbet.Messages;
import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.ReceiptResponseDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.converter.BetToReceiptResponseDtoConverter;
import com.coral.oxygen.middleware.ms.quickbet.impl.SelectionOperations;
import com.entain.oxygen.bettingapi.model.bet.api.response.BetsResponse;
import com.entain.oxygen.bettingapi.model.bet.api.response.ErrorBody;
import java.util.Collection;

class OveraskResponseFactory {

  private final Session session;
  private final SelectionOperations selectionOperations;
  private final BetToReceiptResponseDtoConverter converter;

  OveraskResponseFactory(
      Session session,
      SelectionOperations selectionOperations,
      BetToReceiptResponseDtoConverter converter) {
    this.session = session;
    this.selectionOperations = selectionOperations;
    this.converter = converter;
  }

  void createSuccessOveraskResponse(Messages messages, BetsResponse body) {
    RegularPlaceBetResponse.Data data = new RegularPlaceBetResponse.Data();
    Collection<ReceiptResponseDto> dtoList = converter.convert(body.getBet());
    data.getReceipt().addAll(dtoList);

    session.sendData(messages.code(), new RegularPlaceBetResponse(data));
    selectionOperations.clearSelection(session);
  }

  void createErrorResponse(Messages messages, ErrorBody errorBody) {
    session.sendData(messages.code(), RegularPlaceBetResponse.errorResponse(errorBody));
  }

  void createTimeoutErrorResponse(Messages messages) {
    session.sendData(
        messages.code(),
        RegularPlaceBetResponse.errorResponse(
            OVERASK_TIMEOUT_ERROR.code(), "Overask pending is finished with timeout"));
  }
}
