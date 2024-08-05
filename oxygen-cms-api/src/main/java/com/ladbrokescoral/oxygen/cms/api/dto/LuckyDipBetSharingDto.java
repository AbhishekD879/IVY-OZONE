package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class LuckyDipBetSharingDto {
  private boolean enable;
  private String header;
  private String luckyDipLabel;
  private String backgroundImageUrl;
  private String luckyDipAffiliateLink;
  private String wonLabel;
  private String potentialReturnsLabel;
  private List<ShareCardDetailsDto> openBetControl;
  private List<ShareCardDetailsDto> lostBetControl;
  private List<ShareCardDetailsDto> wonBetControl;
}
