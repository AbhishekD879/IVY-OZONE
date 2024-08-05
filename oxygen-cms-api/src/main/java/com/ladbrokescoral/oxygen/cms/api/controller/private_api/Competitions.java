package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static com.ladbrokescoral.oxygen.cms.api.entity.Patterns.COMMA_SEPARTED_NUMBERS;
import static com.ladbrokescoral.oxygen.cms.util.Util.toList;

import com.ladbrokescoral.oxygen.betradar.client.entity.BrCompetitionSeason;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventValidationResultDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeKnockoutEventDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeMarketDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Competition;
import com.ladbrokescoral.oxygen.cms.api.exception.InputValueIncorrectException;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionModuleService;
import com.ladbrokescoral.oxygen.cms.api.service.CompetitionService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import java.util.List;
import java.util.Optional;
import javax.validation.constraints.Pattern;
import org.apache.commons.lang3.StringUtils;
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

@RestController
@Validated
public class Competitions extends AbstractCrudController<Competition> {
  private CompetitionService competitionService;
  private SiteServeService siteServeService;
  private CompetitionModuleService competitionModuleService;

  @Autowired
  Competitions(
      CompetitionService crudService,
      SiteServeService siteServeService,
      CompetitionModuleService competitionModuleService) {
    super(crudService);
    this.competitionService = crudService;
    this.siteServeService = siteServeService;
    this.competitionModuleService = competitionModuleService;
  }

  @PostMapping("competition")
  @Override
  public ResponseEntity create(@RequestBody @Validated Competition entity) {
    return super.create(entity);
  }

  @GetMapping("competition")
  @Override
  public List<Competition> readAll() {
    return super.readAll();
  }

  @GetMapping("competition/brand/{brand}")
  @Override
  public List<Competition> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @GetMapping("competition/{id}")
  @Override
  public Competition read(@PathVariable String id) {
    return super.read(id);
  }

  @PutMapping("competition/{id}")
  @Override
  public Competition update(
      @PathVariable String id, @RequestBody @Validated Competition updateEntity) {
    Competition competition = competitionService.getCompetitionByid(id);
    updateEntity.setCompetitionTabs(competition.getCompetitionTabs());
    updateEntity.setCompetitionParticipants(competition.getCompetitionParticipants());
    return super.update(id, updateEntity);
  }

  @DeleteMapping("competition/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @GetMapping("competition/brand/{brand}/ss/market/{marketId}")
  public SiteServeMarketDto getMarketById(
      @PathVariable String brand, @PathVariable String marketId) {
    return siteServeService
        .getMarketById(brand, marketId)
        .orElseThrow(() -> new InputValueIncorrectException("marketId", marketId));
  }

  /**
   * @param brand - brand code
   * @param eventIds comma separated SiteServe event ids
   * @return list of events or error if one or more events are invalid
   */
  @GetMapping("competition/brand/{brand}/ss/event")
  public SiteServeEventValidationResultDto validateAndGetEventsById(
      @PathVariable String brand,
      @Pattern(regexp = COMMA_SEPARTED_NUMBERS) @RequestParam String eventIds,
      @RequestParam(required = false, defaultValue = "false") Boolean onlySpecials) {
    return siteServeService.validateAndGetEventsById(brand, toList(eventIds), onlySpecials);
  }

  @GetMapping("competition/brand/{brand}/ss/knockout/event")
  public SiteServeKnockoutEventDto getKnockoutEvent(
      @PathVariable String brand, @RequestParam String eventId) {
    return Optional.ofNullable(eventId)
        .filter(event -> !StringUtils.isEmpty(event))
        .flatMap(id -> siteServeService.getKnockoutEvent(brand, id))
        .orElseThrow(() -> new InputValueIncorrectException("eventId", eventId));
  }

  /**
   * @param brand - brand code
   * @param typeIds comma separated SiteServe type ids
   * @return list of events or error if one or more types are invalid
   */
  @GetMapping("competition/brand/{brand}/ss/type")
  public SiteServeEventValidationResultDto validateTypeAndGetEventsByType(
      @PathVariable String brand,
      @Pattern(regexp = COMMA_SEPARTED_NUMBERS) @RequestParam String typeIds,
      @RequestParam(required = false, defaultValue = "false") Boolean onlySpecials) {
    return siteServeService.validateEventsByTypeId(brand, toList(typeIds), onlySpecials);
  }

  @GetMapping("competition/{compId}/stats/groups")
  public ResponseEntity<BrCompetitionSeason> getGroups(@PathVariable String compId) {
    Competition competition = competitionService.getCompetitionByid(compId);
    return new ResponseEntity<>(
        competitionModuleService.getStatsCenterCompetitionSeason(competition), HttpStatus.OK);
  }
}
