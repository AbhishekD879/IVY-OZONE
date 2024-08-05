package com.ladbrokescoral.cashout.model.safbaf;

import com.ladbrokescoral.cashout.service.SelectionData;
import java.util.Objects;

public interface HasStatus {

  String SUSPENDED_STATUS = "Suspended";
  String ACTIVE_STATUS = "Active";

  default boolean statusChanged() {
    return Objects.nonNull(getStatus());
  }

  default boolean isActivated() {
    return ACTIVE_STATUS.equalsIgnoreCase(getStatus());
  }

  default boolean isSuspended() {
    return SUSPENDED_STATUS.equalsIgnoreCase(getStatus());
  }

  default boolean applyCurrentUpdateStatusIfItExists(SelectionData selectionData) {
    if (this.isActivated()) {
      return changeStatus(selectionData, true);
    } else if (this.isSuspended()) {
      return changeStatus(selectionData, false);
    } else {
      return false;
    }
  }

  boolean changeStatus(SelectionData data, boolean newStatus);

  String getStatus();

  String reasonForUpdate();
}
