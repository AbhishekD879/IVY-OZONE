package com.egalacoral.spark.timeform.api.connectivity;

import com.egalacoral.spark.timeform.api.TimeFormException;

public class NoFailOverStrategy implements FailOverStrategy {
  @Override
  public FailOverAction onError(TimeFormException e, int retryNumber) {
    return null;
  }

  @Override
  public FailOverAction onReloginError(TimeFormException e, int retryNumber) {
    return null;
  }
}
