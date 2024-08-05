package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.MarketLinkDto;
import com.ladbrokescoral.oxygen.cms.api.entity.MarketLink;
import com.ladbrokescoral.oxygen.cms.api.service.CrudService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.util.List;
import javax.validation.Valid;
import org.springframework.beans.BeanUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class MarketLinks extends AbstractCrudController<MarketLink> {

  @Autowired
  public MarketLinks(CrudService<MarketLink> crudService) {
    super(crudService);
  }

  @PostMapping("statistics-links/market-links")
  public ResponseEntity<MarketLink> create(@RequestBody @Valid MarketLinkDto marketLinkDto) {
    MarketLink marketLink = new MarketLink();
    BeanUtils.copyProperties(marketLinkDto, marketLink);
    return super.create(marketLink);
  }

  @GetMapping("statistics-links/market-links/{id}")
  @Override
  public MarketLink read(@PathVariable String id) {
    return super.read(id);
  }

  @GetMapping("statistics-links/market-links/brand/{brand}")
  @Override
  public List<MarketLink> readByBrand(@PathVariable @Brand String brand) {
    return super.readByBrand(brand);
  }

  @PutMapping("statistics-links/market-links/{id}")
  public MarketLink update(
      @PathVariable String id, @RequestBody @Valid MarketLinkDto marketLinkDto) {
    MarketLink marketLink = new MarketLink();
    BeanUtils.copyProperties(marketLinkDto, marketLink);
    return super.update(id, marketLink);
  }

  @DeleteMapping("statistics-links/market-links/{id}")
  @Override
  public ResponseEntity<MarketLink> delete(@PathVariable String id) {
    return super.delete(id);
  }
}
