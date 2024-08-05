package com.ladbrokescoral.oxygen.cms.api.service;

import java.time.Instant;
import lombok.AccessLevel;
import lombok.AllArgsConstructor;
import lombok.Builder;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@Builder
@AllArgsConstructor
@NoArgsConstructor(access = AccessLevel.PRIVATE)
public class IncompleteGameEvent {
  private String eventId;
  private Instant startTime;
  private String homeTeamName;
  private String awayTeamName;
}
