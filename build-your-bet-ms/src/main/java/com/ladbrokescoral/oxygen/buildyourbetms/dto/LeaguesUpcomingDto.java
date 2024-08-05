package com.ladbrokescoral.oxygen.buildyourbetms.dto;

import com.ladbrokescoral.oxygen.byb.banach.dto.external.GetLeaguesResponseDto;
import java.util.ArrayList;
import java.util.List;
import lombok.Builder;
import lombok.Data;

@Data
@Builder
public class LeaguesUpcomingDto {
  @Builder.Default private List<GetLeaguesResponseDto> today = new ArrayList<>();
  @Builder.Default private List<GetLeaguesResponseDto> upcoming = new ArrayList<>();
}
