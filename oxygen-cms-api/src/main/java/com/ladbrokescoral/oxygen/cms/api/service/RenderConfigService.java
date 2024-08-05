package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.RenderConfig;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.RenderConfigRepository;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class RenderConfigService extends AbstractService<RenderConfig> {

  private static final List<String> AVAILABLE_DEVICES = Arrays.asList("MOBILE", "DESKTOP");

  @Autowired
  public RenderConfigService(RenderConfigRepository repository) {
    super(repository);
  }

  public void validate(RenderConfig entity) {
    if (!AVAILABLE_DEVICES.contains(entity.getDevice().toUpperCase())) {
      throw new ValidationException("SSR Config device types has to be in: " + AVAILABLE_DEVICES);
    }

    if (entity.getPath().contains(" ")) {
      throw new ValidationException("SSR Config path shouldn't contain spaces");
    }
    List<RenderConfig> configs = repository.findByBrand(entity.getBrand());
    Optional<RenderConfig> renderConfig =
        configs.stream()
            .filter(
                config ->
                    config
                        .getPath()
                        .replace("/", "")
                        .equalsIgnoreCase(entity.getPath().replace("/", "")))
            .filter(config -> config.getDevice().equalsIgnoreCase(entity.getDevice()))
            .filter(config -> config.getEnabled().equals(entity.getEnabled()))
            .findAny();
    if (renderConfig.isPresent()) {
      throw new ValidationException("SSR Config has to be unique");
    }
  }
}
