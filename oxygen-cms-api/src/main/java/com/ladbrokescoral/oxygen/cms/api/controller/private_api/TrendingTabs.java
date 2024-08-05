package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.entity.TrendingTab;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabHelper;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.TrendingTabService;
import java.util.Optional;
import javax.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class TrendingTabs extends AbstractSortableController<TrendingTab> {

  private final SportTabService sportTabService;

  TrendingTabs(TrendingTabService trendingTabService, SportTabService sportTabService) {
    super(trendingTabService);
    this.sportTabService = sportTabService;
  }

  @GetMapping("trending-tab/{tabId}")
  @Override
  public TrendingTab read(@PathVariable String tabId) {
    TrendingTab trendingTab = super.read(tabId);
    SportTabHelper.sortPopularTabs(trendingTab);
    return trendingTab;
  }

  @PostMapping("trending-tab/{sportTabId}")
  public ResponseEntity<TrendingTab> create(
      @PathVariable String sportTabId, @RequestBody @Validated TrendingTab entity) {
    return sportTabService
        .findOne(sportTabId)
        .map(
            (SportTab sportTab) -> {
              TrendingTab createdEntity = super.createEntity(entity);
              sportTab.getTrendingTabs().add(createdEntity);
              sportTabService.save(sportTab);
              return new ResponseEntity<>(createdEntity, HttpStatus.CREATED);
            })
        .orElse(new ResponseEntity<>(HttpStatus.BAD_REQUEST));
  }

  @Override
  @PutMapping("trending-tab/{id}")
  public TrendingTab update(
      @PathVariable("id") String id, @Valid @Validated @RequestBody TrendingTab updateEntity) {
    Optional<TrendingTab> existingEntity = sortableService.findOne(id);
    existingEntity.ifPresent(existing -> updateEntity.setPopularTabs(existing.getPopularTabs()));
    updateEntity.setId(id);
    return super.update(existingEntity, updateEntity);
  }

  @Override
  @DeleteMapping("trending-tab/{id}")
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  @Override
  @PostMapping("trending-tab/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
