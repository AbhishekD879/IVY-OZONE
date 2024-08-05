package com.oxygen.publisher.model;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import java.util.List;
import java.util.stream.Collectors;
import lombok.Data;

@Data
@JsonInclude(JsonInclude.Include.NON_NULL)
public class SportsRibbon {

  private List<SportsRibbonItem> items;

  @JsonIgnore
  public List<SportsRibbonItem> getItemsWithLiveStreams() {
    return items.stream()
        .filter(
            // filter elements without LiveStream events, remove All Sports section as it isn't
            // needed for UI
            sportsRibbonItem ->
                sportsRibbonItem.getHasLiveNow() && !sportsRibbonItem.getCategoryId().equals(0))
        .collect(Collectors.toList());
  }
}
