package com.ladbrokescoral.oxygen.cms.api.dto.timeline;

import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
public class TemplateDto {
  private String id;
  private String name;
  private String postIconSvgId;
  private String headerIconSvgId;
  private String headerText;
  private String yellowHeaderText;
  private String subHeader;
  private String eventId;
  private String selectionId;
  private String topRightCornerImagePath;
  private String price;
  private String betPromptHeader;
  private String postHref;
  private String text;

  @JsonProperty("isYellowSubHeaderBackground")
  private boolean isYellowSubHeaderBackground;

  private boolean showLeftSideRedLine;
  private boolean showLeftSideBlueLine;
  private boolean showTimestamp;
  private boolean showRedirectArrow;
  private boolean showRacingPostLogoInHeader;

  @JsonProperty("isSpotlightTemplate")
  private boolean isSpotlightTemplate;

  @JsonProperty("isVerdictTemplate")
  private boolean isVerdictTemplate;
}
