package com.ladbrokescoral.cashout.model;

import com.coral.bpp.api.exception.BppConnectionException;
import com.coral.bpp.api.exception.BppUnauthorizedException;
import com.ladbrokescoral.cashout.api.client.exception.OpenBetCashoutServiceConnectionException;
import com.ladbrokescoral.cashout.api.client.exception.OpenBetCashoutServiceFailedRequestException;
import com.ladbrokescoral.cashout.api.client.exception.OpenBetCashoutServiceFailedResponseException;
import com.ladbrokescoral.cashout.exception.BppFailedGetBetDetailsRequestException;

public enum Code {
  BET_PLACEMENT_CONNECTION_ERROR,
  UNAUTHORIZED_ACCESS,
  BET_PLACEMENT_FAILED_GET_BET_DETAILS_ERROR,
  OPEN_BET_CASHOUT_SERVICE_CONNECTION_ERROR,
  OPEN_BET_CASHOUT_SERVICE_FAILED_REQUEST_ERROR,
  OPEN_BET_CASHOUT_SERVICE_FAILED_RESPONSE_ERROR,
  UNKNOWN_SERVICE_ERROR,
  CASHOUT_BET_NO_CASHOUT,
  SUCCESS;

  public static Code fromException(Throwable t) {
    if (t instanceof OpenBetCashoutServiceConnectionException) {
      return Code.OPEN_BET_CASHOUT_SERVICE_CONNECTION_ERROR;
    } else if (t instanceof OpenBetCashoutServiceFailedRequestException) {
      return Code.OPEN_BET_CASHOUT_SERVICE_FAILED_REQUEST_ERROR;
    } else if (t instanceof OpenBetCashoutServiceFailedResponseException) {
      return Code.OPEN_BET_CASHOUT_SERVICE_FAILED_RESPONSE_ERROR;
    } else if (t instanceof BppUnauthorizedException) {
      return Code.UNAUTHORIZED_ACCESS;
    } else if (t instanceof BppConnectionException) {
      return Code.BET_PLACEMENT_CONNECTION_ERROR;
    } else if (t instanceof BppFailedGetBetDetailsRequestException) {
      return Code.BET_PLACEMENT_FAILED_GET_BET_DETAILS_ERROR;
    } else {
      return Code.UNKNOWN_SERVICE_ERROR;
    }
  }
}
