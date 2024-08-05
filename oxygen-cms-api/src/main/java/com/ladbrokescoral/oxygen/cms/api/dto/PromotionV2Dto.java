package com.ladbrokescoral.oxygen.cms.api.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.List;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@NoArgsConstructor
@AllArgsConstructor
public class PromotionV2Dto {

  @JsonProperty("title")
  private String title;

  @JsonProperty("promoKey")
  private String promoKey;

  @JsonProperty("shortDescription")
  private String shortDescription;

  @JsonProperty("description")
  private String description;

  @JsonProperty("filename")
  private String filename;

  @JsonProperty("validityPeriodStart")
  private String validityPeriodStart;

  @JsonProperty("validityPeriodEnd")
  private String validityPeriodEnd;

  @JsonProperty("uriMedium")
  private String uriMedium;

  @JsonProperty("useDirectFileUrl")
  private Boolean useDirectFileUrl;

  @JsonProperty("directFileUrl")
  private String directFileUrl;

  @JsonProperty("widthMedium")
  private Integer widthMedium;

  @JsonProperty("heightMedium")
  private Integer heightMedium;

  @JsonProperty("showToCustomer")
  private List<String> showToCustomer;

  @JsonProperty("vipLevels")
  private List<Integer> vipLevels;

  @JsonProperty("disabled")
  private Boolean disabled;

  @JsonProperty("htmlMarkup")
  private String htmlMarkup;

  @JsonProperty("promotionText")
  private String promotionText;

  private String eventLevelFlag;

  private String marketLevelFlag;

  private String overlayBetNowUrl;

  private Boolean isSignpostingPromotion;

  @JsonProperty("popupTitle")
  private String popupTitle;

  private String promotionId;

  private String openBetId;

  private Boolean useCustomPromotionName;

  private String customPromotionName;

  private String navigationGroupId;

  private String templateMarketName;
  private String blurbMessage;
}
