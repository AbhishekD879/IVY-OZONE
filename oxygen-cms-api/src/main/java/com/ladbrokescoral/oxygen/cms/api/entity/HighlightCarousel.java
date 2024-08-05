package com.ladbrokescoral.oxygen.cms.api.entity;

import com.ladbrokescoral.oxygen.cms.api.entity.menu.SvgAbstractMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.segment.AbstractSportSegmentEntity;
import com.ladbrokescoral.oxygen.cms.api.service.validators.DateRange;
import java.time.Instant;
import java.util.List;
import javax.validation.constraints.NotEmpty;
import javax.validation.constraints.NotNull;
import javax.validation.constraints.Pattern;
import lombok.Data;
import lombok.EqualsAndHashCode;

/**
 * Example JSON: { "id": "5bd1bcdac9e77c00018d2ed6", "displayFrom": "2029-10-11T14:37:07Z",
 * "displayTo": "2039-10-11T14:37:07Z", "title": "title", "disabled": true, "brand": "brandName",
 * "sortOrder": 1, "svg": "", "png": "", "limit": 4, "inPlay": true, "typeId": 2, "sportId" : 4,
 * "events": ["8715640"] * }
 */
@Data
@EqualsAndHashCode(callSuper = true)
@DateRange(startDateField = "displayFrom", endDateField = "displayTo")
public class HighlightCarousel extends AbstractSportSegmentEntity implements SvgAbstractMenu {

  @NotEmpty
  @Pattern(regexp = TITLE_PATTERN, message = "should not be empty and without %^*{}<>[]")
  private String title;

  @NotNull private Instant displayFrom;

  @NotNull private Instant displayTo;

  private Integer limit;

  @NotNull private Boolean inPlay = true;
  private Integer typeId;
  private List<String> typeIds;
  private List<String> events;

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
  private Boolean displayOnDesktop;

  private String displayMarketType;
}
