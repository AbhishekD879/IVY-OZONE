package com.ladbrokescoral.oxygen.questionengine.exception;

public class QuizSubmissionException extends RuntimeException {

  private final transient Object[] errorBody;

  public QuizSubmissionException(String message, Object... errorBody) {
    super(message);
    this.errorBody = errorBody;
  }
  
  public Object[] getErrorBody() {
    return errorBody;
  }
}
