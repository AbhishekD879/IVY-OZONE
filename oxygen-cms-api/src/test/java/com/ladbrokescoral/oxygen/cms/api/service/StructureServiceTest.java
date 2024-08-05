package com.ladbrokescoral.oxygen.cms.api.service;

import static com.ladbrokescoral.oxygen.cms.api.entity.SystemConfigPropertyType.SVG;
import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertFalse;
import static org.junit.Assert.assertTrue;
import static org.mockito.AdditionalAnswers.returnsFirstArg;

import com.ladbrokescoral.oxygen.cms.api.dto.StructureDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Svg;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfigProperty;
import com.ladbrokescoral.oxygen.cms.api.entity.SystemConfiguration;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.repository.SystemConfigurationRepository;
import java.nio.file.Paths;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class StructureServiceTest extends BDDMockito {

  private StructureService structureService;
  @Mock private SystemConfigurationRepository configurationRepository;
  @Mock private ImageService imageService;
  @Mock private SvgImageParser svgImageParser;
  @Mock MultipartFile file;

  private String imageStructurePath;

  private SystemConfiguration systemConfiguration;
  private String brand = "bma";
  private String configName = "element";

  @Before
  public void setUp() {
    imageStructurePath = "uploads/structure";
    structureService =
        new StructureService(
            configurationRepository, imageService, svgImageParser, imageStructurePath);

    Filename filename = new Filename();
    filename.setFilename("fileName");
    when(imageService.upload(anyString(), eq(file), eq(imageStructurePath)))
        .thenReturn(Optional.of(filename));

    systemConfiguration = new SystemConfiguration();
    systemConfiguration.setBrand(brand);
    systemConfiguration.setName(configName);
    systemConfiguration.setProperties(
        Collections.singletonList(
            SystemConfigProperty.builder()
                .name("property")
                .type(SVG.getName())
                .structureValue("noValue")
                .build()));
    doReturn(Optional.of(systemConfiguration))
        .when(configurationRepository)
        .findOneByBrandAndName(systemConfiguration.getBrand(), systemConfiguration.getName());
    doReturn(Collections.singletonList(systemConfiguration))
        .when(configurationRepository)
        .findByBrand(anyString());
    doAnswer(returnsFirstArg()).when(configurationRepository).save(any(SystemConfiguration.class));
  }

  @Test
  public void testUploadImage() {

    Optional<String> uploadedImage =
        structureService.uploadImage(brand, configName, "property", file);

    assertTrue(uploadedImage.isPresent());

    String uploadedPath = Paths.get(imageStructurePath, "fileName").toString();
    assertEquals(uploadedPath, uploadedImage.get());
    verify(configurationRepository).save(systemConfiguration);
  }

  @Test
  public void testUploadSvgImage() {
    Svg svg = new Svg();
    when(svgImageParser.parse(file)).thenReturn(Optional.of(svg));
    Optional<String> uploadedImage = structureService.uploadSvg("bma", "element", "property", file);

    String uploadedPath = Paths.get(imageStructurePath, "fileName").toString();
    assertEquals(
        uploadedPath,
        uploadedImage.orElseThrow(() -> new IllegalArgumentException("should be present")));

    verify(configurationRepository).save(systemConfiguration);
  }

  @Test
  public void testFindAllStructures() {
    when(configurationRepository.findAll())
        .thenReturn(Collections.singletonList(systemConfiguration));

    List<StructureDto> allStructures = structureService.findAllStructures();

    assertEquals(1, allStructures.size());
    assertEquals(systemConfiguration.getBrand(), allStructures.get(0).getBrand());
    assertTrue(allStructures.get(0).getStructure().containsKey(systemConfiguration.getName()));
  }

  @Test
  public void testFindStructureByBrand() {
    Optional<StructureDto> structure =
        structureService.findStructureByBrand(systemConfiguration.getBrand());

    assertTrue(structure.isPresent());
    assertEquals(systemConfiguration.getBrand(), structure.get().getBrand());
    assertTrue(structure.get().getStructure().containsKey(systemConfiguration.getName()));
  }

  @Test
  public void testFindStructureByBrandEmpty() {
    doReturn(Collections.emptyList()).when(configurationRepository).findByBrand(anyString());

    Optional<StructureDto> structure =
        structureService.findStructureByBrand(systemConfiguration.getBrand());

    assertFalse(structure.isPresent());
  }

  @Test
  public void testFindInitialDataStructure() {
    when(configurationRepository.findAllByBrandAndIsInitialDataConfigIsTrue(anyString()))
        .thenReturn(Collections.singletonList(systemConfiguration));

    Optional<StructureDto> structure =
        structureService.findInitialDataStructure(systemConfiguration.getBrand());

    assertTrue(structure.isPresent());
    assertEquals(systemConfiguration.getBrand(), structure.get().getBrand());
    assertTrue(structure.get().getStructure().containsKey(systemConfiguration.getName()));
  }

  @Test
  public void testFindByBrandAndConfigName() {
    when(configurationRepository.findOneByBrandAndName(brand, configName))
        .thenReturn(Optional.of(systemConfiguration));

    Optional<Map<String, Object>> structure =
        structureService.findByBrandAndConfigName(brand, configName);

    assertTrue(structure.isPresent());
    assertEquals(1, structure.get().size());
  }

  @Test
  public void testFailedToFindByBrandAndConfigName() {
    when(configurationRepository.findOneByBrandAndName(brand, "Config"))
        .thenReturn(Optional.empty());

    Optional<Map<String, Object>> structure =
        structureService.findByBrandAndConfigName(brand, "Config");

    assertFalse(structure.isPresent());
  }

  @Test
  public void testUpdateStructure() {

    StructureDto dto = createStructureDto(systemConfiguration);
    dto.getStructure()
        .replaceAll(
            (k, v) -> {
              v.replaceAll((k1, v1) -> "NewPropValue");
              return v;
            });

    StructureDto updated = structureService.updateStructure(brand, dto);

    verify(configurationRepository).saveAll(anyList());
    assertEquals(dto.getBrand(), updated.getBrand());
    assertEquals(1, updated.getStructure().size());
    assertTrue(updated.getStructure().containsKey(systemConfiguration.getName()));
    assertTrue(
        updated.getStructure().get(systemConfiguration.getName()).containsValue("NewPropValue"));
  }

  @Test(expected = NotFoundException.class)
  public void testUpdateStructureNotFound() {
    doReturn(Collections.emptyList()).when(configurationRepository).findByBrand(anyString());

    StructureDto dto = createStructureDto(systemConfiguration);

    structureService.updateStructure(brand, dto);

    verifyNoMoreInteractions(configurationRepository);
  }

  @Test
  public void testUpdateStructureItemNoItemFound() {
    when(configurationRepository.findOneByBrandAndName(anyString(), anyString()))
        .thenReturn(Optional.empty());
    Optional<StructureDto> structureDto =
        structureService.updateStructureItem(
            "bna", "C onfib", Collections.singletonMap("PropKey", "Value"));

    assertFalse(structureDto.isPresent());
  }

  @Test
  public void testUpdateStructureItemNotUpdated() {
    String configName = "C onfib";
    when(configurationRepository.findOneByBrandAndName(anyString(), anyString()))
        .thenReturn(Optional.of(systemConfiguration));
    Optional<StructureDto> structureDto =
        structureService.updateStructureItem(
            "bna", configName, Collections.singletonMap("PropKey", "Value"));

    assertTrue(structureDto.isPresent());
    assertFalse(structureDto.get().getStructure().containsKey(configName));
  }

  @Test
  public void testUpdateStructureItemNoProperties() {
    Optional<StructureDto> structureDto =
        structureService.updateStructureItem(
            brand, configName, Collections.singletonMap("PropKey", "Value"));

    assertTrue(structureDto.isPresent());
    assertTrue(structureDto.get().getStructure().containsKey(configName));
    assertFalse(structureDto.get().getStructure().get(configName).containsKey("PropKey"));
  }

  @Test
  public void testUpdateStructureItemNotChanged() {
    Object oldStructureValue =
        systemConfiguration
            .getProperty("property")
            .orElseThrow(() -> new IllegalArgumentException("wrong property name in test"))
            .getStructureValue();
    Optional<StructureDto> structureDto =
        structureService.updateStructureItem(
            brand, configName, Collections.singletonMap("property", oldStructureValue));

    assertTrue(structureDto.isPresent());
    assertTrue(structureDto.get().getStructure().containsKey(configName));
    assertTrue(structureDto.get().getStructure().get(configName).containsKey("property"));
    assertEquals(
        oldStructureValue, structureDto.get().getStructure().get(configName).get("property"));
  }

  @Test
  public void testUpdateStructureItem() {
    Optional<StructureDto> structureDto =
        structureService.updateStructureItem(
            brand, configName, Collections.singletonMap("property", "NewValue"));

    assertTrue(structureDto.isPresent());
    assertTrue(structureDto.get().getStructure().containsKey(configName));
    assertTrue(structureDto.get().getStructure().get(configName).containsKey("property"));
    assertEquals("NewValue", structureDto.get().getStructure().get(configName).get("property"));
  }

  @Test
  public void testResetToDefaultForBrand() {
    structureService.resetToDefaultForBrand(brand);

    verify(configurationRepository).saveAll(anyList());
  }

  @Test
  public void testResetToDefaultItem() {
    when(configurationRepository.findOneByBrandAndName(anyString(), anyString()))
        .thenReturn(Optional.of(systemConfiguration));

    structureService.resetToDefaultItem(brand, configName);
    verify(configurationRepository).save(any(SystemConfiguration.class));
  }

  private StructureDto createStructureDto(SystemConfiguration systemConfiguration) {
    StructureDto structureDto = new StructureDto();
    structureDto.setBrand(systemConfiguration.getBrand());
    structureDto.setStructure(
        new HashMap<>(
            Collections.singletonMap(
                systemConfiguration.getName(),
                systemConfiguration.getProperties().stream()
                    .collect(
                        Collectors.toMap(
                            SystemConfigProperty::getName,
                            SystemConfigProperty::getStructureValueOrDefault)))));
    return structureDto;
  }

  @Test
  public void removeImage() {
    doReturn(Boolean.TRUE).when(imageService).removeImage(eq(brand), anyString());

    structureService.removeImage(brand, configName, "property");

    verify(imageService).removeImage(eq(brand), anyString());
    verify(configurationRepository).save(any(SystemConfiguration.class));
  }

  @Test(expected = IllegalArgumentException.class)
  public void removeImageFailedOnDefault() {
    SystemConfigProperty property =
        systemConfiguration
            .getProperty("property")
            .orElseThrow(() -> new RuntimeException("Illegal test data"));
    String defaultImagePath = "/path/defaultImage";
    property.setValue(defaultImagePath);
    property.setStructureValue(defaultImagePath);

    structureService.removeImage(brand, configName, "property");

    verifyNoMoreInteractions(imageService);
    verifyNoMoreInteractions(configurationRepository);
  }

  @Test
  public void removeImageNoPath() {
    SystemConfigProperty property =
        systemConfiguration
            .getProperty("property")
            .orElseThrow(() -> new RuntimeException("Illegal test data"));
    property.setStructureValue(new Svg());

    structureService.removeImage(brand, configName, "property");

    verifyNoMoreInteractions(imageService);
    verify(configurationRepository).save(any(SystemConfiguration.class));
  }
}
