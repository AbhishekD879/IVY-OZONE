package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.HomeModuleDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventDto;
import com.ladbrokescoral.oxygen.cms.api.entity.HomeModule;
import com.ladbrokescoral.oxygen.cms.api.entity.PageType;
import com.ladbrokescoral.oxygen.cms.api.entity.SelectionType;
import com.ladbrokescoral.oxygen.cms.api.mapping.HomeModuleMapper;
import com.ladbrokescoral.oxygen.cms.api.service.HomeModuleSiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.HomeModuleServiceImpl;
import java.time.OffsetDateTime;
import java.util.List;
import java.util.stream.Collectors;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.format.annotation.DateTimeFormat;
import org.springframework.format.annotation.DateTimeFormat.ISO;
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
public class HomeModules extends AbstractSortableController<HomeModule> {

  private HomeModuleServiceImpl homeModuleService;
  private HomeModuleSiteServeService homeModuleSiteServeService;

  @Autowired
  HomeModules(
      HomeModuleServiceImpl homeModuleService,
      HomeModuleSiteServeService homeModuleSiteServeService) {
    super(homeModuleService);
    this.homeModuleService = homeModuleService;
    this.homeModuleSiteServeService = homeModuleSiteServeService;
  }

  @PostMapping("home-module")
  @Override
  public ResponseEntity create(@Validated @RequestBody HomeModule entity) {
    return super.create(entity);
  }

  @GetMapping("home-module")
  public ResponseEntity findAll(
      @RequestParam(required = false, defaultValue = "true") Boolean active) {
    List<HomeModuleDto> list =
        homeModuleService.findByActiveState(active).stream()
            .map(HomeModuleMapper.INSTANCE::toDto)
            .collect(Collectors.toList());
    return new ResponseEntity<>(list, HttpStatus.OK);
  }

  @GetMapping("home-module/{id}")
  @Override
  public HomeModule read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("home-module/brand/{brand}")
  public List<HomeModuleDto> readByBrand(
      @PathVariable String brand,
      @RequestParam(required = false, defaultValue = "true") Boolean active) {
    return homeModuleService.findByActiveStateAndPublishToChannel(active, brand).stream()
        .map(HomeModuleMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }

  @GetMapping("home-module/brand/{brand}/{pageType}/{pageId}")
  public List<HomeModuleDto> readByBrandAndPageType(
      @PathVariable String brand,
      @PathVariable @Valid PageType pageType,
      @PathVariable String pageId) {
    return homeModuleService.findAll(brand, pageType, pageId).stream()
        .map(HomeModuleMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }

  @PutMapping("home-module/{id}")
  @Override
  public HomeModule update(
      @PathVariable("id") String id, @Validated @RequestBody HomeModule entity) {
    return super.update(id, entity);
  }

  @DeleteMapping("home-module/{id}")
  @Override
  public ResponseEntity delete(@PathVariable String id) {
    return super.delete(id);
  }

  // FIXME: use Instant on UI side insteaad of ISO.DATE_TIME
  @GetMapping("home-module/brand/{brand}/ss/event")
  public List<SiteServeEventDto> loadSSEvents(
      @PathVariable String brand,
      @RequestParam String selectionType,
      @RequestParam String selectionId,
      @RequestParam @DateTimeFormat(iso = ISO.DATE_TIME) OffsetDateTime dateFrom,
      @RequestParam @DateTimeFormat(iso = ISO.DATE_TIME) OffsetDateTime dateTo) {
    return homeModuleSiteServeService.loadEventsFromSiteServe(
        brand,
        SelectionType.fromString(selectionType),
        selectionId,
        dateFrom.toInstant(),
        dateTo.toInstant());
  }

  @GetMapping("home-module/brand/{brand}/segment/{segmentName}")
  public List<HomeModuleDto> readByBrandAndSegmentName(
      @PathVariable String brand,
      @RequestParam(required = false, defaultValue = "true") Boolean active,
      @PathVariable String segmentName) {
    return homeModuleService
        .findByActiveStateAndPublishToChannelBySegmantName(active, brand, segmentName).stream()
        .map(HomeModuleMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }

  @GetMapping("home-module/brand/{brand}/{pageType}/{pageId}/segment/{segmentName}")
  public List<HomeModuleDto> readByBrandAndPageTypeAndSegmentName(
      @PathVariable String brand,
      @PathVariable @Valid PageType pageType,
      @PathVariable String pageId,
      @PathVariable String segmentName) {
    return homeModuleService.findAll(brand, pageType, pageId, segmentName).stream()
        .map(HomeModuleMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }

  @Override
  @PostMapping("home-module/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
