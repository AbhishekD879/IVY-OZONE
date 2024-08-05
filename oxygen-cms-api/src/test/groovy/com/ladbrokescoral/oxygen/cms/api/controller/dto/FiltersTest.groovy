package com.ladbrokescoral.oxygen.cms.api.controller.dto

import spock.lang.Specification

class FiltersSpecification extends Specification {
  private Filter<Integer> timeFilter
  private NamedLeagueIds namedLeagueIds
  private Filter<NamedLeagueIds> leagueFilter
  private Filters filters

  void setup() {
    timeFilter = Filter.builder()
        .enabled(true).values([1, 2, 3])
        .build()
    namedLeagueIds = NamedLeagueIds.builder()
        .leagueName("test")
        .leagueIds([123, 321]).build()
    leagueFilter = Filter.builder()
        .enabled(true)
        .values([this.namedLeagueIds])
        .build()

    filters = new Filters(this.timeFilter, this.leagueFilter)
  }

  def "When both filters are enabled and have data then simple filters view contains data"() {
    expect:
    def simple = this.filters.toSimplifiedFilters()
    simple.getLeague() == [this.namedLeagueIds]
    simple.getTime() == [1, 2, 3]
  }

  def "If filter is disabled then it's not in simple filter"() {
    timeFilter.setEnabled(false)
    leagueFilter.setEnabled(false)
    expect:
    def simple = filters.toSimplifiedFilters()
    simple.getLeague().isEmpty()
    simple.getTime().isEmpty()
  }

  def "If filter is enabled but data is null then simple filter is empty"() {
    timeFilter.setValues(null)
    leagueFilter.setValues(null)
    expect:
    def simple = filters.toSimplifiedFilters()
    simple.getLeague().isEmpty()
    simple.getTime().isEmpty()
  }

  def "If filter is enabled but data is empty list then simple filter is empty"() {
    timeFilter.setValues([])
    leagueFilter.setValues([])
    expect:
    def simple = filters.toSimplifiedFilters()
    simple.getLeague().isEmpty()
    simple.getTime().isEmpty()
  }
}
