package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import javax.validation.constraints.NotBlank;
import javax.validation.constraints.NotNull;
import lombok.AccessLevel;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Data
@Document(collection = "betpack-label")
@EqualsAndHashCode(callSuper = false)
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class BetPackLabel extends BetPackLabelExt implements HasBrand {
  @Indexed(unique = true)
  @NotBlank
  private String brand;

  @NotBlank private String buyButtonLabel;
  @NotBlank private String buyBetPackLabel;
  @NotBlank private String gotoMyBetPacksLabel;
  @NotBlank private String depositMessage;
  @NotBlank private String maxBetPackPerDayBannerLabel;
  @NotBlank private String betPackAlreadyPurchasedPerDayBannerLabel;
  @NotBlank private String betPackMarketplacePageTitle;
  @NotBlank private String errorTitle;
  @NotBlank private String errorMessage;
  @NotBlank private String goToBettingLabel;
  @NotBlank private String goBettingURL;
  @NotBlank private String moreInfoLabel;
  @NotBlank private String buyNowLabel;
  @NotBlank private String kycArcGenericMessage;

  private boolean isAllFilterPillMessageActive;
  private String allFilterPillMessage;

  @Getter(AccessLevel.NONE)
  @NotNull
  private boolean isDailyLimitBannerEnabled;

  @JsonProperty("isDailyLimitBannerEnabled")
  public boolean isDailyLimitBannerEnabled() {
    return isDailyLimitBannerEnabled;
  }

  @NotBlank private String comingSoon;
  private String comingSoonSvg;
}
