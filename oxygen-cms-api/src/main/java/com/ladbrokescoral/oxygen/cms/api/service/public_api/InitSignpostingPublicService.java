package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.InitSignpostingDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.InitSignpostingMapper;
import com.ladbrokescoral.oxygen.cms.api.service.PromotionService;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class InitSignpostingPublicService {

  private final PromotionService service;

  public InitSignpostingPublicService(PromotionService service) {
    this.service = service;
  }

  public List<InitSignpostingDto> find(String brand) {
    return service.findSignpostingPromotions(brand).stream()
        .map(InitSignpostingMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
