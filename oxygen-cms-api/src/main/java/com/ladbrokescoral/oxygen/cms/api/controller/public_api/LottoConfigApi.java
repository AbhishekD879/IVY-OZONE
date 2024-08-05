package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.LottoBannerConfigDTO;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.LottoConfigService;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RestController;

@RestController
@RequiredArgsConstructor
public class LottoConfigApi implements Public {
  private final LottoConfigService lottoConfigService;

  @GetMapping(value = {"{brand}/lotto-config"})
  public LottoBannerConfigDTO findAllLottoConfigByBrand(@PathVariable("brand") String brand) {
    return lottoConfigService.readByBrand(brand).orElseThrow(NotFoundException::new);
  }
}
