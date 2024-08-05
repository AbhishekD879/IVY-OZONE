package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.StructureDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfigProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfigPropertyType;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfiguration;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.exception.SvgImageParseException;
import com.ladbrokescoral.oxygen.cms.api.mapping.SystemConfigurationMapper;
import com.ladbrokescoral.oxygen.cms.api.repository.SystemConfigurationRepository;
import com.ladbrokescoral.oxygen.cms.util.PathUtil;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.Collection;
import java.util.List;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import java.util.function.Function;
import java.util.function.Predicate;
import java.util.stream.Collectors;
import lombok.extern.slf4j.Slf4j;
import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.springframework.web.multipart.MultipartFile;

@Slf4j
@Component
public class StructureService extends AbstractService<SystemConfiguration> {

  private final SystemConfigurationRepository systemConfigurationRepository;
  private final ImageService imageService;
  private final SvgImageParser svgImageParser;
  private final String imageStructurePath;

  @Autowired
  public StructureService(
      SystemConfigurationRepository systemConfigurationRepository,
      ImageService imageService,
      SvgImageParser svgImageParser,
      @Value("${images.structure.path}") String imageStructurePath) {
    super(systemConfigurationRepository);
    this.systemConfigurationRepository = systemConfigurationRepository;
    this.imageService = imageService;
    this.svgImageParser = svgImageParser;
    this.imageStructurePath = imageStructurePath;
  }

  public List<StructureDto> findAllStructures() {
    Map<String, List<SystemConfiguration>> byBrand =
        systemConfigurationRepository.findAll().stream()
            .collect(Collectors.groupingBy(SystemConfiguration::getBrand));
    return byBrand.entrySet().stream()
        .map(e -> SystemConfigurationMapper.INSTANCE.toStructureDto(e.getKey(), e.getValue()))
        .collect(Collectors.toList());
  }

  public Optional<StructureDto> findStructureByBrand(String brand) {
    Collection<SystemConfiguration> brandConfigurations =
        systemConfigurationRepository.findByBrand(brand);
    if (brandConfigurations.isEmpty()) {
      return Optional.empty();
    }
    return Optional.of(
        SystemConfigurationMapper.INSTANCE.toStructureDto(brand, brandConfigurations));
  }

  public Optional<StructureDto> findInitialDataStructure(String brand) {
    Collection<SystemConfiguration> initialConfigs =
        systemConfigurationRepository.findAllByBrandAndIsInitialDataConfigIsTrue(brand);
    return Optional.of(SystemConfigurationMapper.INSTANCE.toStructureDto(brand, initialConfigs));
  }

  public Optional<Map<String, Object>> findByBrandAndConfigName(String brand, String elementName) {
    Optional<SystemConfiguration> config =
        systemConfigurationRepository.findOneByBrandAndName(brand, elementName);
    return config.map(
        c -> SystemConfigurationMapper.INSTANCE.getStructureProperties(c.getProperties()));
  }

  public Optional<Object> findValueByProperty(String brand, String configName, String property) {
    return findByBrandAndConfigName(brand, configName).map(config -> config.get(property));
  }

  public StructureDto updateStructure(String brand, StructureDto entity) {
    List<SystemConfiguration> allConfigs = systemConfigurationRepository.findByBrand(brand);
    if (allConfigs.isEmpty()) {
      throw new NotFoundException("Configs for brand " + brand);
    }
    Map<String, Map<String, Object>> newStructure = entity.getStructure();
    List<SystemConfiguration> updated =
        allConfigs.stream()
            .filter(config -> newStructure.containsKey(config.getName()))
            .filter(config -> updateStructureProperties(config, newStructure.get(config.getName())))
            .collect(Collectors.toList());
    systemConfigurationRepository.saveAll(updated);
    return SystemConfigurationMapper.INSTANCE.toStructureDto(brand, allConfigs);
  }

  public void resetToDefaultForBrand(String brand) {
    List<SystemConfiguration> allConfigs = systemConfigurationRepository.findByBrand(brand);
    List<SystemConfiguration> updated =
        allConfigs.stream().filter(this::resetToDefaultProperties).collect(Collectors.toList());
    systemConfigurationRepository.saveAll(updated);
  }

  public Optional<StructureDto> updateStructureItem(
      String brand, String configName, Map<String, Object> properties) {

    return systemConfigurationRepository
        .findOneByBrandAndName(brand, configName)
        .map(
            (SystemConfiguration structure) -> {
              updateStructureProperties(structure, properties);
              return structure;
            })
        .map(this::save)
        .flatMap(anyFound -> findStructureByBrand(brand));
  }

