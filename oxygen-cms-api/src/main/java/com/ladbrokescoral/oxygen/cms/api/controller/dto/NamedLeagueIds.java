package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import java.util.ArrayList;
import java.util.List;
import lombok.Builder;
import lombok.Builder.Default;
import lombok.Data;

@Data
@Builder
public class NamedLeagueIds {
  private String leagueName;
  @Default private List<Integer> leagueIds = new ArrayList<>();
}
