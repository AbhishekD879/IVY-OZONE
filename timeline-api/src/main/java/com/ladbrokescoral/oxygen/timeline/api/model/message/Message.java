package com.ladbrokescoral.oxygen.timeline.api.model.message;

import com.fasterxml.jackson.annotation.JsonIgnoreProperties;
import com.fasterxml.jackson.annotation.JsonSubTypes;
import com.fasterxml.jackson.annotation.JsonTypeInfo;
import java.time.Instant;
import lombok.Data;
import lombok.EqualsAndHashCode;
import lombok.Getter;
import lombok.RequiredArgsConstructor;
import lombok.experimental.Accessors;
import org.apache.commons.lang3.StringUtils;

@Data
@JsonIgnoreProperties(ignoreUnknown = true)
@JsonSubTypes({
  @JsonSubTypes.Type(value = CampaignMessage.class, name = "CAMPAIGN"),
  @JsonSubTypes.Type(value = ChangeCampaignMessage.class, name = "CHANGE_CAMPAIGN"),
  @JsonSubTypes.Type(value = RemoveCampaignMessage.class, name = "REMOVE_CAMPAIGN"),
  @JsonSubTypes.Type(value = PostMessage.class, name = "POST"),
  @JsonSubTypes.Type(value = ChangePostMessage.class, name = "CHANGE_POST"),
  @JsonSubTypes.Type(value = RemovePostMessage.class, name = "REMOVE_POST"),
  @JsonSubTypes.Type(value = TimelineConfigMessage.class, name = "TIMELINE_CONFIG"),
})
@Accessors(chain = true)
@JsonTypeInfo(use = JsonTypeInfo.Id.NAME, property = "type")
public abstract class Message {
  private String id;
  private Instant createdDate;
  private String brand;

  public TimeBasedId timeBasedId() {
    return new TimeBasedId(id, createdDate);
  }

  public String getId() {
    return id;
  }

  public Instant getCreatedDate() {
    return createdDate;
  }

  public String getBrand() {
    return brand;
  }

  @Getter
  @EqualsAndHashCode
  @RequiredArgsConstructor
  public static class TimeBasedId {
    private final String id;
    private final Instant timestamp;

    public boolean isNotEmpty() {
      return StringUtils.isNotEmpty(id) && timestamp != null;
    }
  }
}
