package com.ladbrokescoral.oxygen.cms.api.entity;

import com.fasterxml.jackson.annotation.JsonProperty;
import java.util.ArrayList;
import java.util.List;
import lombok.Data;

@Data
public class NextRacesResult {

  private Boolean ukAndIre;
  private List<NextRace> races = new ArrayList<>();

  @JsonProperty(value = "isUkAndIre")
  public Boolean getUkAndIre() {
    return ukAndIre;
  }
}
