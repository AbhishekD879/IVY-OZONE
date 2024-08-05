package com.ladbrokescoral.oxygen.cms.api.dto;

import com.ladbrokescoral.oxygen.cms.api.entity.*;
import lombok.Data;

@Data
public class AccaInsuranceMessageDto extends AbstractDto {
  private Boolean accInsMsgEnabled;
  private Boolean enabled;
  private String svgId;
  private String bsAddToQualifyMsg;
  private String bsQualifiedMsg;
  private Boolean bsqInfoIcon;
  private String avlblInscCountIndi;
  private Integer obAccaCount;
  private BetslipSpDto betslipSp;
  private AccabarSpDto accabarSp;
  private BetreceiptSpDto betreceiptSp;
  private MybetsSpDto mybetsSp;
  private String profitIndi;
  private String profitIndiUrl;
  private PopUpDetailsDto popUpDetails;
}
