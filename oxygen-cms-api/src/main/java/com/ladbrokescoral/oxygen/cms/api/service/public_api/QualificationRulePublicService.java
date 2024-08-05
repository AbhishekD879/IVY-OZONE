package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.QualificationRuleDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.QualificationRuleMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.QualificationRuleRepository;
import java.util.Optional;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class QualificationRulePublicService {
  private final QualificationRuleRepository qualificationRuleRepository;

  public Optional<QualificationRuleDto> findByBrand(String brand) {
    return qualificationRuleRepository
        .findOneByBrandAndEnabledIsTrue(brand)
        .map(QualificationRuleMapper.getInstance()::toDto);
  }
}
