package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipV2ConfigurationDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipV2Config;
import com.ladbrokescoral.oxygen.cms.api.exception.LuckyDipConfigNotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipV2ConfigService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.data.domain.Sort;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class LuckyDipV2ConfigController extends AbstractCrudController<LuckyDipV2Config> {

  private final LuckyDipV2ConfigService luckyDipV2ConfigService;
  private static final String ERR_MSG = "Error while fetching Lucky Dip config for the given brand";

  @Autowired
  public LuckyDipV2ConfigController(LuckyDipV2ConfigService luckyDipV2ConfigService) {
    super(luckyDipV2ConfigService);
    this.luckyDipV2ConfigService = luckyDipV2ConfigService;
  }

  @PostMapping("{brand}/lucky-dip")
  public ResponseEntity<LuckyDipV2Config> create(
      @PathVariable("brand") String brand,
      @RequestBody LuckyDipV2ConfigurationDto luckyDipConfigurationDto) {
    if (!brand.equalsIgnoreCase(luckyDipConfigurationDto.getBrand())) {
      throw new LuckyDipConfigNotFoundException(
          "Brand does not match the given LuckyDip brand value");
    }
    return super.create(luckyDipV2ConfigService.convertDtoToEntity(luckyDipConfigurationDto));
  }

  @PutMapping("{brand}/lucky-dip/{id}")
  public LuckyDipV2Config update(
      @PathVariable("brand") String brand,
      @PathVariable String id,
      @RequestBody LuckyDipV2ConfigurationDto luckyDipConfigurationDto) {
    if (!brand.equalsIgnoreCase(luckyDipConfigurationDto.getBrand())) {
      throw new LuckyDipConfigNotFoundException(ERR_MSG);
    }
    return super.update(id, luckyDipV2ConfigService.convertDtoToEntity(luckyDipConfigurationDto));
  }

  @GetMapping("{brand}/lucky-dip/{id}")
  public LuckyDipV2Config read(@PathVariable("brand") String brand, @PathVariable String id) {
    LuckyDipV2Config luckyDipV2Config = super.read(id);
    if (!brand.equalsIgnoreCase(luckyDipV2Config.getBrand())) {
      throw new LuckyDipConfigNotFoundException(ERR_MSG);
    }
    return luckyDipV2Config;
  }

  @DeleteMapping("{brand}/lucky-dip/{id}")
  public ResponseEntity<LuckyDipV2Config> delete(
      @PathVariable("brand") String brand, @PathVariable("id") String id) {
    LuckyDipV2Config luckyDipV2Config = super.read(id);
    if (!brand.equalsIgnoreCase(luckyDipV2Config.getBrand())) {
      throw new LuckyDipConfigNotFoundException(ERR_MSG);
    }
    return super.delete(id);
  }

  @GetMapping("lucky-dip/brand/{brand}")
  public List<LuckyDipV2Config> findAllLuckyDipConfigByBrand(
      @PathVariable("brand") String brand, Sort sort) {
    return luckyDipV2ConfigService.findAllLuckyDipConfigByBrand(brand, sort);
  }
}
