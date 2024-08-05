package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SeasonDetailsDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SeasonUserDetailsDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Season;
import com.ladbrokescoral.oxygen.cms.api.exception.SeasonAlreadyExistException;
import com.ladbrokescoral.oxygen.cms.api.service.SeasonService;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
@SuppressWarnings("java:S4684")
public class SeasonController extends AbstractCrudController<Season> {

  private SeasonService seasonService;

  SeasonController(SeasonService seasonService) {
    super(seasonService);
    this.seasonService = seasonService;
  }

  @PostMapping("/season")
  @Override
  public ResponseEntity<Season> create(@RequestBody @Valid Season entity) {
    validateAlreadySeasonExist(entity);
    return super.create(entity);
  }

  @PutMapping("/season/{id}/{isSeasonDateChanged}")
  public Season update(
      @PathVariable String id,
      @PathVariable("isSeasonDateChanged") boolean isSeasonDateChanged,
      @RequestBody @Valid Season entity) {
    if (isSeasonDateChanged) {
      validateAlreadySeasonExistForUpdate(entity);
    }
    return super.update(id, entity);
  }

  @GetMapping("/season/{id}")
  public Optional<SeasonUserDetailsDto> readById(@PathVariable String id) {
    Season season = super.read(id);
    return seasonService.getSeasonById(Optional.ofNullable(season), id);
  }

  @GetMapping("/season/brand/{brand}")
  public List<SeasonDetailsDto> findSeasonsByBrand(@PathVariable String brand, Sort sort) {
    return seasonService.findSeasonsByBrand(brand, sort);
  }

  @DeleteMapping("/season/{id}")
  @Override
  public ResponseEntity<Season> delete(@PathVariable String id) {
    return super.delete(id);
  }

  private void validateAlreadySeasonExist(Season season) {
    List<Season> seasonList = seasonService.getSeasonBetweenDates(season);
    if (!seasonList.isEmpty()) {
      throw new SeasonAlreadyExistException(
          "Another Season is already saved with same date period");
    }
  }

  private void validateAlreadySeasonExistForUpdate(Season season) {
    List<Season> seasonList = seasonService.getSeasonBetweenDates(season);
    Optional<Season> originalSeason =
        seasonList.stream().filter(season1 -> season1.getId().equals(season.getId())).findFirst();
    originalSeason.ifPresent(seasonList::remove);
    if (!seasonList.isEmpty()) {
      throw new SeasonAlreadyExistException(
          "Another Season is already saved with same date period");
    }
  }
}
