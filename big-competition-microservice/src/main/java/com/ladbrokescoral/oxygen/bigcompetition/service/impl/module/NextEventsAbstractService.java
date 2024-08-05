package com.ladbrokescoral.oxygen.bigcompetition.service.impl.module;

import static com.egalacoral.spark.siteserver.api.SiteServerApi.COMPETITION_OUTCOME_NAME_DELIMITERS;
import static com.ladbrokescoral.oxygen.bigcompetition.util.Utils.buildCompetitionParticipant;
import static java.util.stream.Collectors.toMap;

import com.egalacoral.spark.siteserver.model.Aggregation;
import com.ladbrokescoral.oxygen.bigcompetition.dto.ParticipantDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;
import com.ladbrokescoral.oxygen.bigcompetition.service.CmsApiService;
import com.ladbrokescoral.oxygen.bigcompetition.service.SiteServeApiService;
import com.ladbrokescoral.oxygen.cms.client.model.Competition;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionParticipant;
import java.util.*;
import java.util.stream.Collectors;
import lombok.AllArgsConstructor;

@AllArgsConstructor
public abstract class NextEventsAbstractService {

  private final SiteServeApiService siteServeApiService;
  private final CmsApiService cmsApiService;
  private final String brand;

  protected Set<EventDto> populateEventsWithParticipants(
      String competitionUri, Set<EventDto> events) {
    Optional<List<Aggregation>> aggregations =
        siteServeApiService.getMarketsCountForEvents(
            events.stream()
                .map(EventDto::getId)
                .map(Integer::valueOf)
                .collect(Collectors.toList()));

    List<CompetitionParticipant> participants =
        cmsApiService
            .findCompetitionByBrandAndUri(brand, competitionUri)
            .map(Competition::getCompetitionParticipants)
            .orElseGet(ArrayList::new);
    aggregations.ifPresent(
        s -> {
          Map<String, Integer> marketCountForEventMap =
              s.stream()
                  .collect(
                      toMap(item -> String.valueOf(item.getRefRecordId()), Aggregation::getCount));
          events.forEach(
              event -> {
                event.setMarketsCount(marketCountForEventMap.get(event.getId()));

                List<String> names =
                    Arrays.stream(
                            event
                                .getName()
                                .replace("|", "")
                                .split(COMPETITION_OUTCOME_NAME_DELIMITERS))
                        .map(String::trim)
                        .collect(Collectors.toList());
                if (names.size() == 2) {
                  getParticipantByName(names.get(0), participants)
                      .ifPresent(item -> event.getParticipants().put("HOME", item));
                  getParticipantByName(names.get(1), participants)
                      .ifPresent(item -> event.getParticipants().put("AWAY", item));
                }
              });
        });

    return events;
  }

  private Optional<ParticipantDto> getParticipantByName(
      String name, List<CompetitionParticipant> participants) {
    return Optional.ofNullable(buildCompetitionParticipant(participants, name));
  }
}
