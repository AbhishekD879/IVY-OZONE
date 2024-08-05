package com.ladbrokescoral.oxygen.trendingbets.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.fasterxml.jackson.databind.ser.std.DateSerializer;
import java.util.Collections;
import java.util.Date;
import java.util.List;
import lombok.Data;

@Data
public class PersonalizedBets {

  @JsonProperty("_id")
  private String id;

  @JsonProperty("application")
  private String application;

  @JsonProperty("usecase")
  private String usecase;

  @JsonProperty("version")
  private String version;

  @JsonProperty("last_update_utc")
  @JsonSerialize(using = DateSerializer.class)
  private Date lastUpdate;

  @JsonProperty("frontend")
  private String frontend;

  @JsonProperty("user_rec_type")
  private String userRecordsType;

  @JsonProperty("payloads")
  private PersonalizedPayload payload;

  private static class PersonalizedPayload {
    @JsonProperty("personalized_recs")
    private List<TrendingItem> personalizedRecords;

    @JsonProperty("fanzone_widget_feed_1")
    private List<TrendingItem> fanzoneBets;

    @JsonProperty("fanzone_widget_feed_2")
    private List<TrendingItem> fanzoneOtherBets;
  }

  public List<TrendingItem> getPersonalizedRecords() {
    if (payload != null && payload.personalizedRecords != null) {
      return payload.personalizedRecords;
    }
    return Collections.emptyList();
  }

  public List<TrendingItem> getFanzoneYourTeam() {
    if (payload != null && payload.fanzoneBets != null) {
      return payload.fanzoneBets;
    }
    return Collections.emptyList();
  }

  public List<TrendingItem> getFanzoneOtherTeam() {
    if (payload != null && payload.fanzoneOtherBets != null) {
      return payload.fanzoneOtherBets;
    }
    return Collections.emptyList();
  }
}
