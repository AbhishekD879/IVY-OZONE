package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.TrendingBetDto;
import com.ladbrokescoral.oxygen.cms.api.entity.TrendingBet;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.TrendingBetService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import javax.validation.Valid;
import org.modelmapper.ModelMapper;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class TrendingBets extends AbstractCrudController<TrendingBet> {
  private final ModelMapper modelMapper;
  private final TrendingBetService trendingBetService;

  public TrendingBets(ModelMapper modelMapper, TrendingBetService trendingBetService) {
    super(trendingBetService);
    this.modelMapper = modelMapper;
    this.trendingBetService = trendingBetService;
  }

  @PostMapping("/trending-bet")
  public ResponseEntity<TrendingBet> createTrendingBet(
      @Valid @Validated @RequestBody TrendingBetDto trendingBetDto) {
    TrendingBet trendingBet = modelMapper.map(trendingBetDto, TrendingBet.class);
    return super.create(trendingBet);
  }

  @PutMapping("/trending-bet/{id}")
  public TrendingBet updateTrendingBet(
      @PathVariable("id") String id, @Valid @Validated @RequestBody TrendingBetDto trendingBetDto) {
    TrendingBet trendingBet = modelMapper.map(trendingBetDto, TrendingBet.class);
    return super.update(id, trendingBet);
  }

  @DeleteMapping("/trending-bet/{id}")
  public ResponseEntity<TrendingBet> deleteById(@PathVariable("id") String id) {
    return super.delete(id);
  }

  @GetMapping("/trending-bet/brand/{brand}")
  public TrendingBet getByBrand(
      @Valid @Validated @Brand @PathVariable("brand") String brand,
      @RequestParam(value = "type") String type) {
    return trendingBetService
        .getTrendingBetsByBrand(brand, type)
        .orElseThrow(NotFoundException::new);
  }
}
