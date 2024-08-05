package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class DataSelectionDto {
  private String selectionType;
  private String selectionId;

  public String getSelectionType() {
    return selectionType;
  }

  public void setSelectionType(String selectionType) {
    this.selectionType = selectionType;
  }

  public String getSelectionId() {
    return selectionId;
  }

  public void setSelectionId(String selectionId) {
    this.selectionId = selectionId;
  }
}
