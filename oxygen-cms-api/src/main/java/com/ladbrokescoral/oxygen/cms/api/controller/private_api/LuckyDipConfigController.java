package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.LuckyDipConfigurationDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LuckyDipConfiguration;
import com.ladbrokescoral.oxygen.cms.api.service.LuckyDipConfigService;
import java.util.List;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
public class LuckyDipConfigController extends AbstractCrudController<LuckyDipConfiguration> {

  private final LuckyDipConfigService luckyDipConfigService;

  @Autowired
  public LuckyDipConfigController(LuckyDipConfigService luckyDipConfigService) {
    super(luckyDipConfigService);
    this.luckyDipConfigService = luckyDipConfigService;
  }

  @PostMapping("luckydip")
  public ResponseEntity<LuckyDipConfiguration> create(
      @RequestBody LuckyDipConfigurationDto luckyDipConfigurationDto) {
    return super.create(luckyDipConfigService.convertDtoToEntity(luckyDipConfigurationDto));
  }

  @PutMapping("luckydip/{id}")
  public LuckyDipConfiguration update(
      @PathVariable String id, @RequestBody LuckyDipConfigurationDto luckyDipConfigurationDto) {
    return super.update(id, luckyDipConfigService.convertDtoToEntity(luckyDipConfigurationDto));
  }

  @GetMapping("luckydip/brand/{brand}")
  public LuckyDipConfiguration findLuckyDipConfigByBrand(@PathVariable("brand") String brand) {
    List<LuckyDipConfiguration> lDFieldsConfigurationList =
        luckyDipConfigService.findByBrand(brand);
    return !lDFieldsConfigurationList.isEmpty()
        ? lDFieldsConfigurationList.get(0)
        : new LuckyDipConfiguration();
  }
}
