package com.ladbrokescoral.oxygen.bigcompetition.controller;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.when;

import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Event;
import com.ladbrokescoral.oxygen.bigcompetition.TestUtil;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.CompetitionModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.service.CmsApiService;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionModule;
import java.util.List;
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
@Ignore
public class CompetitionApiFindModuleByIdWithOutrightsTest {

  @Autowired private TestRestTemplate restTemplate;

  @MockBean private CmsApiService cmsApiServiceMock;

  @MockBean private SiteServerApi siteServerApiMock;

  @Test
  public void testFindCompetitionModuleWithOutrights() throws Exception {
    CompetitionModule competitionModule =
        TestUtil.deserializeWithJackson(
            "/moduleByIdWithOutrights/competitionModule_from_cms.json", CompetitionModule.class);
    when(cmsApiServiceMock.findCompetitionModuleById("5aa78dbac9e77c00019b9718"))
        .thenReturn(Optional.of(competitionModule));

    List<Event> events =
        TestUtil.deserializeListWithJackson(
            "/moduleByIdWithOutrights/event_from_siteServe.json", Event.class);
    when(siteServerApiMock.getWholeEventToOutcomeForMarket("115295194", false))
        .thenReturn(Optional.of(events));

    CompetitionModuleDto response =
        restTemplate.getForObject(
            "/competition/module/5aa78dbac9e77c00019b9718", CompetitionModuleDto.class);

    CompetitionModuleDto expected =
        TestUtil.deserializeWithJackson(
            "/moduleByIdWithOutrights/competitionModuleDto.json", CompetitionModuleDto.class);

    assertEquals(expected, response);
  }
}
