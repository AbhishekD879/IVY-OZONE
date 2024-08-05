package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.dto.SeoPageDto;
import com.ladbrokescoral.oxygen.cms.api.dto.SeoSitemapDto;
import com.ladbrokescoral.oxygen.cms.api.entity.SeoPage;
import com.ladbrokescoral.oxygen.cms.api.mapping.DtoMapper;
import com.ladbrokescoral.oxygen.cms.api.mapping.SeoPageMapper;
import com.ladbrokescoral.oxygen.cms.api.service.SeoPageService;
import java.util.Map;
import java.util.Optional;
import org.springframework.stereotype.Service;

@Service
public class SeoPagePublicService {

  private final SeoPageService service;

  public SeoPagePublicService(SeoPageService service) {
    this.service = service;
  }

  public Map<String, String> find(String brand) {
    return SeoPageMapper.toDto(service.findAllByBrandAndDisabled(brand));
  }

  @FortifyXSSValidate("return")
  public Optional<SeoPageDto> find(String brand, String id) {
    Optional<SeoPage> maybeSeoPage = service.findOneByIdAndBrand(id, brand);
    return maybeSeoPage.map(SeoPageMapper.INSTANCE::toDto);
  }

  public Map<String, SeoSitemapDto> findSeoSitemap(String brand) {
    return DtoMapper.toDtoSeoSitemap(service.findAllByBrandAndDisabled(brand));
  }
}
