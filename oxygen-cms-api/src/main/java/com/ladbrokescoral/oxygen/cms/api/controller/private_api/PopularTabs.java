package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularTab;
import com.ladbrokescoral.oxygen.cms.api.entity.TrendingTab;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.PopularTabService;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.TrendingTabService;
import javax.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class PopularTabs extends AbstractSortableController<PopularTab> {

  private final TrendingTabService trendingTabService;

  PopularTabs(PopularTabService popularTabService, TrendingTabService trendingTabService) {
    super(popularTabService);
    this.trendingTabService = trendingTabService;
  }

  @GetMapping("popular-tab/{tabId}")
  @Override
  public PopularTab read(@PathVariable String tabId) {
    return super.read(tabId);
  }

  @PostMapping("popular-tab/{trendingTabId}")
  public ResponseEntity<PopularTab> create(
      @PathVariable("trendingTabId") String trendingTabId,
      @RequestBody @Validated PopularTab entity) {
    return trendingTabService
        .findOne(trendingTabId)
        .map(
            (TrendingTab trendingTab) -> {
              PopularTab createdEntity = super.createEntity(entity);
              trendingTab.getPopularTabs().add(createdEntity);
              trendingTabService.save(trendingTab);
              return new ResponseEntity<>(createdEntity, HttpStatus.CREATED);
            })
        .orElse(new ResponseEntity<>(HttpStatus.BAD_REQUEST));
  }

  @Override
  @PutMapping("popular-tab/{id}")
  public PopularTab update(
      @PathVariable("id") String id, @Valid @Validated @RequestBody PopularTab updateEntity) {
    return super.update(id, updateEntity);
  }

  @Override
  @DeleteMapping("popular-tab/{id}")
  public ResponseEntity delete(@PathVariable("id") String id) {
    return super.delete(id);
  }

  @Override
  @PostMapping("popular-tab/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
