package com.egalacoral.spark.timeform.actions;

import com.egalacoral.spark.timeform.api.tools.Tools;
import java.text.SimpleDateFormat;
import java.util.Date;
import org.slf4j.LoggerFactory;

public class DatedAction extends ChainedAction {

  private final ActionCalendar calendar;

  private final String name;

  private Date requestedTime;

  public DatedAction(Date requestedTime, ActionCalendar calendar, String name) {
    super();
    this.calendar = calendar;
    this.name = name;
    this.requestedTime = requestedTime;
    addOnSuccess(this::success);
    addOnError(this::error);
  }

  private void success() {
    calendar.setSuccess(getOperationName());
    LoggerFactory.getLogger(getClass()).info("Success operation {}", getOperationName());
  }

  private void error(Exception e) {
    LoggerFactory.getLogger(getClass()).error("Failed operation {}", getOperationName());
  }

  public void forceSuccessRemove() {
    calendar.removeSuccess(getOperationName());
    LoggerFactory.getLogger(getClass()).info("Remove operation {}", getOperationName());
  }

  protected String getOperationName() {
    SimpleDateFormat simpleDateFormat = Tools.simpleDateFormat("yyyy-MM-dd");
    return new StringBuilder(name)
        .append(" at ")
        .append(simpleDateFormat.format(requestedTime))
        .toString();
  }

  public ChainedAction ifWasNotPerformed() {

    class IfWasNotPerformedAction extends ChainedAction {
      public IfWasNotPerformedAction() {
        setAction(
            (chainedWrapper) -> {
              Date lastSuccess = calendar.lastSuccess(getOperationName());
              if (lastSuccess == null) {
                delegate(DatedAction.this);
              } else {
                LoggerFactory.getLogger(DatedAction.this.getClass())
                    .debug(
                        "Operation {} was already performed at {}",
                        getOperationName(),
                        lastSuccess);
              }
            });
      };
    }

    return new IfWasNotPerformedAction();
  }

  public ChainedAction ifWasBefore(DatedAction otherAction) {

    class IfWasBeforeAction extends ChainedAction {
      public IfWasBeforeAction() {
        setAction(
            (chainedWrapper) -> {
              Date lastSuccess = calendar.lastSuccess(getOperationName());
              Date lastOtherSuccess = calendar.lastSuccess(otherAction.getOperationName());
              if (lastOtherSuccess == null) {
                LoggerFactory.getLogger(DatedAction.this.getClass())
                    .debug("Operation {} was not performed yet", otherAction.getOperationName());
                return;
              } else if (lastSuccess == null) {
                delegate(DatedAction.this);
              } else if (!lastSuccess.after(lastOtherSuccess)) {
                delegate(DatedAction.this);
              } else {
                LoggerFactory.getLogger(DatedAction.this.getClass())
                    .debug(
                        "Operation {} was already performed at {} after {} at {}",
                        getOperationName(),
                        lastSuccess,
                        otherAction.getOperationName(),
                        lastOtherSuccess);
              }
            });
      };
    }

    return new IfWasBeforeAction();
  }
}
