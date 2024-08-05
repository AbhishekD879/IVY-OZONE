package com.ladbrokescoral.oxygen.cms.api.dto;

import java.util.ArrayList;
import java.util.List;
import lombok.Data;
import lombok.EqualsAndHashCode;

@EqualsAndHashCode(callSuper = true)
@Data
public class SeasonDetailsDto extends SeasonDto {
  private boolean isGamificationLinked;
  private boolean isGameLinked;
  private List<String> gamesLinked = new ArrayList<>();
}
