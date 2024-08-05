package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonAutoDetect;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.SvgAbstractMenu;
import javax.validation.constraints.Min;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@JsonAutoDetect(fieldVisibility = JsonAutoDetect.Visibility.ANY)
@Document(collection = "odds-boost-configuration")
@Data
@EqualsAndHashCode(callSuper = true)
public class OddsBoostConfigEntity extends SortableEntity implements HasBrand, SvgAbstractMenu {

  private boolean enabled = false;
  private String loggedInHeaderText = "";
  private String loggedOutHeaderText = "";
  private String moreLink = "";
  private String lang = "en";
  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated private String svg = "";

  private String svgId;
  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated private SvgFilename svgFilename;

  private String termsAndConditionsText = "";
  @NotBlank private String brand;

  /**
   * properties @allowUserToToggleVisibility and @daysToKeepPopupHidden added to enable 'Don't show
   * me this again' feature toggle
   */
  private boolean allowUserToToggleVisibility = true;

  @Min(0)
  private int daysToKeepPopupHidden = 60;

  private String countDownTimer;
  private String noTokensText;
}
