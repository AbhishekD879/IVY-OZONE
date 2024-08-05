package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.OtfIosAppToggleDto;
import com.ladbrokescoral.oxygen.cms.api.entity.OtfIosAppToggle;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.mapping.OtfIosAppToggleMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.OtfIosAppToggleRepository;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;

@Service
@RequiredArgsConstructor
public class OtfIosAppTogglePublicService {
  private final OtfIosAppToggleRepository repository;

  public OtfIosAppToggleDto findByBrand(String brand) {
    OtfIosAppToggle toggle = repository.findOneByBrand(brand).orElseThrow(NotFoundException::new);

    return OtfIosAppToggleMapper.getInstance().toDto(toggle);
  }
}
