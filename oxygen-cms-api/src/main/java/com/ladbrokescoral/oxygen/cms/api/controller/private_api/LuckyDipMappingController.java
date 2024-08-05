package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipMappingDto;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipMapping;
import com.ladbrokescoral.oxygen.cms.api.exception.LuckyDipMappingNotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipMappingService;
import java.util.List;
import javax.validation.Valid;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class LuckyDipMappingController extends AbstractSortableController<LuckyDipMapping> {

  private final LuckyDipMappingService luckyDipMappingService;
  private static final String ERR_MSG =
      "Error while fetching LuckyDipMapping config for the given brand";

  public LuckyDipMappingController(LuckyDipMappingService luckyDipMappingService) {
    super(luckyDipMappingService);
    this.luckyDipMappingService = luckyDipMappingService;
  }

  @PostMapping("{brand}/lucky-dip-mapping")
  public ResponseEntity<LuckyDipMapping> create(
      @PathVariable("brand") String brand,
      @RequestBody @Valid LuckyDipMappingDto luckyDipMappingDto) {
    LuckyDipMapping luckyDipMapping = luckyDipMappingService.convertDtoToEntity(luckyDipMappingDto);
    if (!brand.equalsIgnoreCase(luckyDipMapping.getBrand())) {
      throw new LuckyDipMappingNotFoundException(
          "Brand does not match the given LuckyDip brand value");
    }
    luckyDipMappingService.validateCategoryAndTypeIds(luckyDipMapping);
    return super.create(luckyDipMapping);
  }

  @PutMapping("{brand}/lucky-dip-mapping/{id}")
  public LuckyDipMapping update(
      @PathVariable("brand") String brand,
      @PathVariable String id,
      @RequestBody @Valid LuckyDipMappingDto luckyDipMappingDto) {
    LuckyDipMapping luckyDipMapping = luckyDipMappingService.convertDtoToEntity(luckyDipMappingDto);
    if (!brand.equalsIgnoreCase(luckyDipMapping.getBrand())) {
      throw new LuckyDipMappingNotFoundException(ERR_MSG);
    }
    luckyDipMappingService.validateCategoryAndTypeIds(luckyDipMapping);
    return super.update(id, luckyDipMapping);
  }

  @GetMapping("lucky-dip-mapping/brand/{brand}")
  @Override
  public List<LuckyDipMapping> readByBrand(@PathVariable String brand) {
    return super.readByBrand(brand);
  }

  @GetMapping("{brand}/lucky-dip-mapping/{id}")
  public LuckyDipMapping read(@PathVariable("brand") String brand, @PathVariable String id) {
    LuckyDipMapping luckyDipMapping = super.read(id);
    if (!brand.equalsIgnoreCase(luckyDipMapping.getBrand())) {
      throw new LuckyDipMappingNotFoundException(ERR_MSG);
    }
    return luckyDipMapping;
  }

  @DeleteMapping("{brand}/lucky-dip-mapping/{id}")
  public ResponseEntity<LuckyDipMapping> delete(
      @PathVariable("brand") String brand, @PathVariable String id) {
    LuckyDipMapping luckyDipMapping = super.read(id);
    if (!brand.equalsIgnoreCase(luckyDipMapping.getBrand())) {
      throw new LuckyDipMappingNotFoundException(ERR_MSG);
    }
    return super.delete(id);
  }

  @Override
  @PostMapping("lucky-dip-mapping/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
