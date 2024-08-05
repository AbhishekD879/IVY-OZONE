package com.ladbrokescoral.oxygen.cms.api.service;

import com.google.common.base.Strings;
import com.ladbrokescoral.oxygen.cms.api.entity.Competition;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionParticipant;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.CompetitionParticipantRepository;
import com.ladbrokescoral.oxygen.cms.api.service.validators.ValidFileType;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import org.springframework.stereotype.Component;
import org.springframework.util.Assert;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.multipart.MultipartFile;

@Component
@Validated
public class CompetitionParticipantService extends AbstractService<CompetitionParticipant> {

  private final SvgImageParser imageService;
  private final CompetitionService competitionService;

  public CompetitionParticipantService(
      CompetitionParticipantRepository repository,
      CompetitionService competitionService,
      SvgImageParser imageService) {
    super(repository);
    this.imageService = imageService;
    this.competitionService = competitionService;
  }

  public CompetitionParticipant createCompetitionParticipant(
      CompetitionParticipant participant, String compId) {
    Assert.isTrue(null != participant, "Participant is not created");
    Competition competition = competitionService.getCompetitionByid(compId);
    List<CompetitionParticipant> participants =
        Optional.ofNullable(competition.getCompetitionParticipants()).orElse(new ArrayList<>());
    validateParticipants(participant, participants);
    participants.add(participant);
    competition.setCompetitionParticipants(participants);
    competitionService.save(competition);
    return participant;
  }

  private void validateParticipants(
      CompetitionParticipant participant, List<CompetitionParticipant> participants) {
    Assert.isTrue(
        !Strings.isNullOrEmpty(participant.getObName()), "obName is required, but is empty");
    Optional<CompetitionParticipant> expectedNoParticipant =
        participants.stream().filter(p -> participant.getObName().equals(p.getObName())).findAny();
    Assert.isTrue(!expectedNoParticipant.isPresent(), "Expected no duplicated participants");
  }

  public Competition readCompetitionByCompetitionParticipant(String compId, String participantId) {
    Competition competition =
        Optional.ofNullable(competitionService.getCompetitionByid(compId))
            .orElseThrow(NotFoundException::new);
    CompetitionParticipant participant =
        competitionService.getCompetitionParticipant(participantId, competition);
    competition.setCompetitionParticipants(Arrays.asList(participant));
    return competition;
  }

  public void deleteCompetitionParticipantFromCompetition(String compId, String participantId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    List<CompetitionParticipant> newParticipants =
        competition.getCompetitionParticipants().stream()
            .filter(participant -> !participant.getId().equals(participantId))
            .collect(Collectors.toList());
    competition.setCompetitionParticipants(newParticipants);
    competitionService.save(competition);
  }

  public Optional<CompetitionParticipant> attachImage(
      String id, @ValidFileType("svg") MultipartFile file) {
    Optional<CompetitionParticipant> one = super.findOne(id);

    Optional<Svg> svg = imageService.parse(file);

    return one.filter(cp -> svg.isPresent())
        .map(
            entity ->
                CompetitionParticipant.setSvgFields(
                    entity, svg.get().getSvg(), svg.get().getId(), svg.get().getValue()))
        .map(this::save);
  }

  public Optional<CompetitionParticipant> removeImage(String id) {
    Optional<CompetitionParticipant> one = super.findOne(id);

    return one.map(entity -> CompetitionParticipant.setSvgFields(entity, null, null, null))
        .map(this::save);
  }
}
