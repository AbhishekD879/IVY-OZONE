package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class FanzoneOptinEmailDto {

  private String brand;
  private String fanzoneEmailPopupTitle;
  private String fanzoneEmailPopupDescription;
  private String fanzoneEmailPopupOptIn;
  private String fanzoneEmailPopupRemindMeLater;
  private String fanzoneEmailPopupDontShowThisAgain;
}
