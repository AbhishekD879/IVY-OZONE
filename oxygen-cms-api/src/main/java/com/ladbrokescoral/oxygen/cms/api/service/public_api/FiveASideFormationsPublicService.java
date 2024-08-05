package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.FiveASideFormationDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.FiveASideFormationMapper;
import com.ladbrokescoral.oxygen.cms.api.service.FiveASideFormationService;
import java.util.List;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class FiveASideFormationsPublicService {
  private final FiveASideFormationService fiveASideFormationService;

  public List<FiveASideFormationDto> findAll(String brand) {
    return fiveASideFormationService.findByBrand(brand).stream()
        .map(FiveASideFormationMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
