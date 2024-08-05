package com.egalacoral.spark.timeform.api.connectivity;

import java.util.Arrays;
import java.util.Objects;
import java.util.Optional;

import com.egalacoral.spark.timeform.api.TimeFormException;
import com.egalacoral.spark.timeform.model.internal.DataResponse;

import com.google.gson.Gson;

public class RetryReloginFailOverStrategy implements FailOverStrategy {

  private final int retryCount;

  private final int reloginCount;

  public RetryReloginFailOverStrategy(int retryCount, int reloginCount) {
    this.retryCount = retryCount;
    this.reloginCount = reloginCount;
  }

  @Override
  public FailOverAction onError(TimeFormException e, int retryNumber) {
    if (retryNumber > retryCount) {
      return null;
    }
    if (e.getResponse() == null) {
      return FailOverAction.RETRY;
    }
    Optional<String> message = Arrays.asList(e.getResponse().body(), tryToParseRaw(e)).stream() //
            .filter(b -> b instanceof DataResponse<?>) //
            .map(b -> (DataResponse) b) //
            .map(DataResponse::getError) //
            .filter(Objects::nonNull) //
            .map(DataResponse.Error::getMessage) //
            .filter(Objects::nonNull) //
            .map(DataResponse.ErrorMessage::getValue) //
            .filter(Objects::nonNull) //
            .findFirst();
    if (message.isPresent() && message.get().toLowerCase().contains("authorization")) {
      return FailOverAction.RELOGIN_AND_RETRY;
    } else {
      return FailOverAction.RETRY;
    }
  }

  private DataResponse<Object> tryToParseRaw(TimeFormException tfe) {
    try {
      DataResponse dataResponse = new Gson().fromJson(tfe.getMessage(), DataResponse.class);
      return dataResponse;
    } catch (Exception e) {
      return null;
    }
  }

  @Override
  public FailOverAction onReloginError(TimeFormException e, int retryNumber) {
    return retryNumber > reloginCount ? null : FailOverAction.RETRY;
  }
}
