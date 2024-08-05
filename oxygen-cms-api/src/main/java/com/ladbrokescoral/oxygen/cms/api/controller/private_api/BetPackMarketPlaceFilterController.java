package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.BPMDto;
import com.ladbrokescoral.oxygen.cms.api.dto.BetPackFilterDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.BetPackFilter;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackEnablerFilterService;
import com.ladbrokescoral.oxygen.cms.api.service.BetPackMarketPlaceService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class BetPackMarketPlaceFilterController extends AbstractSortableController<BetPackFilter> {

  private final BetPackMarketPlaceService betPackMarketPlaceService;
  private final BetPackEnablerFilterService betPackEnablerFilterService;

  public BetPackMarketPlaceFilterController(
      BetPackMarketPlaceService betPackMarketPlaceService,
      BetPackEnablerFilterService betPackEnablerFilterService) {
    super(betPackEnablerFilterService);
    this.betPackEnablerFilterService = betPackEnablerFilterService;
    this.betPackMarketPlaceService = betPackMarketPlaceService;
  }

  @GetMapping("bet-pack/filters")
  public List<BetPackFilter> getAllBetPackFilters() {
    return super.readAll();
  }

  @GetMapping("bet-pack/filters/brand/{brand}")
  public List<BetPackFilter> getBetPackFiltersByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("bet-pack/filter")
  public ResponseEntity<BetPackFilter> createBetPackFilter(
      @RequestBody @Valid BetPackFilterDto betPackFilterDto) {
    BetPackFilter entity =
        betPackEnablerFilterService.checkActiveFilterLimit(
            betPackFilterDto.getId(), betPackFilterDto);
    return super.create(entity);
  }

  @Override
  @PostMapping("bet-pack/filter/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }

  @GetMapping("bet-pack/filter/{id}")
  public ResponseEntity<BetPackFilter> getBetPackFilter(@PathVariable String id) {
    return new ResponseEntity<>(super.read(id), HttpStatus.OK);
  }

  @PutMapping("bet-pack/filter/{id}")
  public ResponseEntity<BPMDto> update(
      @PathVariable("id") String id, @Valid @RequestBody BetPackFilterDto betPackFilterDto) {
    betPackEnablerFilterService.validateSortOrder(betPackFilterDto);
    BetPackFilter entity = betPackEnablerFilterService.checkActiveFilterLimit(id, betPackFilterDto);
    BPMDto bpmDto = new BPMDto();
    BetPackFilter filterEntity = super.read(id);
    List<BetPackEntity> allBetPackEntities = betPackMarketPlaceService.findAllBetPackEntities();
    bpmDto =
        betPackEnablerFilterService.getFilterStatus(
            filterEntity.getFilterName(), bpmDto, allBetPackEntities);
    if (!bpmDto.isFilterAssociated()) {
      super.update(id, entity);
    }
    return new ResponseEntity<>(bpmDto, HttpStatus.OK);
  }

  @DeleteMapping("bet-pack/filter/{filterName}")
  public ResponseEntity<BPMDto> deleteByFilterName(@PathVariable String filterName) {
    BPMDto bpmDto = new BPMDto();
    List<BetPackEntity> allBetPackEntities = betPackMarketPlaceService.findAllBetPackEntities();
    bpmDto = betPackEnablerFilterService.getFilterStatus(filterName, bpmDto, allBetPackEntities);
    if (!bpmDto.isFilterAssociated()) {
      Long status = betPackEnablerFilterService.deleteByFilterName(filterName);
      if (1l == status) {
        return new ResponseEntity<>(bpmDto, HttpStatus.ACCEPTED);
      } else {
        return new ResponseEntity<>(bpmDto, HttpStatus.NO_CONTENT);
      }
    } else {
      return new ResponseEntity<>(bpmDto, HttpStatus.OK);
    }
  }
}
