package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.List;
import lombok.Data;

@Data
public class InitSignpostingDto {
  private String id;
  private String title;
  private String requestId;
  private String promoKey;
  private String promotionText;
  private String eventLevelFlag;
  private String marketLevelFlag;
  private List<String> showToCustomer;
  private List<Integer> vipLevels;
  private String templateMarketName;
  private String blurbMessage;
}
