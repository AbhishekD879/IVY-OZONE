package com.ladbrokescoral.oxygen.bigcompetition.controller;

import static org.junit.Assert.*;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.bigcompetition.TestUtil;
import com.ladbrokescoral.oxygen.bigcompetition.dto.*;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.CompetitionModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.service.CmsApiService;
import com.ladbrokescoral.oxygen.cms.client.model.*;
import java.util.Collections;
import java.util.Map;
import java.util.Optional;
import org.junit.Ignore;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.boot.test.web.client.TestRestTemplate;
import org.springframework.test.context.junit4.SpringRunner;

@RunWith(SpringRunner.class)
@SpringBootTest(webEnvironment = SpringBootTest.WebEnvironment.RANDOM_PORT)
public class CompetitionApiTest {

  @Autowired private TestRestTemplate restTemplate;

  @MockBean private CmsApiService cmsApiServiceMock;

  @Test
  public void testFindCompetitionWithoutModules() throws Exception {
    Competition competition =
        TestUtil.deserializeWithJackson(
            "/competitionApi/competition_from_cms.json", Competition.class);
    when(cmsApiServiceMock.findCompetitionByBrandAndUri("bma", "CompName"))
        .thenReturn(Optional.of(competition));

    CompetitionDto response =
        restTemplate.getForObject("/competition/CompName", CompetitionDto.class);

    CompetitionDto expected =
        TestUtil.deserializeWithJackson(
            "/competitionApi/competitionDto.json", CompetitionDto.class);
    assertEquals(expected, response);
  }

  @Test
  public void testFindCompetitionTab() throws Exception {
    CompetitionTab competitionTab =
        TestUtil.deserializeWithJackson(
            "/competitionApi/competition_from_cms.json", CompetitionTab.class);
    when(cmsApiServiceMock.findCompetitionTabById("5a9fcdeec9e77c0001e5c54b"))
        .thenReturn(Optional.of(competitionTab));

    CompetitionTabDto response =
        restTemplate.getForObject(
            "/competition/tab/5a9fcdeec9e77c0001e5c54b", CompetitionTabDto.class);

    CompetitionTabDto expected =
        TestUtil.deserializeWithJackson(
            "/competitionApi/competitionDto.json", CompetitionTabDto.class);
    assertEquals(expected, response);
  }

  @Test
  public void testFindCompetitionSubTab() throws Exception {
    CompetitionSubTab competitionSubTab =
        TestUtil.deserializeWithJackson(
            "/competitionApi/competition_from_cms.json", CompetitionSubTab.class);
    when(cmsApiServiceMock.findCompetitionSubTabById("5a9fce09c9e77c0001eeaec6"))
        .thenReturn(Optional.of(competitionSubTab));

    CompetitionSubTabDto response =
        restTemplate.getForObject(
            "/competition/subtab/5a9fce09c9e77c0001eeaec6", CompetitionSubTabDto.class);

    CompetitionSubTabDto expected =
        TestUtil.deserializeWithJackson(
            "/competitionApi/competitionDto.json", CompetitionSubTabDto.class);
    assertEquals(expected, response);
  }

  @Test
  @Ignore
  public void testFindCompetitionModule() throws Exception {
    CompetitionModule competitionModule =
        TestUtil.deserializeWithJackson(
            "/competitionApi/competitionModule_from_cms.json", CompetitionModule.class);
    when(cmsApiServiceMock.findCompetitionModuleById("5a9fce48c9e77c0001045f97"))
        .thenReturn(Optional.of(competitionModule));

    CompetitionModuleDto response =
        restTemplate.getForObject(
            "/competition/module/5a9fce48c9e77c0001045f97", CompetitionModuleDto.class);

    CompetitionModuleDto expected =
        TestUtil.deserializeWithJackson(
            "/competitionApi/competitionModuleDto.json", CompetitionModuleDto.class);
    assertEquals(expected, response);
  }

  @Test
  public void testFindCompetitionParticipants() {
    Competition competition =
        TestUtil.deserializeWithJackson(
            "/competitionApi/competitionParticipants.json", Competition.class);
    when(cmsApiServiceMock.findCompetitionByBrandAndUri("bma", "Comp"))
        .thenReturn(Optional.of(competition));
    Map result = this.restTemplate.getForObject("/competition/Comp/participant", Map.class);
    System.out.println(result);
    assertNotNull(result);
    assertEquals(1, result.keySet().size());
  }

  @Test
  public void testFindCompetitionParticipantsEmpty() {
    Competition competition = new Competition();
    competition.setCompetitionParticipants(Collections.emptyList());
    when(cmsApiServiceMock.findCompetitionByBrandAndUri("bma", "Comp"))
        .thenReturn(Optional.of(competition));
    Map result = this.restTemplate.getForObject("/competition/Comp/participant", Map.class);
    assertEquals(4, result.keySet().size());
  }
}
