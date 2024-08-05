package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class FTPBetSharingDto {
  private boolean enable;
  private String header;
  private String subHeader;
  private String backgroundImageUrl;
  private String affiliateLink;
  private String playLabel;
  private List<TeamDetailsDto> teamDetails;
}
