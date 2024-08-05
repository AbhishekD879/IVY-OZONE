package com.ladbrokescoral.oxygen.bigcompetition.service;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.bigcompetition.TestUtil;
import com.ladbrokescoral.oxygen.bigcompetition.dto.siteServe.EventDto;
import com.ladbrokescoral.oxygen.bigcompetition.service.impl.CompetitionParticipantServiceImpl;
import com.ladbrokescoral.oxygen.cms.client.model.Competition;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
// @Ignore
public class CompetitionParticipantServiceTest {

  @Mock private CmsApiService cmsApiServiceMock;

  private CompetitionParticipantService competitionParticipantService;

  @Before
  public void setUp() throws Exception {
    competitionParticipantService = new CompetitionParticipantServiceImpl(cmsApiServiceMock, "bma");
  }

  @Test
  public void testPopulateEventWithParticipants() {
    Competition competition =
        TestUtil.deserializeWithJackson(
            "/competitionParticipantService/competition_from_cms.json", Competition.class);
    when(cmsApiServiceMock.findCompetitionByBrandAndUri("bma", "comp"))
        .thenReturn(Optional.of(competition));

    EventDto eventDto =
        TestUtil.deserializeWithJackson(
            "/competitionParticipantService/eventDto.json", EventDto.class);
    when(cmsApiServiceMock.findCompetitionByBrandAndUri("bma", "comp"))
        .thenReturn(Optional.of(competition));

    EventDto expected =
        TestUtil.deserializeWithJackson(
            "/competitionParticipantService/eventDtoWithParticipants.json", EventDto.class);

    EventDto result = competitionParticipantService.populateEventWithParticipants(eventDto, "comp");
    assertEquals(expected, result);
  }
}
