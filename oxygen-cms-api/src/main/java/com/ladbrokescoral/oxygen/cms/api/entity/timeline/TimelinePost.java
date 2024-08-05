package com.ladbrokescoral.oxygen.cms.api.entity.timeline;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.HasBrand;
import java.time.Instant;
import javax.validation.constraints.NotBlank;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.NoArgsConstructor;
import org.springframework.data.mongodb.core.index.CompoundIndex;
import org.springframework.data.mongodb.core.mapping.Document;

@Document(collection = "timelinePost")
@CompoundIndex(name = "brand_campaignId", def = "{'brand' : 1, 'campaignId': 1}")
@CompoundIndex(
    name = "brand_sorting_fields",
    def =
        "{'brand': 1, 'name': 1, 'template.name': 1, 'postStatus': 1, 'updatedByUserName': 1, 'updatedAt': 1}")
@Data
@EqualsAndHashCode(callSuper = true)
@AllArgsConstructor
@NoArgsConstructor
public class TimelinePost extends AbstractTimelineEntity<TimelinePost>
    implements HasBrand, Auditable<TimelinePost> {

  @NotBlank private String brand;

  private Template template;
  private String name;
  private String campaignId;
  private String campaignName;

  @JsonProperty("isSpotlight")
  private boolean isSpotlight;

  @JsonProperty("isVerdict")
  private boolean isVerdict;

  private PostStatus postStatus;

  private boolean pinned;

  private Instant publishedAt;

  @Override
  public TimelinePost content() {
    return this;
  }

  public TimelinePost unpublish() {
    setPostStatus(PostStatus.UNPUBLISHED);

    return this;
  }
}
