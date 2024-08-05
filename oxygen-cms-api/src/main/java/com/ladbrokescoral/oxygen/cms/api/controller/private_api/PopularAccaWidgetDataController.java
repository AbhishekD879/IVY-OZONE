package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.dto.PopularAccaWidgetDataDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeEventValidationResultDto;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularAccaType;
import com.ladbrokescoral.oxygen.cms.api.entity.PopularAccaWidgetData;
import com.ladbrokescoral.oxygen.cms.api.exception.InputValueIncorrectException;
import com.ladbrokescoral.oxygen.cms.api.service.PopularAccaWidgetDataService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.util.ArrayList;
import java.util.List;
import javax.validation.Valid;
import org.modelmapper.ModelMapper;
import org.springframework.http.ResponseEntity;
import org.springframework.util.CollectionUtils;
import org.springframework.util.StringUtils;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@Validated
public class PopularAccaWidgetDataController
    extends AbstractSortableController<PopularAccaWidgetData> {
  private final PopularAccaWidgetDataService popularAccaWidgetDataService;

  private final ModelMapper mapper;

  private final SiteServeService siteServeService;

  public PopularAccaWidgetDataController(
      PopularAccaWidgetDataService popularAccaWidgetDataService,
      ModelMapper mapper,
      SiteServeService siteServeService) {
    super(popularAccaWidgetDataService);
    this.popularAccaWidgetDataService = popularAccaWidgetDataService;
    this.mapper = mapper;
    this.siteServeService = siteServeService;
  }

  @Override
  @GetMapping("/popular-acca-widget-data/{id}")
  public PopularAccaWidgetData read(@PathVariable("id") String id) {
    return super.read(id);
  }

  @PostMapping("/popular-acca-widget-data")
  public ResponseEntity<PopularAccaWidgetData> create(
      @Valid @RequestBody PopularAccaWidgetDataDto popularAccaWidgetDataDto) {
    validate(popularAccaWidgetDataDto);
    PopularAccaWidgetData popularAccaWidgetData =
        mapper.map(popularAccaWidgetDataDto, PopularAccaWidgetData.class);
    return super.create(popularAccaWidgetData);
  }

  @PutMapping("/popular-acca-widget-data/{id}")
  public PopularAccaWidgetData update(
      @PathVariable String id,
      @Valid @RequestBody PopularAccaWidgetDataDto popularAccaWidgetDataDto) {
    validate(popularAccaWidgetDataDto);
    PopularAccaWidgetData popularAccaWidgetData =
        mapper.map(popularAccaWidgetDataDto, PopularAccaWidgetData.class);
    return super.update(id, popularAccaWidgetData);
  }

  @GetMapping("/popular-acca-widget-data/brand/{brand}")
  public List<PopularAccaWidgetDataDto> findAllByBrand(@PathVariable @Brand String brand) {
    return popularAccaWidgetDataService.readByBrand(brand).orElseGet(ArrayList::new);
  }

  @GetMapping("/popular-acca-widget-data/brand/{brand}/status")
  public List<PopularAccaWidgetDataDto> findAllByStatusAndBrand(
      @PathVariable @Brand String brand,
      @RequestParam(required = false, defaultValue = "true") Boolean active) {

    return popularAccaWidgetDataService
        .getRecordsByBrandAndStatus(brand, active)
        .orElseGet(ArrayList::new);
  }

  @DeleteMapping("/popular-acca-widget-data/{id}")
  public ResponseEntity<PopularAccaWidgetData> deleteById(@PathVariable String id) {
    return super.delete(id);
  }

  @Override
  @PostMapping("/popular-acca-widget-data/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  private void validate(PopularAccaWidgetDataDto data) {
    PopularAccaType popularAccaType = PopularAccaType.getPopularAccaType(data.getAccaIdsType());
    if (popularAccaType == PopularAccaType.ALL) {
      return;
    }
    if (CollectionUtils.isEmpty(data.getListOfIds())) {
      throw new InputValueIncorrectException("listOfIds", "");
    } else {
      SiteServeEventValidationResultDto resultDto;
      if (popularAccaType == PopularAccaType.TYPEID) {
        resultDto =
            siteServeService.validateEventsByTypeId(data.getBrand(), data.getListOfIds(), false);
      } else if (popularAccaType == PopularAccaType.EVENT) {
        resultDto =
            siteServeService.validateAndGetEventsById(data.getBrand(), data.getListOfIds(), false);
      } else {
        resultDto =
            siteServeService.validateEventsByOutcomeId(data.getBrand(), data.getListOfIds());
      }
      if (!CollectionUtils.isEmpty(resultDto.getInvalid())) {
        throw new InputValueIncorrectException(
            "listOfIds", StringUtils.collectionToCommaDelimitedString(resultDto.getInvalid()));
      }
    }
  }
}
