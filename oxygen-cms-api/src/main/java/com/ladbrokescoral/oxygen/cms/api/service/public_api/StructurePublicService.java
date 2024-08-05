package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.StructureDto;
import com.ladbrokescoral.oxygen.cms.api.exception.EmptyConfigurationStructureException;
import com.ladbrokescoral.oxygen.cms.api.service.StructureService;
import java.text.MessageFormat;
import java.util.Map;
import java.util.Optional;
import org.springframework.stereotype.Service;

@Service
public class StructurePublicService {

  private final StructureService service;

  public StructurePublicService(StructureService service) {
    this.service = service;
  }

  public Optional<Map<String, Map<String, Object>>> find(String brand) {
    return service.findStructureByBrand(brand).map(StructureDto::getStructure);
  }

  public Optional<Map<String, Object>> findElement(String brand, String configName) {
    return service.findByBrandAndConfigName(brand, configName);
  }

  public Map<String, Map<String, Object>> getInitialDataConfiguration(String brand) {
    return service
        .findInitialDataStructure(brand)
        .map(StructureDto::getStructure)
        .orElseThrow(
            () ->
                new EmptyConfigurationStructureException(
                    MessageFormat.format("Cannot find structure for brand {0}", brand)));
  }
}
