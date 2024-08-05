package com.ladbrokescoral.oxygen.cms.api.service.vault;

public class VaultException extends Exception {

  public VaultException() {}

  public VaultException(String message) {
    super(message);
  }

  public VaultException(String message, Throwable cause) {
    super(message, cause);
  }
}
