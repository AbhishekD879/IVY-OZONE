package com.coral.oxygen.middleware.ms.quickbet.util;

import com.coral.oxygen.middleware.ms.quickbet.Session;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.RegularPlaceBetResponse;
import com.coral.oxygen.middleware.ms.quickbet.impl.SiteServException;
import com.entain.oxygen.bettingapi.model.bet.api.common.YesNo;
import com.entain.oxygen.bettingapi.model.bet.api.response.*;
import io.vavr.control.Either;
import java.util.List;

public class ResponseUtils {

  private ResponseUtils() {
    throw new IllegalStateException("Utility class");
  }

  public static Either<RegularPlaceBetResponse, BetsResponse> handleErrors(
      GeneralResponse<BetsResponse> generalResponse) {
    ErrorBody errorBody = generalResponse.getErrorBody();
    if (errorBody != null) {
      return Either.left(createErrorResponse(errorBody));
    } else {
      BetsResponse body = generalResponse.getBody();
      List<BetError> betError = body.getBetError();
      if (betError != null && !betError.isEmpty()) {
        RegularPlaceBetResponse errorResponse = createErrorResponse(body);
        return Either.left(errorResponse);
      } else {
        return Either.right(body);
      }
    }
  }

  public static RegularPlaceBetResponse createErrorResponse(BetsResponse body) {
    return RegularPlaceBetResponse.errorResponse(body);
  }

  public static RegularPlaceBetResponse createErrorResponse(ErrorBody errorBody) {
    return RegularPlaceBetResponse.errorResponse(errorBody.getStatus(), errorBody.getError());
  }

  public static boolean isConfirmed(Bet bet) {
    return YesNo.Y.equals(bet.getIsConfirmed());
  }

  public static void sendSiteServerException(Session session, SiteServException e) {
    session.sendData(e.getMsg().code(), e.getResponse());
  }
}
