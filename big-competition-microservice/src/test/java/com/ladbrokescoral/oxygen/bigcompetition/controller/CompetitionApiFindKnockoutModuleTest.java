package com.ladbrokescoral.oxygen.bigcompetition.controller;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.*;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.api.ExistsFilter;
import com.egalacoral.spark.siteserver.api.SimpleFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.bigcompetition.TestUtil;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.KnockoutModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.service.CmsApiService;
import com.ladbrokescoral.oxygen.bigcompetition.service.impl.StatsCenterApiServiceImpl;
import com.ladbrokescoral.oxygen.cms.client.model.Competition;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.http.HttpMethod;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class CompetitionApiFindKnockoutModuleTest {

  @Autowired private TestRestTemplate restTemplate;

  @MockBean private CmsApiService cmsApiServiceMock;

  @MockBean private SiteServerApi siteServerApiMock;

  @MockBean private StatsCenterApiServiceImpl statsCenterApiMock;

  @Test
  public void testFindKnockoutModule() {
    CompetitionModule competitionModule =
        TestUtil.deserializeWithJackson(
            "/competitionApi/knockoutModule/knockoutModule_from_cms.json", CompetitionModule.class);
    when(cmsApiServiceMock.findCompetitionModuleById("5acf86d1c9e77c000195ec18"))
        .thenReturn(Optional.of(competitionModule));

    List<Event> events =
        TestUtil.deserializeListWithJackson(
            "/competitionApi/knockoutModule/knockoutEvent_from_ss.json", Event.class);
    when(siteServerApiMock.getEventToOutcomeForEvent(
            eq(Collections.singletonList("6826779")),
            any(SimpleFilter.class),
            any(ExistsFilter.class),
            any(),
            any(),
            eq(false)))
        .thenReturn(Optional.of(events));

    Competition competition =
        TestUtil.deserializeWithJackson(
            "/competitionApi/knockoutModule/knockoutCompetition_from_cms.json", Competition.class);
    when(cmsApiServiceMock.findCompetitionByBrandAndUri("bma", "comp1"))
        .thenReturn(Optional.of(competition));

    when(statsCenterApiMock.getMatchDetails(anyString())).thenReturn(Optional.empty());

    KnockoutModuleDto expected =
        TestUtil.deserializeWithJackson(
            "/competitionApi/knockoutModule/knockoutModuleDto.json", KnockoutModuleDto.class);

    KnockoutModuleDto response =
        restTemplate.getForObject(
            "/competition/module/5acf86d1c9e77c000195ec18", KnockoutModuleDto.class);

    assertEquals(expected, response);
  }

  @Test
  public void testFindNotExistedKnockoutModule() {
    when(cmsApiServiceMock.findCompetitionModuleById("5acf86d1c9e77c000195ec18"))
        .thenReturn(Optional.empty());

    ResponseEntity<KnockoutModuleDto> response =
        restTemplate.exchange(
            "/competition/module/5acf86d1c9e77c000195ec18",
            HttpMethod.GET,
            null,
            KnockoutModuleDto.class);

    assertEquals(404, response.getStatusCode().value());
  }
}
