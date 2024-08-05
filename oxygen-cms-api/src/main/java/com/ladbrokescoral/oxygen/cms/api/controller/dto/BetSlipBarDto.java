package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import javax.validation.constraints.Size;
import lombok.Data;

@Data
public class BetSlipBarDto {

  private String id;
  private Double sortOrder;
  private Boolean enableAddToBetSlipBar;
  private String betSlipBarBetsAddedDesc;
  private String betSlipBarCTALabel;
  private String betSlipBarDesc;
  private String betSlipBarRemoveBetsCTALabel;

  @Size(max = 50, message = "Description should be max of 50 chars")
  private String suspendedBetsDesc;

  @Size(max = 50, message = "Text should be max of 50 chars")
  private String suspendedBetsAddedText;

  private String nonLoginHeader;

  private String noBettingHeader;
  private String noBettingDesc;
  private String noBettingCTA;
  private String noBettingDescTitle;
}
