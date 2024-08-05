package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.List;
import lombok.Data;

@Data
public class LuckyDipBetSharing {
  private boolean enable;
  private String header;
  private String luckyDipLabel;
  private String backgroundImageUrl;
  private String luckyDipAffiliateLink;
  private String wonLabel;
  private String potentialReturnsLabel;
  private List<ShareCardDetails> openBetControl;
  private List<ShareCardDetails> lostBetControl;
  private List<ShareCardDetails> wonBetControl;
}
