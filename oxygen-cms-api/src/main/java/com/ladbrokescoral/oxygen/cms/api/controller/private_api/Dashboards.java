package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.AbstractEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.Dashboard;
import com.ladbrokescoral.oxygen.cms.api.service.DashboardService;
import java.time.LocalDate;
import java.util.Comparator;
import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;
import javax.validation.constraints.Min;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.format.annotation.DateTimeFormat.ISO;
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

@Validated
@RestController
public class Dashboards extends PageableAbstractCrudController<Dashboard> {
  private DashboardService service;

  @Autowired
  Dashboards(DashboardService crudService) {
    super(crudService);
    service = crudService;
  }

  @PostMapping(value = "dashboard")
  public ResponseEntity create(@Validated @RequestBody Dashboard entity) {
    return super.create(entity);
  }

  @GetMapping("dashboard")
  public List<Dashboard> readAll(
      @Min(value = 0L, message = "must be greater than or equal to 0")
          @RequestParam(name = "offset", required = false)
          Long offset,
      @Min(value = 1L, message = "must be greater than or equal to 1")
          @RequestParam(value = "limit", required = false)
          Long limit) {
    Optional<Integer> offsetInteger = Optional.ofNullable(offset).map(Long::intValue);
    Optional<Integer> limitInteger = Optional.ofNullable(limit).map(Long::intValue);
    return super.readAll(offsetInteger, limitInteger);
  }

  @GetMapping("dashboard/{id}")
  @Override
  public Dashboard read(@PathVariable String id) {
    return super.read(id);
  }

  @PutMapping("dashboard/{id}")
  @Override
  public Dashboard update(@PathVariable String id, @Validated @RequestBody Dashboard entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("dashboard/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @GetMapping("dashboard/brand/{brand}")
  public List<Dashboard> readByBrandAndDate(
      @PathVariable String brand,
      @RequestParam(required = false) @DateTimeFormat(iso = ISO.DATE) @Validated LocalDate date) {

    List<Dashboard> dashboards = date == null ? service.findAll() : service.readByDate(date);
    Comparator<Dashboard> comparator = Comparator.comparing(AbstractEntity::getCreatedAt);

    return populateCreatorAndUpdater(
        dashboards.stream().sorted(comparator.reversed()).limit(100).collect(Collectors.toList()));
  }
}
