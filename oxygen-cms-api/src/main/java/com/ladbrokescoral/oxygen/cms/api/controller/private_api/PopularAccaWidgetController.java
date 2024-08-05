package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static com.ladbrokescoral.oxygen.cms.api.service.sporttab.MainTier1Sports.FOOTBALL;

import com.ladbrokescoral.oxygen.cms.api.dto.PopularAccaWidgetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularAccaWidget;
import com.ladbrokescoral.oxygen.cms.api.entity.SportModuleType;
import com.ladbrokescoral.oxygen.cms.api.service.PopularAccaWidgetDataService;
import com.ladbrokescoral.oxygen.cms.api.service.PopularAccaWidgetService;
import com.ladbrokescoral.oxygen.cms.api.service.SportCategoryService;
import com.ladbrokescoral.oxygen.cms.api.service.SportModuleService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.Valid;
import org.modelmapper.ModelMapper;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class PopularAccaWidgetController extends AbstractCrudController<PopularAccaWidget> {
  private final PopularAccaWidgetService popularAccaWidgetService;
  private final PopularAccaWidgetDataService popularAccaWidgetDataService;
  private final SportModuleService sportModuleService;
  private final SportCategoryService sportCategoryService;
  private final ModelMapper mapper;

  public PopularAccaWidgetController(
      PopularAccaWidgetService popularAccaWidgetService,
      PopularAccaWidgetDataService popularAccaWidgetDataService,
      ModelMapper mapper,
      SportModuleService sportModuleService,
      SportCategoryService sportCategoryService) {
    super(popularAccaWidgetService);
    this.popularAccaWidgetService = popularAccaWidgetService;
    this.sportModuleService = sportModuleService;
    this.mapper = mapper;
    this.popularAccaWidgetDataService = popularAccaWidgetDataService;
    this.sportCategoryService = sportCategoryService;
  }

  @PostMapping("/popular-acca-widget")
  public ResponseEntity<PopularAccaWidget> create(
      @Valid @RequestBody PopularAccaWidgetDto popularAccaWidgetDto) {
    PopularAccaWidget popularAccaWidget = mapper.map(popularAccaWidgetDto, PopularAccaWidget.class);
    return super.create(popularAccaWidget);
  }

  @PutMapping("/popular-acca-widget/{id}")
  public PopularAccaWidget update(
      @PathVariable String id, @Valid @RequestBody PopularAccaWidgetDto popularAccaWidgetDto) {

    PopularAccaWidget popularAccaWidget = mapper.map(popularAccaWidgetDto, PopularAccaWidget.class);
    return super.update(id, popularAccaWidget);
  }

  @GetMapping("/popular-acca-widget/brand/{brand}")
  public PopularAccaWidgetDto findAllByBrand(@PathVariable @Brand String brand) {

    return popularAccaWidgetService
        .readByBrand(brand)
        .map((PopularAccaWidget entity) -> mapToPopularAccaWidgetDto(entity, brand))
        .orElseGet(() -> initNewDto(brand));
  }

  private PopularAccaWidgetDto mapToPopularAccaWidgetDto(
      PopularAccaWidget popularAccaWidget, String brand) {
    PopularAccaWidgetDto dto = mapper.map(popularAccaWidget, PopularAccaWidgetDto.class);
    popularAccaWidgetDataService.getRecordsByBrandAndStatus(brand, true).ifPresent(dto::setData);
    sportModuleService
        .findAll(brand, SportModuleType.POPULAR_ACCA)
        .forEach(
            sportModule ->
                dto.getDisplayOn().put(sportModule.getPageId(), !sportModule.isDisabled()));
    initCategoryIds(brand, dto);
    return dto;
  }

  private PopularAccaWidgetDto initNewDto(String brand) {
    PopularAccaWidgetDto dto = new PopularAccaWidgetDto();
    initCategoryIds(brand, dto);
    return dto;
  }

  private void initCategoryIds(String brand, PopularAccaWidgetDto dto) {
    sportCategoryService
        .findOneByCategoryId(brand, FOOTBALL.getCategoryId())
        .ifPresent(
            category -> dto.getCategoryIds().put(FOOTBALL.getCategoryId(), category.getId()));
  }
}
