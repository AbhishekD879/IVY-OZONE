package com.egalacoral.spark.timeform.api.connectivity;

import com.egalacoral.spark.timeform.api.TimeFormException;

public interface FailOverStrategy {

  public enum FailOverAction {
    RETRY,
    RELOGIN_AND_RETRY,
  }

  FailOverAction onError(TimeFormException e, int retryNumber);

  FailOverAction onReloginError(TimeFormException e, int retryNumber);

}
