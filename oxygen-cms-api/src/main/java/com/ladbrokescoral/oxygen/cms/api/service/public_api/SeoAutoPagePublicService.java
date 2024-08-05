package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SeoAutoInitDataDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.SeoAutoPageMapper;
import com.ladbrokescoral.oxygen.cms.api.service.SeoAutoPageService;
import java.util.*;
import org.springframework.stereotype.Service;

@Service
public class SeoAutoPagePublicService {

  private final SeoAutoPageService service;

  public SeoAutoPagePublicService(SeoAutoPageService service) {
    this.service = service;
  }

  public Map<String, SeoAutoInitDataDto> find(String brand) {
    return SeoAutoPageMapper.toDto(service.findAllByBrand(brand));
  }
}
