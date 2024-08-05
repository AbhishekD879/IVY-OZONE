package com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.ComplexSelection;
import io.vavr.collection.List;

public interface ComplexSelectionRequest {
  List<String> getOutcomeIds();

  ComplexSelection.Type getSelectionType();
}
