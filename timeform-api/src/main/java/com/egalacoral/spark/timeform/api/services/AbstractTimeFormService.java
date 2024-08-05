package com.egalacoral.spark.timeform.api.services;

import com.egalacoral.spark.timeform.api.TimeFormContext;

public abstract class AbstractTimeFormService {

  private final TimeFormContext context;

  public AbstractTimeFormService(TimeFormContext context) {
    this.context = context;
  }

  protected TimeFormContext getContext() {
    return context;
  }

}
