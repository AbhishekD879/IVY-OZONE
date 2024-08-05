package com.ladbrokescoral.oxygen.cms.api.service;

import com.fortify.annotations.FortifyXSSValidate;
import com.ladbrokescoral.oxygen.cms.api.entity.SimpleModule;
import com.ladbrokescoral.oxygen.cms.api.entity.SportsFeaturedTab;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.SportsFeaturedTabRepository;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import java.util.UUID;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class SportsFeaturedTabService extends AbstractService<SportsFeaturedTab> {
  private final SportsFeaturedTabRepository sportsFeaturedTabRepository;

  @Autowired
  public SportsFeaturedTabService(SportsFeaturedTabRepository sportsFeaturedTabRepository) {
    super(sportsFeaturedTabRepository);
    this.sportsFeaturedTabRepository = sportsFeaturedTabRepository;
  }

  @Override
  public <S extends SportsFeaturedTab> S save(S entity) {
    entity.setPath(stripLeadingSlashFromPath(entity.getPath()));
    if (!entity.isDisabled()) {
      checkIfSuchFeaturedTabExistsAndEnabled(entity);
    }
    return sportsFeaturedTabRepository.save(entity);
  }

  // check if enabled featuredTab entity with such path and brand already exist
  private <S extends SportsFeaturedTab> void checkIfSuchFeaturedTabExistsAndEnabled(S entity) {
    findEnabledByBrandAndPath(entity.getBrand(), entity.getPath())
        .filter(e -> !e.getId().equals(entity.getId())) // allows updating itself
        .ifPresent(
            e -> {
              String msg =
                  String.format(
                      "SportsFeaturedTab for brand=%s with path=%s already exist",
                      e.getBrand(), e.getPath());
              throw new ValidationException(msg);
            });
  }

  private String stripLeadingSlashFromPath(String path) {
    return path.replaceAll("^/+", "");
  }

  @FortifyXSSValidate("return")
  @Override
  public Optional<SportsFeaturedTab> findOne(String id) {
    return sportsFeaturedTabRepository
        .findById(id)
        .map(
            featuredTab -> {
              Collections.sort(featuredTab.getModules());
              return featuredTab;
            });
  }

  public Optional<SportsFeaturedTab> addNewModule(String featureTabId, SimpleModule module) {
    UUID newModuleId = UUID.randomUUID();
    module.setId(newModuleId.toString());

    return findOne(featureTabId)
        .map(
            featuredTab -> {
              featuredTab.getModules().add(module);
              return featuredTab;
            })
        .map(this::save);
  }

  public Optional<SportsFeaturedTab> removeModule(String featureTabId, String moduleId) {
    return findOne(featureTabId)
        .map(
            featuredTab -> {
              if (featuredTab.getModules().removeIf(sm -> sm.getId().equals(moduleId))) {
                return featuredTab;
              } else {
                return null;
              }
            })
        .map(this::save);
  }

  public Optional<SportsFeaturedTab> updateModule(String featureTabId, SimpleModule module) {
    return findOne(featureTabId)
        .map(
            featuredTab -> {
              if (featuredTab.getModules().removeIf(sm -> sm.getId().equals(module.getId()))) {
                featuredTab.getModules().add(module);
                return featuredTab;
              } else {
                return null;
              }
            })
        .map(this::save);
  }

  public Optional<List<SimpleModule>> getModules(String featureTabId) {
    return findOne(featureTabId)
        .map(SportsFeaturedTab::getModules)
        .map(
            modules -> {
              Collections.sort(modules);
              return modules;
            });
  }

  public Optional<SimpleModule> getModule(String id, String moduleId) {
    return findOne(id).flatMap(featuredTab -> featuredTab.getModule(moduleId));
  }

  public Optional<SportsFeaturedTab> findEnabledByBrandAndPath(String brand, String path) {
    return Optional.ofNullable(
            sportsFeaturedTabRepository.findByBrandIgnoreCaseAndPathIgnoreCaseAndDisabledIsFalse(
                brand, path))
        .map(
            featuredTab -> {
              Collections.sort(featuredTab.getModules());
              return featuredTab;
            });
  }
}
