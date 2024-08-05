package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybWidget;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.service.BybWidgetDataService;
import com.ladbrokescoral.oxygen.cms.api.service.BybWidgetService;
import com.ladbrokescoral.oxygen.cms.api.service.ModuleRibbonTabService;
import com.ladbrokescoral.oxygen.cms.api.service.SportModuleService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.Valid;
import org.modelmapper.ModelMapper;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class BybWidgetController extends AbstractCrudController<BybWidget> {
  private final BybWidgetService bybWidgetService;
  private final BybWidgetDataService bybWidgetDataService;
  private final SportModuleService sportModuleService;
  private final ModuleRibbonTabService moduleRibbonTabService;

  private final ModelMapper mapper;

  public BybWidgetController(
      BybWidgetService bybWidgetService,
      BybWidgetDataService bybWidgetDataService,
      ModelMapper mapper,
      SportModuleService sportModuleService,
      ModuleRibbonTabService moduleRibbonTabService) {
    super(bybWidgetService);
    this.bybWidgetService = bybWidgetService;
    this.sportModuleService = sportModuleService;
    this.mapper = mapper;
    this.bybWidgetDataService = bybWidgetDataService;
    this.moduleRibbonTabService = moduleRibbonTabService;
  }

  @PostMapping("/byb-widget")
  public ResponseEntity<BybWidget> create(@Valid @RequestBody BybWidgetDto bybWidgetDto) {
    BybWidget bybWidget = mapper.map(bybWidgetDto, BybWidget.class);
    return super.create(bybWidget);
  }

  @PutMapping("/byb-widget/{id}")
  public BybWidget update(@PathVariable String id, @Valid @RequestBody BybWidgetDto bybWidgetDto) {

    BybWidget bybWidget = mapper.map(bybWidgetDto, BybWidget.class);
    return super.update(id, bybWidget);
  }

  @GetMapping("/byb-widget/brand/{brand}")
  public BybWidgetDto findAllByBrand(@PathVariable @Brand String brand) {

    return bybWidgetService
        .readByBrand(brand)
        .map((BybWidget entity) -> mapToBybWidgetDto(entity, brand))
        .orElseGet(BybWidgetDto::new);
  }

  private BybWidgetDto mapToBybWidgetDto(BybWidget bybWidget, String brand) {
    BybWidgetDto dto = mapper.map(bybWidget, BybWidgetDto.class);
    bybWidgetDataService.getRecordsByBrandAndStatus(brand, true).ifPresent(dto::setData);
    sportModuleService
        .findAll(brand, SportModuleType.BYB_WIDGET)
        .forEach(
            sportModule ->
                dto.getDisplayOn().put(sportModule.getPageId(), !sportModule.isDisabled()));
    dto.getDisplayOn()
        .put("BybHomePage", moduleRibbonTabService.existsByBrandAndBybVisbleTrue(brand));
    return dto;
  }
}
