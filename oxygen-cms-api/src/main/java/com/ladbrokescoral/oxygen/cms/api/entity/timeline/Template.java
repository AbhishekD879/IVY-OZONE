package com.ladbrokescoral.oxygen.cms.api.entity.timeline;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import javax.validation.constraints.NotBlank;
import lombok.Data;
import lombok.EqualsAndHashCode;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "timelineTemplate")
@Data
@EqualsAndHashCode(callSuper = true)
public class Template extends AbstractTimelineEntity<Template>
    implements HasBrand, Auditable<Template> {

  @NotBlank private String brand;

  private String name;
  private boolean draft;
  private String postIconSvgId;
  private String headerIconSvgId;
  private String headerText;
  private String yellowHeaderText;
  private String subHeader;
  private String eventId;
  private String selectionId;
  private Filename topRightCornerImage;
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

  @Override
  public Template content() {
    return this;
  }
}
