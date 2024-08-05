package com.ladbrokescoral.oxygen.bigcompetition.controller;

import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionSubTabDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.CompetitionTabDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.ParticipantWithSvgDto;
import com.ladbrokescoral.oxygen.bigcompetition.dto.module.CompetitionModuleDto;
import com.ladbrokescoral.oxygen.bigcompetition.exception.NotFoundException;
import com.ladbrokescoral.oxygen.bigcompetition.service.CompetitionService;
import java.util.Map;
import java.util.concurrent.TimeUnit;
import org.springframework.http.CacheControl;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class CompetitionApi {
  private final CompetitionService competitionService;

  private static final int CACHE_CONTROL_TIMEOUT = 30;

  public CompetitionApi(CompetitionService competitionService) {
    this.competitionService = competitionService;
  }

  @GetMapping(value = "competition/{uri}")
  public ResponseEntity<CompetitionDto> findCompetition(@PathVariable String uri) {
    return ResponseEntity.ok()
        .cacheControl(CacheControl.maxAge(CACHE_CONTROL_TIMEOUT, TimeUnit.SECONDS))
        .body(
            competitionService
                .findCompetitionDtoWithoutModules(uri)
                .orElseThrow(NotFoundException::new));
  }

  @GetMapping(value = "competition/tab/{id}")
  public ResponseEntity<CompetitionTabDto> findCompetitionTab(@PathVariable String id) {
    return ResponseEntity.ok()
        .cacheControl(CacheControl.maxAge(CACHE_CONTROL_TIMEOUT, TimeUnit.SECONDS))
        .body(competitionService.findCompetitionTabDto(id).orElseThrow(NotFoundException::new));
  }

  @GetMapping(value = "competition/subtab/{id}")
  public ResponseEntity<CompetitionSubTabDto> findCompetitionSubTab(@PathVariable String id) {
    return ResponseEntity.ok()
        .cacheControl(CacheControl.maxAge(CACHE_CONTROL_TIMEOUT, TimeUnit.SECONDS))
        .body(competitionService.findCompetitionSubTabDto(id).orElseThrow(NotFoundException::new));
  }

  @GetMapping(value = "competition/module/{id}")
  public ResponseEntity<CompetitionModuleDto> findModule(@PathVariable String id) {
    return ResponseEntity.ok()
        .cacheControl(CacheControl.maxAge(CACHE_CONTROL_TIMEOUT, TimeUnit.SECONDS))
        .body(competitionService.findCompetitionModuleDto(id).orElseThrow(NotFoundException::new));
  }

  @GetMapping(value = "competition/{uri}/participant")
  public ResponseEntity<Map<String, ParticipantWithSvgDto>> findParticipantsForCompetition(
      @PathVariable String uri) {
    return ResponseEntity.ok()
        .cacheControl(CacheControl.maxAge(CACHE_CONTROL_TIMEOUT, TimeUnit.SECONDS))
        .body(
            competitionService
                .findCompetitionParticipants(uri)
                .orElseThrow(NotFoundException::new));
  }
}
