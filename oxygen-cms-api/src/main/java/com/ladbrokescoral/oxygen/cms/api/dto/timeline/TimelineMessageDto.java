package com.ladbrokescoral.oxygen.cms.api.dto.timeline;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import java.time.Instant;
import lombok.Data;
import lombok.experimental.Accessors;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonSubTypes({
  @JsonSubTypes.Type(value = TimelineCampaignDto.class, name = "CAMPAIGN"),
  @JsonSubTypes.Type(value = ChangeCampaignTimelineMessageDto.class, name = "CHANGE_CAMPAIGN"),
  @JsonSubTypes.Type(value = RemoveCampaignTimelineMessageDto.class, name = "REMOVE_CAMPAIGN"),
  @JsonSubTypes.Type(value = TimelinePostDto.class, name = "POST"),
  @JsonSubTypes.Type(value = ChangePostTimelineMessageDto.class, name = "CHANGE_POST"),
  @JsonSubTypes.Type(value = RemovePostTimelineMessageDto.class, name = "REMOVE_POST"),
})
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "type", include = JsonTypeInfo.As.PROPERTY)
@Accessors(chain = true)
public abstract class TimelineMessageDto {
  private String id;
  private Instant createdDate;
  private String brand;
}
