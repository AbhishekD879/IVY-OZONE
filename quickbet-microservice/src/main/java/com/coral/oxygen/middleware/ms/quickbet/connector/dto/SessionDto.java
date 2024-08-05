package com.coral.oxygen.middleware.ms.quickbet.connector.dto;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.BanachSelectionRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.CalculateOddsRequestDto;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.FreeBetForChannelRequestData;
import com.coral.oxygen.middleware.ms.quickbet.connector.dto.request.v2.RegularSelectionRequest;
import com.entain.oxygen.bettingapi.model.bet.api.request.BetRef;
import com.fasterxml.jackson.annotation.JsonCreator;
import com.fasterxml.jackson.annotation.JsonProperty;
import io.vavr.collection.HashMap;
import io.vavr.collection.List;
import io.vavr.collection.Map;
import java.io.Serializable;
import java.util.UUID;
import lombok.Data;

@Data
public final class SessionDto implements Serializable {
  private String sessionId;
  private RegularSelectionRequest regularSelectionRequest;
  private List<CalculateOddsRequestDto> oddsRequest;
  private BanachSelectionRequestData banachSelectionRequestData;
  private FreeBetForChannelRequestData freeBetForChannelRequestData;
  private List<String> selectedOutcomeIds;
  private List<ComplexSelection> complexSelections;
  private String token;
  private Map<UUID, List<BetRef>> betsToReadInBackground;

  @JsonCreator
  public SessionDto(@JsonProperty("sessionId") String sessionId) {
    this.sessionId = sessionId;
    this.complexSelections = List.empty();
    this.selectedOutcomeIds = List.empty();
    this.betsToReadInBackground = HashMap.empty();
  }
}