  public Optional<StructureDto> resetToDefaultItem(String brand, String elementName) {
    return systemConfigurationRepository
        .findOneByBrandAndName(brand, elementName)
        .map(
            (SystemConfiguration structure) -> {
              resetToDefaultProperties(structure);
              return structure;
            })
        .map(this::save)
        .flatMap(anyFound -> findStructureByBrand(brand));
  }

  private boolean resetToDefaultProperties(SystemConfiguration config) {
    return updateStructureProperties(
        config,
        p -> true,
        p -> SystemConfigPropertyType.from(p.getType()).parseDefaultStructureValue(p.getValue()));
  }

  private boolean resetToDefaultProperties(SystemConfiguration config, String propertyName) {
    return updateStructureProperties(
        config,
        p -> p.getName().equals(propertyName),
        p -> SystemConfigPropertyType.from(p.getType()).parseDefaultStructureValue(p.getValue()));
  }

  private boolean updateStructureProperties(
      SystemConfiguration config, Map<String, Object> properties) {
    return updateStructureProperties(
        config, p -> properties.containsKey(p.getName()), p -> properties.get(p.getName()));
  }

  private boolean updateStructureProperties(
      SystemConfiguration config,
      Predicate<SystemConfigProperty> shouldBeUpdated,
      Function<SystemConfigProperty, Object> newPropertyValue) {
    long updatedProperties =
        config.getProperties().stream()
            .filter(shouldBeUpdated)
            .filter(p -> !Objects.equals(p.getStructureValue(), newPropertyValue.apply(p)))
            .peek(p -> p.setStructureValue(newPropertyValue.apply(p)))
            .count();
    return updatedProperties > 0;
  }

  public Optional<String> uploadImage(
      String brand, String elementName, String propertyName, MultipartFile file) {

    Optional<String> maybeUploaded = uploadImage(brand, file);
    maybeUploaded.ifPresent(
        pathOfUploadedImage ->
            saveStructureProperty(brand, elementName, propertyName, pathOfUploadedImage));

    return maybeUploaded;
  }

  public Optional<String> uploadSvg(
      String brand, String elementName, String propertyName, MultipartFile svgFile) {
    Svg svg = svgImageParser.parse(svgFile).orElseThrow(SvgImageParseException::new);

    Optional<String> maybeUploadedSvg = uploadImage(brand, svgFile);
    maybeUploadedSvg.ifPresent(
        (String pathOfUploadedImage) -> {
          svg.setPath(pathOfUploadedImage);
          saveStructureProperty(brand, elementName, propertyName, svg);
        });

    return maybeUploadedSvg;
  }

  private void saveStructureProperty(
      String brand, String elementName, String propertyName, Object value) {
    SystemConfiguration systemConfiguration =
        systemConfigurationRepository
            .findOneByBrandAndName(brand, elementName)
            .orElseThrow(NotFoundException::new);
    SystemConfigProperty configProperty =
        systemConfiguration.getProperty(propertyName).orElseThrow(NotFoundException::new);
    configProperty.setStructureValue(value);
    systemConfigurationRepository.save(systemConfiguration);
  }

  private Optional<String> uploadImage(String brand, MultipartFile file) {
    return imageService
        .upload(brand, file, imageStructurePath)
        .map(Filename::getFilename)
        .map(
            fileName ->
                Paths.get(PathUtil.normalize(imageStructurePath), PathUtil.normalize(fileName)))
        .map(Path::toString);
  }

  public Optional<StructureDto> removeImage(String brand, String configName, String propertyName) {
    return systemConfigurationRepository
        .findOneByBrandAndName(brand, configName)
        .map(config -> removeImageAndSave(config, propertyName))
        .flatMap(config -> findStructureByBrand(brand));
  }

  private SystemConfiguration removeImageAndSave(SystemConfiguration config, String propertyName) {
    SystemConfigProperty property =
        config.getProperty(propertyName).orElseThrow(NotFoundException::new);
    if (Objects.equals(property.getValue(), property.getStructureValue())) {
      throw new IllegalArgumentException("Cannot remove default config image");
    }

    String path = getImagePath(property.getStructureValue());
    if (StringUtils.isNotEmpty(path)) {
      Boolean deleted = imageService.removeImage(config.getBrand(), path);
      log.info("File {} removal status : {}", path, deleted);
    }
    resetToDefaultProperties(config, propertyName);
    return systemConfigurationRepository.save(config);
  }

  private String getImagePath(Object structureValue) {
    String path = null;

    if (structureValue instanceof Svg) {
      path = Optional.ofNullable(((Svg) structureValue).getPath()).orElse("");
    } else if (structureValue instanceof Map) {
      // where it can be set with map?
      path = (String) ((Map) structureValue).getOrDefault("path", "");
    } else if (Objects.nonNull(structureValue)) {
      path = structureValue.toString();
    }
    return path;
  }
}
