package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.Competition;
import com.ladbrokescoral.oxygen.cms.api.entity.CompetitionParticipant;
import com.ladbrokescoral.oxygen.cms.api.entity.FileType;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionParticipantService;
import java.util.List;
import javax.validation.constraints.NotEmpty;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.multipart.MultipartFile;

@RestController
public class CompetionsParticipants extends AbstractCrudController<CompetitionParticipant> {

  private final CompetitionParticipantService service;

  @Autowired
  CompetionsParticipants(CompetitionParticipantService crudService) {
    super(crudService);
    service = crudService;
  }

  @PostMapping("competition/{compId}/participant")
  public ResponseEntity createWithParentCompetition(
      @RequestBody @Validated CompetitionParticipant entity,
      @PathVariable @NotEmpty String compId) {
    CompetitionParticipant participant = super.createEntity(entity);
    participant = service.createCompetitionParticipant(participant, compId);
    return new ResponseEntity<>(participant, HttpStatus.CREATED);
  }

  @GetMapping("competition/{compId}/participant/{participantId}")
  public ResponseEntity readWithParentCompetition(
      @PathVariable @NotEmpty String compId, @PathVariable @NotEmpty String participantId) {
    Competition competition =
        service.readCompetitionByCompetitionParticipant(compId, participantId);
    populateCreatorAndUpdater(competition);
    populateCreatorAndUpdater(competition.getCompetitionParticipants().get(0));
    return new ResponseEntity<>(competition, HttpStatus.OK);
  }

  @DeleteMapping("competition/{compId}/participant/{participantId}")
  public ResponseEntity deleteWithParentCompetition(
      @PathVariable String compId, @PathVariable String participantId) {
    service.deleteCompetitionParticipantFromCompetition(compId, participantId);
    return super.delete(participantId);
  }

  @GetMapping("participant")
  @Override
  public List<CompetitionParticipant> readAll() {
    return super.readAll();
  }

  @GetMapping("participant/{participantId}")
  @Override
  public CompetitionParticipant read(@PathVariable String participantId) {
    return super.read(participantId);
  }

  @PutMapping("participant/{participantId}")
  @Override
  public CompetitionParticipant update(
      @PathVariable String participantId, @RequestBody CompetitionParticipant entity) {
    return super.update(participantId, entity);
  }

  @PostMapping("participant/{participantId}/image")
  public ResponseEntity uploadImage(
      @PathVariable("participantId") String participantId,
      @RequestParam(value = "fileType", defaultValue = "svg", required = false) FileType fileType,
      @RequestParam("file") MultipartFile file) {

    return FileType.SVG.equals(fileType)
        ? service.attachImage(participantId, file).map(ResponseEntity::ok).orElseGet(notFound())
        : new ResponseEntity(HttpStatus.BAD_REQUEST);
  }

  @DeleteMapping("participant/{participantId}/image")
  public ResponseEntity removeImage(
      @PathVariable("participantId") String participantId,
      @RequestParam(value = "fileType", defaultValue = "svg", required = false) FileType fileType) {
    return FileType.SVG.equals(fileType)
        ? service.removeImage(participantId).map(ResponseEntity::ok).orElseGet(notFound())
        : new ResponseEntity(HttpStatus.BAD_REQUEST);
  }
}
