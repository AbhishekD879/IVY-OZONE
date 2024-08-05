package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.FooterLogoDto;
import com.ladbrokescoral.oxygen.cms.api.dto.FooterLogoNativeDto;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterLogo;
import com.ladbrokescoral.oxygen.cms.api.mapping.FooterLogoMapper;
import com.ladbrokescoral.oxygen.cms.api.service.FooterLogoService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class FooterLogoPublicService {

  private final FooterLogoService service;

  public FooterLogoPublicService(FooterLogoService service) {
    this.service = service;
  }

  public List<FooterLogoDto> find(String brand) {
    List<FooterLogo> footerLogoCollection = service.findAllByBrandAndDisabled(brand);
    return footerLogoCollection.stream()
        .map(FooterLogoMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }

  public List<FooterLogoNativeDto> findNative(String brand) {
    List<FooterLogo> footerLogoCollection = service.findAllByBrandAndDisabled(brand);
    return footerLogoCollection.stream()
        .map(FooterLogoMapper.INSTANCE::toDtoNative)
        .collect(Collectors.toList());
  }
}
