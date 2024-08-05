package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.DesktopQuickLinkDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.DesktopQuickLinkMapper;
import com.ladbrokescoral.oxygen.cms.api.service.ApiService;
import com.ladbrokescoral.oxygen.cms.api.service.DesktopQuickLinkService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

@Service
public class DesktopQuickLinkPublicService implements ApiService<DesktopQuickLinkDto> {

  private final DesktopQuickLinkService service;

  @Autowired
  public DesktopQuickLinkPublicService(DesktopQuickLinkService service) {
    this.service = service;
  }

  public List<DesktopQuickLinkDto> findByBrand(String brand) {
    return service.findAllByBrandAndDisabled(brand).stream()
        .map(DesktopQuickLinkMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
