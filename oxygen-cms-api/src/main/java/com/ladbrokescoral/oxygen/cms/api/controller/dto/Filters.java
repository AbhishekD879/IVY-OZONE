package com.ladbrokescoral.oxygen.cms.api.controller.dto;

import com.fasterxml.jackson.annotation.JsonIgnore;
import com.fasterxml.jackson.annotation.JsonInclude;
import com.fasterxml.jackson.annotation.JsonInclude.Include;
import com.ladbrokescoral.oxygen.cms.api.controller.dto.PublicApiFilters.PublicApiFiltersBuilder;
import java.util.Optional;
import lombok.AllArgsConstructor;
import lombok.Data;
import lombok.NoArgsConstructor;

@Data
@AllArgsConstructor
@NoArgsConstructor
@JsonInclude(Include.NON_EMPTY)
public class Filters {

  private Filter<Integer> time;
  private Filter<NamedLeagueIds> league;

  @JsonIgnore
  public PublicApiFilters toSimplifiedFilters() {
    PublicApiFiltersBuilder builder = PublicApiFilters.builder();

    Optional.ofNullable(time).map(Filter::getDataIfEnabled).ifPresent(builder::time);

    Optional.ofNullable(league).map(Filter::getDataIfEnabled).ifPresent(builder::league);

    return builder.build();
  }
}
