package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.dto.LottoBannerConfigDTO;
import com.ladbrokescoral.oxygen.cms.api.dto.LottoConfigDTO;
import com.ladbrokescoral.oxygen.cms.api.dto.OrderDto;
import com.ladbrokescoral.oxygen.cms.api.entity.LottoConfig;
import com.ladbrokescoral.oxygen.cms.api.service.LottoConfigService;
import com.ladbrokescoral.oxygen.cms.api.service.validators.Brand;
import java.util.ArrayList;
import javax.validation.Valid;
import org.modelmapper.ModelMapper;
import org.springframework.http.ResponseEntity;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
public class LottoConfigs extends AbstractSortableController<LottoConfig> {

  private final LottoConfigService lottoConfigService;
  private final ModelMapper mapper;

  public LottoConfigs(LottoConfigService lottoConfigService, ModelMapper mapper) {
    super(lottoConfigService);
    this.lottoConfigService = lottoConfigService;
    this.mapper = mapper;
  }

  @PostMapping("lotto-config")
  public ResponseEntity<LottoConfig> create(
      @Valid @Validated @RequestBody LottoConfigDTO lottoConfigDTO) {
    LottoConfig entity = mapper.map(lottoConfigDTO, LottoConfig.class);
    return super.create(entity);
  }

  @PutMapping("lotto-config/{id}")
  public LottoConfig update(
      @PathVariable("id") String id, @Valid @Validated @RequestBody LottoConfigDTO lottoConfigDTO) {
    LottoConfig updateEntity = mapper.map(lottoConfigDTO, LottoConfig.class);
    return super.update(id, updateEntity);
  }

  @DeleteMapping("lotto-config/{id}")
  @Override
  public ResponseEntity<LottoConfig> delete(@PathVariable("id") String id) {
    return super.delete(id);
  }

  @PutMapping("lotto-config/banner-link/brand/{brand}")
  public void update(
      @Valid @Validated @RequestBody LottoBannerConfigDTO lottoBannerConfigDTO,
      @Valid @Validated @Brand @PathVariable("brand") String brand) {
    lottoConfigService.updateBannerLink(lottoBannerConfigDTO, brand);
  }

  @GetMapping("lotto-config/brand/{brand}")
  public LottoBannerConfigDTO findByBrand(
      @Valid @Validated @Brand @PathVariable("brand") String brand) {
    return lottoConfigService
        .readByBrand(brand)
        .orElse(LottoBannerConfigDTO.builder().lottoConfig(new ArrayList<>()).build());
  }

  @Override
  @GetMapping("lotto-config/{id}")
  public LottoConfig read(@PathVariable("id") String id) {
    return super.read(id);
  }

  @Override
  @PostMapping("lotto-config/ordering")
  public void order(@RequestBody OrderDto newOrder) {
    super.order(newOrder);
  }
}
