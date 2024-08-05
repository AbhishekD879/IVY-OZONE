package com.ladbrokescoral.oxygen.cms.api.exception;

public class CampaignAlreadyExistException extends RuntimeException {

  private static final long serialVersionUID = 1L;

  public CampaignAlreadyExistException(String errorMessage) {
    super(errorMessage);
  }
}
