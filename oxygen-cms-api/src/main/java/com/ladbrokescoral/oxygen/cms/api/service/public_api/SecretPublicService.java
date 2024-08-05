package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.SecretDetailedDto;
import com.ladbrokescoral.oxygen.cms.api.mapping.SecretMapper;
import com.ladbrokescoral.oxygen.cms.api.service.SecretService;
import java.util.Optional;
import lombok.extern.slf4j.Slf4j;
import org.springframework.stereotype.Service;

@Slf4j
@Service
public class SecretPublicService {

  private final SecretService service;
  private final SecretMapper mapper;

  public SecretPublicService(SecretService service, SecretMapper mapper) {
    this.service = service;
    this.mapper = mapper;
  }

  public Optional<SecretDetailedDto> findSecret(String brand, String uri) {
    log.info("Secrets search by {} and {} uri", brand, uri);
    return service.readActiveByBrandAndUri(brand, uri).map(mapper::toDetailedDto);
  }
}
