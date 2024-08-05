package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.RacingEdpMarketDto;
import com.ladbrokescoral.oxygen.cms.api.controller.mapping.RacingEdpMarketsMapper;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RacingEdpMarket;
import com.ladbrokescoral.oxygen.cms.api.service.RacingEdpMarketService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController
public class RacingEdpMarkets extends AbstractSortableController<RacingEdpMarket> {

  @Autowired
  public RacingEdpMarkets(RacingEdpMarketService crudService) {
    super(crudService);
  }

  @GetMapping("racing-edp-market/brand/{brand}")
  @Override
  public List<RacingEdpMarket> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @PostMapping("racing-edp-market")
  public ResponseEntity<RacingEdpMarket> create(@Valid @RequestBody RacingEdpMarketDto dto) {

    return super.create(RacingEdpMarketsMapper.ENTITY_MAPPER.toEntity(dto));
  }

  @PutMapping("racing-edp-market/{id}")
  public RacingEdpMarket update(
      @PathVariable String id, @Valid @RequestBody RacingEdpMarketDto dto) {
    return super.update(id, RacingEdpMarketsMapper.ENTITY_MAPPER.toEntity(dto));
  }

  @GetMapping("racing-edp-market/{id}")
  @Override
  public RacingEdpMarket read(@PathVariable String id) {
    return super.read(id);
  }

  @DeleteMapping("racing-edp-market/{id}")
  @Override
  public ResponseEntity<RacingEdpMarket> delete(@PathVariable String id) {
    return super.delete(id);
  }

  @GetMapping("racing-edp-market")
  @Override
  public List<RacingEdpMarket> readAll() {
    return super.readAll();
  }

  @PostMapping("racing-edp-market/ordering")
  @Override
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
