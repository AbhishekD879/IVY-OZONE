package com.egalacoral.spark.timeform.actions;

import java.util.Date;

public interface ActionCalendar {

  Date lastSuccess(String operationName);

  void setSuccess(String operationName);

  void removeSuccess(String operationName);
}
