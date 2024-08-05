package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OnBoardingGuideDto;
import com.ladbrokescoral.oxygen.cms.api.entity.OnBoardingGuide;
import com.ladbrokescoral.oxygen.cms.api.mapping.OnBoardingGuideMapper;
import com.ladbrokescoral.oxygen.cms.api.service.OnBoardingGuideService;
import java.util.List;
import java.util.stream.Collectors;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class OnBoardingGuidePublicService {

  private final OnBoardingGuideService privateService;

  public List<OnBoardingGuideDto> getOnBoardingGuides(String brand) {
    return privateService.findByBrand(brand).stream()
        .filter(OnBoardingGuide::isEnabled)
        .map(OnBoardingGuideMapper.INSTANCE::toDto)
        .collect(Collectors.toList());
  }
}
