package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertNull;
import static org.mockito.Mockito.doReturn;
import static org.mockito.Mockito.verify;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.Competition;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionParticipant;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.repository.CompetitionParticipantRepository;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class CompetitionParticipantServiceTest {

  @Mock private CompetitionService competitionService;
  @Mock private SvgImageParser svgImageParser;
  @Mock CompetitionParticipantRepository repository;
  CompetitionParticipantService service;
  Competition competition;
  CompetitionParticipant competitionParticipant;
  CompetitionParticipant existingCP;
  @Mock MultipartFile svgFile;
  @Mock Svg svg;

  @Before
  public void init() throws Exception {
    service = new CompetitionParticipantService(repository, competitionService, svgImageParser);

    competition = TestUtil.deserializeWithJackson("test/competition.json", Competition.class);
    existingCP = competition.getCompetitionParticipants().get(0);
    competitionParticipant = new CompetitionParticipant();
    competitionParticipant.setObName("newObName");
    competitionParticipant.setFullName("fullName");
    doReturn(competition).when(competitionService).save(competition);
    doReturn(competition).when(competitionService).getCompetitionByid(competition.getId());
    doReturn(existingCP)
        .when(competitionService)
        .getCompetitionParticipant(existingCP.getId(), competition);
    doReturn(Optional.of(existingCP)).when(repository).findById(existingCP.getId());
    doReturn(Optional.of(svg)).when(svgImageParser).parse(svgFile);
    doReturn("svgId").when(svg).getId();
    doReturn("svgValue").when(svg).getSvg();
  }

  @Test
  public void createCompetitionParticipantTest() {
    service.createCompetitionParticipant(competitionParticipant, competition.getId());
    verify(competitionService).save(competition);
  }

  @Test
  public void readCompetitionByCompetitionParticipantTest() {
    service.readCompetitionByCompetitionParticipant(competition.getId(), existingCP.getId());
    verify(competitionService).getCompetitionParticipant(existingCP.getId(), competition);
  }

  @Test
  public void deleteCompetitionParticipantFromCompetitionTest() {
    service.deleteCompetitionParticipantFromCompetition(competition.getId(), existingCP.getId());
    verify(competitionService).getCompetitionByid(competition.getId());
    verify(competitionService).save(competition);
  }

  @Test
  public void attachImageTest() {
    service.attachImage(existingCP.getId(), svgFile);
    verify(repository).findById(existingCP.getId());
    verify(svgImageParser).parse(svgFile);
    assertEquals(svg.getSvg(), existingCP.getSvg());
    assertEquals(svg.getId(), existingCP.getSvgId());
  }

  @Test
  public void removeImageTest() {
    service.removeImage(existingCP.getId());
    verify(repository).findById(existingCP.getId());
    assertNull(existingCP.getSvg());
    assertNull(existingCP.getSvgId());
  }
}
