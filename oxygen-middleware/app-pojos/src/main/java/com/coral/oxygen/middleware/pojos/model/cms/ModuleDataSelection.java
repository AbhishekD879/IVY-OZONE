package com.coral.oxygen.middleware.pojos.model.cms;

import com.coral.oxygen.middleware.pojos.model.ChangeDetect;
import java.io.Serializable;

public class ModuleDataSelection implements Serializable {

  private String selectionId;

  private String selectionType;

  @ChangeDetect
  public String getSelectionId() {
    return selectionId;
  }

  public void setSelectionId(String selectionId) {
    this.selectionId = selectionId;
  }

  @ChangeDetect
  public String getSelectionType() {
    return selectionType;
  }

  public void setSelectionType(String selectionType) {
    this.selectionType = selectionType;
  }
}
