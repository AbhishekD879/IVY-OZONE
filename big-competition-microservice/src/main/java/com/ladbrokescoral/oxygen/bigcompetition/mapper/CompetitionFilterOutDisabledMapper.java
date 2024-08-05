package com.ladbrokescoral.oxygen.bigcompetition.mapper;

import com.ladbrokescoral.oxygen.cms.client.model.*;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.function.Function;
import java.util.stream.Collectors;

// FIXME: need rework. crazy code. use frameworks for mapping.
public class CompetitionFilterOutDisabledMapper {

  private CompetitionFilterOutDisabledMapper() {}

  public static Optional<Competition> filterOutDisabled(Competition competition) {
    return Optional.ofNullable(competition)
        .filter(Competition::isEnabled)
        .map(
            comp -> {
              comp.setCompetitionTabs(
                  mapListWithFilter(
                      comp.getCompetitionTabs(),
                      CompetitionFilterOutDisabledMapper::filterOutDisabled));
              return comp;
            });
  }

  public static Optional<Competition> filterOutDisabledWithOutModules(Competition competition) {
    return Optional.ofNullable(competition)
        .filter(Competition::isEnabled)
        .map(
            (Competition comp) -> {
              comp.setCompetitionTabs(
                  mapListWithFilter(
                      comp.getCompetitionTabs(),
                      CompetitionFilterOutDisabledMapper::filterOutDisabledWithOutModules));
              return comp;
            });
  }

  public static Optional<CompetitionTab> filterOutDisabledWithOutModules(
      CompetitionTab competitionTab) {
    return Optional.ofNullable(competitionTab)
        .filter(CompetitionTab::isEnabled)
        .map(
            (CompetitionTab tab) -> {
              tab.setCompetitionSubTabs(
                  mapListWithFilter(
                      tab.getCompetitionSubTabs(),
                      CompetitionFilterOutDisabledMapper::filterOutDisabledWithOutModules));
              return tab;
            })
        .map(
            (CompetitionTab tab) -> {
              tab.setCompetitionModules(Collections.emptyList());
              return tab;
            });
  }

  public static Optional<CompetitionSubTab> filterOutDisabledWithOutModules(
      CompetitionSubTab competitionSubTab) {
    return Optional.ofNullable(competitionSubTab)
        .filter(CompetitionSubTab::isEnabled)
        .map(
            (CompetitionSubTab subTab) -> {
              subTab.setCompetitionModules(Collections.emptyList());
              return subTab;
            });
  }

  public static Optional<CompetitionTab> filterOutDisabled(CompetitionTab competitionTab) {
    return Optional.ofNullable(competitionTab)
        .filter(CompetitionTab::isEnabled)
        .map(
            tab -> {
              tab.setCompetitionSubTabs(
                  mapListWithFilter(
                      tab.getCompetitionSubTabs(),
                      CompetitionFilterOutDisabledMapper::filterOutDisabled));
              return tab;
            })
        .map(
            tab -> {
              tab.setCompetitionModules(
                  mapListWithFilter(
                      tab.getCompetitionModules(),
                      CompetitionFilterOutDisabledMapper::filterOutDisabled));
              return tab;
            });
  }

  public static Optional<CompetitionSubTab> filterOutDisabled(CompetitionSubTab competitionSubTab) {
    return Optional.ofNullable(competitionSubTab)
        .filter(CompetitionSubTab::isEnabled)
        .map(
            subTab -> {
              subTab.setCompetitionModules(
                  mapListWithFilter(
                      subTab.getCompetitionModules(),
                      CompetitionFilterOutDisabledMapper::filterOutDisabled));
              return subTab;
            });
  }

  public static Optional<CompetitionModule> filterOutDisabled(CompetitionModule competitionModule) {
    return Optional.ofNullable(competitionModule)
        .filter(CompetitionModule::isEnabled)
        .map(
            module -> {
              module.setMarkets(
                  mapListWithFilter(
                      module.getMarkets(), CompetitionFilterOutDisabledMapper::filterOutDisabled));
              return module;
            });
  }

  public static Optional<CompetitionMarket> filterOutDisabled(CompetitionMarket competitionMarket) {
    return Optional.ofNullable(competitionMarket).filter(CompetitionMarket::isEnabled);
  }

  private static <T> List<T> mapListWithFilter(List<T> inputList, Function<T, Optional<T>> filter) {
    return inputList.stream()
        .map(filter)
        .filter(Optional::isPresent)
        .map(Optional::get)
        .collect(Collectors.toList());
  }
}
