package com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2;

import java.util.Objects;

/** Created by azayats on 23.11.17. */
public class RegularSelectionRequestValidator implements RequestValidator<RegularSelectionRequest> {

  @Override
  public void validate(RegularSelectionRequest request) throws RequestValidationException {
    String selectionType = request.getSelectionType();
    if (Objects.isNull(selectionType)) {
      throw new RequestValidationException("selectionType is required");
    }
    switch (selectionType) {
      case RegularSelectionRequest.SIMPLE_SELECTION_TYPE:
        validateSimpleRequest(request);
        break;
      case RegularSelectionRequest.SCORECAST_SELECTION_TYPE:
        validateScorecastRequest(request);
        break;
      default:
        throw new RequestValidationException("Unsupported selection type '" + selectionType + "'");
    }
  }

  private void validateSimpleRequest(RegularSelectionRequest request)
      throws RequestValidationException {
    generalOutcomeIdsValidation(request, 1);
    if (Objects.nonNull(request.getAdditional())) {
      throw new RequestValidationException(
          "additional parameters aren't allowed for simple request");
    }
  }

  private void validateScorecastRequest(RegularSelectionRequest request)
      throws RequestValidationException {
    generalOutcomeIdsValidation(request, 2);
    RegularSelectionRequest.AdditionalParameters additional = request.getAdditional();
    if (Objects.isNull(additional) || Objects.isNull(additional.getScorecastMarketId())) {
      throw new RequestValidationException("additional.scorecastMarketId parameter is required");
    }
  }

  private void generalOutcomeIdsValidation(RegularSelectionRequest request, int requiredSize)
      throws RequestValidationException {
    if (Objects.isNull(request.getOutcomeIds())) {
      throw new RequestValidationException("outcomeIds is null");
    }
    if (request.getOutcomeIds().isEmpty()) {
      throw new RequestValidationException("empty outcomeIds");
    }
    if (request.getOutcomeIds().size() != requiredSize) {
      throw new RequestValidationException(
          request.getSelectionType() + " selection requires " + requiredSize + " outcomes");
    }
    for (int i = 0; i < request.getOutcomeIds().size(); i++) {
      if (Objects.isNull(request.getOutcomeIds().get(i))) {
        throw new RequestValidationException("null outcome id in element " + i);
      }
    }
  }
}
