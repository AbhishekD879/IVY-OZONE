package com.egalacoral.spark.timeform.actions;

import com.egalacoral.spark.timeform.service.ActionCalendarStorageService;
import java.util.Date;

public class ActionCalendarImpl implements ActionCalendar {

  private ActionCalendarStorageService calendarStorageService;

  public ActionCalendarImpl(ActionCalendarStorageService calendarStorageService) {
    this.calendarStorageService = calendarStorageService;
  }

  @Override
  public Date lastSuccess(String operationName) {
    return calendarStorageService.getValue(operationName);
  }

  @Override
  public void setSuccess(String operationName) {
    calendarStorageService.save(operationName, new Date());
  }

  @Override
  public void removeSuccess(String operationName) {
    calendarStorageService.deleteKey(operationName);
  }
}
