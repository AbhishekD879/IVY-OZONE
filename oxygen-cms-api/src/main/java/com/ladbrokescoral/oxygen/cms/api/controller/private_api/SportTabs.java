package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.SportTabInputDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SportTab;
import com.ladbrokescoral.oxygen.cms.api.mapping.SportTabMapper;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabHelper;
import com.ladbrokescoral.oxygen.cms.api.service.sporttab.SportTabService;
import java.util.List;
import java.util.Optional;
import org.springframework.util.CollectionUtils;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class SportTabs extends AbstractSortableController<SportTab> {

  private final SportTabService sportTabService;

  SportTabs(SportTabService sportTabService) {
    super(sportTabService);
    this.sportTabService = sportTabService;
  }

  @GetMapping("sport-tab/{tabId}")
  @Override
  public SportTab read(@PathVariable String tabId) {
    SportTab tab = super.read(tabId);
    SportTabHelper.sortTrendingTabs(tab);
    return tab;
  }

  @GetMapping("sport-tab/brand/{brand}/sport/{sportId}")
  public List<SportTab> readByBrandAndSportId(
      @PathVariable String brand, @PathVariable Integer sportId) {
    List<SportTab> sporttabs = sportTabService.findAll(brand, sportId);
    sporttabs.forEach(SportTabHelper::sortTrendingTabs);
    return sporttabs;
  }

  @PutMapping("sport-tab/{tabId}")
  public SportTab update(
      @PathVariable String tabId, @Validated @RequestBody SportTabInputDto inputDto) {
    SportTab entity = SportTabMapper.INSTANCE.toEntity(inputDto);
    Optional<SportTab> existingEntity = sportTabService.findOne(tabId);
    if (CollectionUtils.isEmpty(entity.getTrendingTabs())) {
      existingEntity.ifPresent(sportTab -> entity.setTrendingTabs(sportTab.getTrendingTabs()));
    } else {
      sportTabService.saveTrendingTabForPopularBets(entity);
    }
    entity.setId(tabId);
    return super.update(existingEntity, entity);
  }

  @PostMapping("sport-tab/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
