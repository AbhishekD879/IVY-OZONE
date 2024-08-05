package com.ladbrokescoral.oxygen.bigcompetition.service;

import static org.mockito.ArgumentMatchers.any;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.ArgumentMatchers.eq;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.model.Aggregation;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.betradar.client.entity.Match;
import com.ladbrokescoral.oxygen.bigcompetition.TestUtil;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.KnockoutModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.knockout.CompetitionKnockoutEventDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.MatchDetailsDtoMapper;
import com.ladbrokescoral.oxygen.bigcompetition.service.impl.module.KnockoutModuleServiceImpl;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionKnockoutModuleData;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CompetitionKnockoutServiceTest {

  @Mock SiteServeApiService siteServerApiMock;
  @Mock CompetitionParticipantService participantServiceMock;
  @Mock StatsCenterApiService statsCenterApiService;

  private MatchDetailsDtoMapper matchDetailsMapper = new MatchDetailsDtoMapper();
  private KnockoutModuleService service;

  @Before
  public void setUp() {
    service =
        new KnockoutModuleServiceImpl(
            statsCenterApiService, siteServerApiMock, participantServiceMock, matchDetailsMapper);
  }

  @Test
  public void testObMEventMarkets() {

    CompetitionModule competitionModule =
        TestUtil.deserializeWithJackson(
            "/competitionKnockoutService/competitionModuleDto.json", CompetitionModule.class);
    CompetitionKnockoutModuleData knockoutModuleData =
        TestUtil.deserializeWithJackson(
            "/competitionKnockoutService/knockoutEventDto.json",
            CompetitionKnockoutModuleData.class);
    competitionModule.setKnockoutModuleData(knockoutModuleData);
    Event event1 =
        TestUtil.deserializeWithJackson(
            "/competitionKnockoutService/ssObEvent_1.json", Event.class);
    when(siteServerApiMock.getEventWithOutcomesForEventKnockout("8208403"))
        .thenReturn(Optional.of(event1));

    CompetitionKnockoutEventDto participant1 =
        TestUtil.deserializeWithJackson(
            "/competitionKnockoutService/participant1.json", CompetitionKnockoutEventDto.class);
    when(participantServiceMock.populateKnockoutEventWithParticipant(any(), eq("world-cup")))
        .thenReturn(participant1);

    List<Aggregation> aggregations =
        TestUtil.deserializeListWithJackson(
            "/competitionKnockoutService/ssMarketsCount.json", Aggregation.class);
    when(siteServerApiMock.getMarketsCountForEvents(Arrays.asList(8208403)))
        .thenReturn(Optional.of(aggregations));

    KnockoutModuleDto moduleDto = (KnockoutModuleDto) service.process(competitionModule);

    moduleDto
        .getKnockoutEvents()
        .forEach(
            event -> {
              Assert.assertTrue(event.getObEvent().getMarkets().size() == 1);
              Assert.assertTrue(event.getObEvent().getMarketsCount() != null);
            });
  }

  @Test
  public void testKnockoutPostMatchResult() {
    Match match =
        TestUtil.deserializeWithJackson(
            "/competitionKnockoutService/scMatchDetails.json", Match.class);
    when(statsCenterApiService.getMatchDetails("8272981")).thenReturn(Optional.of(match));

    CompetitionModule competitionModule =
        TestUtil.deserializeWithJackson(
            "/competitionKnockoutService/competitionModuleDto_postMatch.json",
            CompetitionModule.class);
    CompetitionKnockoutModuleData knockoutModuleData =
        TestUtil.deserializeWithJackson(
            "/competitionKnockoutService/knockoutEventDto_postMatch.json",
            CompetitionKnockoutModuleData.class);
    competitionModule.setKnockoutModuleData(knockoutModuleData);
    Event event1 =
        TestUtil.deserializeWithJackson(
            "/competitionKnockoutService/ssObEvent_postMatch.json", Event.class);
    when(siteServerApiMock.getEventWithOutcomesForEventKnockout("8272981"))
        .thenReturn(Optional.of(event1));

    CompetitionKnockoutEventDto participant1 =
        TestUtil.deserializeWithJackson(
            "/competitionKnockoutService/participant_postMatch.json",
            CompetitionKnockoutEventDto.class);

    when(participantServiceMock.populateKnockoutEventWithParticipant(any(), anyString()))
        .thenReturn(participant1);

    KnockoutModuleDto moduleDto = (KnockoutModuleDto) service.process(competitionModule);

    CompetitionKnockoutEventDto knockoutEventDto = moduleDto.getKnockoutEvents().get(0);
    Assert.assertTrue(knockoutEventDto.isResulted());
    Assert.assertTrue(knockoutEventDto.getResult() != null);
    Assert.assertTrue(knockoutEventDto.getResult().getScore().length == 2);
    Assert.assertTrue(knockoutEventDto.getResult().getAet().length == 2);
    Assert.assertTrue(knockoutEventDto.getResult().getPen().length == 2);
    Assert.assertTrue(
        Boolean.valueOf(knockoutEventDto.getParticipants().get("HOME").getIsWinner()));
    Assert.assertFalse(
        Boolean.valueOf(knockoutEventDto.getParticipants().get("AWAY").getIsWinner()));
  }
}
