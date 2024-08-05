package com.ladbrokescoral.oxygen.bigcompetition.service;

import com.ladbrokescoral.oxygen.bigcompetition.dto.module.knockout.CompetitionKnockoutEventDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;

public interface CompetitionParticipantService {

  EventDto populateEventWithParticipants(EventDto event, String competitionUri);

  CompetitionKnockoutEventDto populateKnockoutEventWithParticipant(
      CompetitionKnockoutEventDto knockoutEventDto, String competitionUri);
}
