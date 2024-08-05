package com.ladbrokescoral.oxygen.timeline.api.model;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonProperty;
import lombok.Data;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
public class Template {
  private String id;
  private String name;
  private String headerText;
  private String yellowHeaderText;
  private String subHeader;
  private String eventId;
  private String selectionId;
  private String price;
  private String text;
  private String betPromptHeader;
  private String postHref;

  @JsonProperty("isYellowSubHeaderBackground")
  private boolean isYellowSubHeaderBackground;

  private boolean showLeftSideRedLine;
  private boolean showLeftSideBlueLine;
  private boolean showTimestamp;
  private boolean showRedirectArrow;
  private boolean showRacingPostLogoInHeader;
  private String headerIconSvgId;
  private String postIconSvgId;
  private String topRightCornerImagePath;

  @JsonProperty("isSpotlightTemplate")
  private boolean isSpotlightTemplate;

  @JsonProperty("isVerdictTemplate")
  private boolean isVerdictTemplate;
}
