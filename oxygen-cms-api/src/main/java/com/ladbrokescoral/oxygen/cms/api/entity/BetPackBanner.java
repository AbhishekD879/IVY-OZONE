package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import javax.validation.constraints.NotNull;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.index.Indexed;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Data
@Document(collection = "betpack-banner")
@EqualsAndHashCode(callSuper = false)
@NoArgsConstructor
@JsonIgnoreProperties(ignoreUnknown = true)
public class BetPackBanner extends SortableEntity implements HasBrand {
  @NotNull private String welcomeMsg;

  @Indexed(unique = true)
  @NotNull
  private String brand;

  @NotNull private String termsAndCondition;
  @NotNull private String termsAndConditionLink;
  private Filename bannerImage;
  private String bannerImageFileName;
  @NotNull private boolean enabled;

  // OZONE-5901
  // Expiring Bet Bundle Token(s) Banners
  @NotNull private boolean bannerActiveInMarketPlace;
  private String marketPlaceImageFileName;
  private String marketPlaceBgImageFileName;
  private String bannerTextDescInMarketPlacePage;

  @NotNull private boolean bannerActiveInReviewPage;
  private String reviewPageImageFileName;
  private String reviewPageBgImageFileName;
  private String bannerTextDescInReviewPage;

  @NotNull private boolean expiresInActive;
  private String expiresInText;

  private String expiresInIconImage;
}
