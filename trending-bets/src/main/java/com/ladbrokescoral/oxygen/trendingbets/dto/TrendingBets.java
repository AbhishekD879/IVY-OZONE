package com.ladbrokescoral.oxygen.trendingbets.dto;

import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.annotation.JsonSerialize;
import com.fasterxml.jackson.databind.ser.std.DateSerializer;
import java.util.Date;
import java.util.List;

public record TrendingBets(
    @JsonProperty("event_type") String eventType,
    @JsonProperty("payload_type") String payloadType,
    @JsonProperty("application") String application,
    @JsonProperty("usecase") String usecase,
    @JsonProperty("sport") String sport,
    @JsonProperty("backed_within") String backedWithIn,
    @JsonProperty("event_starts_in") String eventStartIn,
    @JsonProperty("version") String version,
    @JsonProperty("last_update_utc") @JsonSerialize(using = DateSerializer.class) Date lastUpdate,
    @JsonProperty("frontend") String frontend,
    @JsonProperty("payload") List<TrendingItem> events) {}
