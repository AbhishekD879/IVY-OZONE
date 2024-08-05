package com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v3;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.ComplexSelection;
import io.vavr.collection.List;
import lombok.Value;

@Value
public class AddComplexSelectionRequest implements ComplexSelectionRequest {
  private List<String> outcomeIds;
  private ComplexSelection.Type selectionType;
}
