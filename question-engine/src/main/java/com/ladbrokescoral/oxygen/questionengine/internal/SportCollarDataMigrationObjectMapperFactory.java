package com.ladbrokescoral.oxygen.questionengine.internal;

import com.fasterxml.jackson.annotation.JsonFormat;
import com.fasterxml.jackson.annotation.JsonProperty;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.ladbrokescoral.oxygen.questionengine.configuration.ObjectMapperFactory;
import com.ladbrokescoral.oxygen.questionengine.thirdparty.bigquery.model.BigQueryEntries;
import lombok.AccessLevel;
import lombok.NoArgsConstructor;

import java.time.Instant;

@NoArgsConstructor(access = AccessLevel.PRIVATE)
public final class SportCollarDataMigrationObjectMapperFactory {
  public static ObjectMapper getInstance() {
    return ObjectMapperFactory.getInstance()
        .addMixIn(BigQueryEntries.class, RawBigQueryEntries.class);
  }

  private abstract static class RawBigQueryEntries {

    @JsonProperty("Brand")
    String brand;

    @JsonProperty("Game")
    String game;

    @JsonProperty("GameID")
    String gameId;

    @JsonProperty("GameStartDate")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss", timezone = "UTC")
    Instant gameStartDate;

    @JsonProperty("GameEndDate")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss", timezone = "UTC")
    Instant gameEndDate;

    @JsonProperty("CustomerID")
    String customerId;

    @JsonProperty("Username")
    String username;

    @JsonProperty("CreatedDate")
    @JsonFormat(shape = JsonFormat.Shape.STRING, pattern = "yyyy-MM-dd'T'HH:mm:ss", timezone = "UTC")
    Instant createdDate;

    @JsonProperty("EventID")
    String eventId;

    @JsonProperty("Predictions")
    String predictions;
  }
}
