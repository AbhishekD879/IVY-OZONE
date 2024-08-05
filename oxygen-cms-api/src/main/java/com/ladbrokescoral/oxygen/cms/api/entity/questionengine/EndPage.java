package com.ladbrokescoral.oxygen.cms.api.entity.questionengine;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.experimental.Accessors;
import org.springframework.data.mongodb.core.mapping.Document;

@Data
@EqualsAndHashCode(callSuper = true)
@Document(collection = "endPage")
@Accessors(chain = true)
public class EndPage extends AbstractEntity implements HasBrand {

  @NotBlank private String title;

  @NotBlank private String brand;

  private Filename backgroundSvgImage;

  private String gameDescription;
  private String submitMessage;
  private String noLatestRoundMessage;
  private String noPreviousRoundMessage;
  private String upsellAddToBetslipCtaText;
  private String upsellBetInPlayCtaText;
  private String submitCta;

  private boolean showUpsell;
  private boolean showResults;
  private boolean showAnswersSummary;
  private boolean showPrizes;
  private String successMessage;
  private String errorMessage;
  private String redirectionButtonLabel;
  private String redirectionButtonUrl;
  private String bannerSiteCoreId;
}
