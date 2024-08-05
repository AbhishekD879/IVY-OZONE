package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.menu.SvgAbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.AbstractSportSegmentEntity;
import com.ladbrokescoral.oxygen.cms.api.service.validators.DateRange;
import java.math.BigInteger;
import java.time.Instant;
import java.util.Set;
import javax.validation.Valid;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * BMA-34866: Surface Bets - CMS UI ... And the create surface bet button 1. Position 2. Check box
 * to display on Highlights tab 3. Check box to display on EDP 4. Text box to enter the category ID
 * 5. Title of the surface bet 6. Strat time 7. End time 8. Delete option. ...
 *
 * <p>the surface bet module 1. Position 2. Check box to display on Highlights tab 3. Check box to
 * display on EDP 4. Text box to enter the category ID (Option to provide comma separated ID's) of
 * the SLP the surface bets should be displayed. 5. Option to upload the icon 6. Title of the
 * surface bet 7. Option to provide the content of the surface bet 8. Option to input the
 * comma-separated Event ID (When event ID has been input then the surface bet should be displayed
 * on all their EDP's) 9. Option to input the selection ID 10. Option to input was price 11. Option
 * to provide the scheduling of the surface bet
 */
@Data
@EqualsAndHashCode(callSuper = true)
@DateRange(startDateField = "displayFrom", endDateField = "displayTo")
public class SurfaceBet extends AbstractSportSegmentEntity implements SvgAbstractMenu {

  @NotEmpty
  @Pattern(regexp = TITLE_PATTERN, message = "should not be empty and without %^{}<>[]*")
  private String title;

  @NotNull private Instant displayFrom;
  @NotNull private Instant displayTo;
  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated private String svg;
  /**
   * @deprecated use SvgImages api to upload images and use update the menu endpoint to set the
   *     svgId delete after release-103.0.0 goes live (check with ui)
   */
  @Deprecated private SvgFilename svgFilename;

  private String svgId;
  private String content;

  private Boolean edpOn;
  private Boolean highlightsTabOn;
  private Set<Relation> references;
  @NotNull private BigInteger selectionId;
  @Valid private Price price;
  private String svgBgImgPath;
  private String contentHeader;
  private String svgBgId;
  private Boolean displayOnDesktop;
  private boolean isReactionsEnabled;

  @JsonProperty("isReactionsEnabled")
  public boolean isReactionsEnabled() {
    return isReactionsEnabled;
  }
}
