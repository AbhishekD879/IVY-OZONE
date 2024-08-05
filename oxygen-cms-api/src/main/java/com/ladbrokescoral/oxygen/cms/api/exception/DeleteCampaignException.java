package com.ladbrokescoral.oxygen.cms.api.exception;

public class DeleteCampaignException extends RuntimeException {

  private static final long serialVersionUID = 1L;

  public DeleteCampaignException(String errorMessage) {
    super(errorMessage);
  }
}
