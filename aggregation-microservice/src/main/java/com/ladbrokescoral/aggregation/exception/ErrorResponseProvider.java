package com.ladbrokescoral.aggregation.exception;

import static com.ladbrokescoral.aggregation.model.ErrorMessages.NO_SUCH_ID;

public final class ErrorResponseProvider {

  private ErrorResponseProvider() {}

  public static void handleSilkUrlProviderError(String errorMessage) {
    errorMessage = errorMessage != null ? errorMessage.trim() : "";
    switch (errorMessage) {
      case NO_SUCH_ID:
        throw new BadRequestException(errorMessage);
      default:
        throw new RuntimeException("Error occurred while fetching silks: " + errorMessage);
    }
  }
}
