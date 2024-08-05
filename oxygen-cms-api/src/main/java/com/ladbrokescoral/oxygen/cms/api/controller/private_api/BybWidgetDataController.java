package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BybWidgetDataDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SiteServeMarketDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BybWidgetData;
import com.ladbrokescoral.oxygen.cms.api.exception.InputValueIncorrectException;
import com.ladbrokescoral.oxygen.cms.api.service.BybWidgetDataService;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.util.ArrayList;
import java.util.List;
import java.util.Optional;
import javax.validation.Valid;
import org.modelmapper.ModelMapper;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@Validated
public class BybWidgetDataController extends AbstractSortableController<BybWidgetData> {
  private final BybWidgetDataService bybWidgetDataService;

  private final ModelMapper mapper;

  private final SiteServeService siteServeService;

  public BybWidgetDataController(
      BybWidgetDataService bybWidgetDataService,
      ModelMapper mapper,
      SiteServeService siteServeService) {
    super(bybWidgetDataService);
    this.bybWidgetDataService = bybWidgetDataService;
    this.mapper = mapper;
    this.siteServeService = siteServeService;
  }

  @PostMapping("/byb-widget-data")
  public ResponseEntity<BybWidgetData> create(
      @Valid @RequestBody BybWidgetDataDto bybWidgetDataDto) {

    return validateEventAndMarketId(bybWidgetDataDto)
        .map(
            (SiteServeMarketDto market) -> {
              BybWidgetData bybWidgetData = mapper.map(bybWidgetDataDto, BybWidgetData.class);
              return super.create(bybWidgetData);
            })
        .orElseThrow(
            () ->
                new InputValueIncorrectException(
                    "EventId/marketId ",
                    bybWidgetDataDto.getEventId() + "/" + bybWidgetDataDto.getMarketId()));
  }

  @PutMapping("/byb-widget-data/{id}")
  public BybWidgetData update(
      @PathVariable String id, @Valid @RequestBody BybWidgetDataDto bybWidgetDataDto) {

    return validateEventAndMarketId(bybWidgetDataDto)
        .map(
            (SiteServeMarketDto market) -> {
              BybWidgetData bybWidgetData = mapper.map(bybWidgetDataDto, BybWidgetData.class);
              return super.update(id, bybWidgetData);
            })
        .orElseThrow(
            () ->
                new InputValueIncorrectException(
                    "EventId/marketId ",
                    bybWidgetDataDto.getEventId() + "/" + bybWidgetDataDto.getMarketId()));
  }

  private Optional<SiteServeMarketDto> validateEventAndMarketId(BybWidgetDataDto bybWidgetDataDto) {
    return siteServeService
        .getMarketById(bybWidgetDataDto.getBrand(), bybWidgetDataDto.getMarketId())
        .filter(market -> bybWidgetDataDto.getEventId().equals(market.getEventId()));
  }

  @GetMapping("/byb-widget-data/brand/{brand}")
  public List<BybWidgetDataDto> findAllByBrand(@PathVariable @Brand String brand) {
    return bybWidgetDataService.readByBrand(brand).orElseGet(ArrayList::new);
  }

  @GetMapping("/byb-widget-data/brand/{brand}/status")
  public List<BybWidgetDataDto> findAllByStatusAndBrand(
      @PathVariable @Brand String brand,
      @RequestParam(required = false, defaultValue = "true") Boolean active) {

    return bybWidgetDataService.getRecordsByBrandAndStatus(brand, active).orElseGet(ArrayList::new);
  }

  @DeleteMapping("/byb-widget-data/{id}")
  public void deleteById(@PathVariable String id) {
    super.delete(id);
  }

  @Override
  @PostMapping("/byb-widget-data/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
