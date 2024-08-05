package com.ladbrokescoral.oxygen.cms.api.entity;

import java.util.List;
import lombok.Data;

@Data
public class FTPBetSharing {
  private boolean enable;
  private String header;
  private String subHeader;
  private String backgroundImageUrl;
  private String affiliateLink;
  private String playLabel;
  private List<TeamDetails> teamDetails;
}
