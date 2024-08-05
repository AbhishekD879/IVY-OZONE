package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.StaticTextOtfDto;
import com.ladbrokescoral.oxygen.cms.api.entity.StaticTextOtf;
import com.ladbrokescoral.oxygen.cms.api.mapping.StaticTextOtfMapper;
import com.ladbrokescoral.oxygen.cms.api.service.StaticTextOtfService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class StaticTextOtfPublicService {

  private final StaticTextOtfService staticTextService;

  public StaticTextOtfPublicService(StaticTextOtfService staticTextService) {
    this.staticTextService = staticTextService;
  }

  public List<StaticTextOtfDto> findEnabledByBrand(String brand) {
    return staticTextService.findByBrand(brand).stream()
        .filter(StaticTextOtf::isEnabled)
        .map(StaticTextOtfMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
