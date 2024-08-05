package com.ladbrokescoral.oxygen.cms.api.dto;

import lombok.Data;

@Data
public class OddsBoostMessageDto extends AbstractDto {
  private Boolean oddsBoostMsgEnabled;
  private String svgId;
  private String bsHeader;
  private String bsDesc;
  private Boolean infoIcon;
  private String brsp;
  private Boolean brspEnabled;
  private Boolean brDispBoostedPrice;
  private String mbsp;
  private Boolean mbspEnabled;
  private Boolean mbDispBoostedPrice;
  private String profitIndicator;
  private PopUpDetailsDto popUpDetails;
}
