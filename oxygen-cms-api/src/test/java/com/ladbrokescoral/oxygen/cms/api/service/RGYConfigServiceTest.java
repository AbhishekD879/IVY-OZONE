package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.RGYModule;
import com.ladbrokescoral.oxygen.cms.api.dto.AliasModuleNamesDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYConfigurationEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.RGYConfigRepository;
import java.io.IOException;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = {RGYConfigService.class})
class RGYConfigServiceTest {

  @MockBean private RGYConfigRepository rgyConfigRepository;

  @MockBean private RGYModuleService rgyModuleService;

  @InjectMocks private RGYConfigService rgyConfigService;

  @BeforeEach
  public void setup() throws IOException, URISyntaxException {
    MockitoAnnotations.openMocks(this);
  }

  @Test
  void testReadByBrand() {
    List<RGYConfigurationEntity> rgyConfigurationEntities = new ArrayList<>();
    rgyConfigurationEntities.add(getRGYConfigurationEntity());
    when(rgyConfigRepository.findByBrand(Mockito.any())).thenReturn(rgyConfigurationEntities);
    when(rgyModuleService.findByModuleId("fiveaside211212")).thenReturn(getRGYModule());
    List<RGYConfigurationEntity> rgYellowConfigEntities =
        rgyConfigService.readByBrand(Mockito.any());
    assertEquals(1, rgYellowConfigEntities.size());
  }

  @Test
  void testReadByBrandModuleEmpty() {
    RGYConfigurationEntity rgyConfigurationEntity = getRGYConfigurationEntity();
    rgyConfigurationEntity.setBonusSuppression(false);
    List<RGYConfigurationEntity> rgyConfigurationEntities = new ArrayList<>();
    rgyConfigurationEntities.add(rgyConfigurationEntity);
    when(rgyConfigRepository.findByBrand(Mockito.any())).thenReturn(rgyConfigurationEntities);
    when(rgyModuleService.findByModuleId("fiveaside211212")).thenReturn(null);
    List<RGYConfigurationEntity> rgYellowConfigEntities =
        rgyConfigService.readByBrand(Mockito.any());
    assertEquals(1, rgYellowConfigEntities.size());
    assertEquals(0, rgYellowConfigEntities.get(0).getModules().size());
  }

  @Test
  void testReadByBrand_empty() {
    when(rgyConfigRepository.findByBrand(Mockito.any())).thenReturn(Collections.emptyList());
    List<RGYConfigurationEntity> rgYellowConfigEntities =
        rgyConfigService.readByBrand(Mockito.any());
    assertEquals(0, rgYellowConfigEntities.size());
  }

  @Test
  void testGetById() {
    when(rgyConfigRepository.findById(Mockito.any()))
        .thenReturn(Optional.of(getRGYConfigurationEntity()));
    when(rgyModuleService.findByModuleId("fiveaside211212")).thenReturn(getRGYModule());
    ResponseEntity<RGYConfigurationEntity> rgYellowConfigEntities =
        rgyConfigService.getById(Mockito.any());
    assertEquals(HttpStatus.OK, rgYellowConfigEntities.getStatusCode());
    assertNotNull(rgYellowConfigEntities.getBody());
    assertNotNull(rgYellowConfigEntities.getBody().getModules());
  }

  @Test
  void testGetById_ModuleEmpty() {
    when(rgyConfigRepository.findById(Mockito.any()))
        .thenReturn(Optional.of(getRGYConfigurationEntity()));
    when(rgyModuleService.findByModuleId("fiveaside211212")).thenReturn(null);
    ResponseEntity<RGYConfigurationEntity> rgYellowConfigEntities =
        rgyConfigService.getById(Mockito.any());
    assertEquals(HttpStatus.OK, rgYellowConfigEntities.getStatusCode());
    assertNotNull(rgYellowConfigEntities.getBody());
    assertNotNull(rgYellowConfigEntities.getBody().getModules());
  }

  @Test
  void testGetByIdEmpty() {
    when(rgyConfigRepository.findById(Mockito.any())).thenReturn(Optional.empty());
    ResponseEntity<RGYConfigurationEntity> rgYellowConfigEntities =
        rgyConfigService.getById(Mockito.any());
    assertEquals(HttpStatus.NOT_FOUND, rgYellowConfigEntities.getStatusCode());
  }

  @Test
  void testFindByBrandAndReasonCodeAndRiskLevelCode() {
    when(rgyConfigRepository.findByBrandAndReasonCodeAndRiskLevelCode("ladbrokes", 3, 4))
        .thenReturn(getRGYConfigurationEntity());
    RGYConfigurationEntity rgyConfigurationEntity =
        rgyConfigService.findByBrandAndReasonCodeAndRiskLevelCode("ladbrokes", 3, 4);
    assertNotNull(rgyConfigurationEntity);
  }

  @Test
  void testFindByBrandAndReasonCodeAndRiskLevelCodeEmpty() {
    when(rgyConfigRepository.findByBrandAndReasonCodeAndRiskLevelCode("ladbrokes", 3, 4))
        .thenReturn(null);
    RGYConfigurationEntity rgyConfigurationEntity =
        rgyConfigService.findByBrandAndReasonCodeAndRiskLevelCode("ladbrokes", 4, 5);
    assertNull(rgyConfigurationEntity);
  }

  @Test
  void testGetAndMapRGYModulesIdsEmpty() {
    RGYConfigurationEntity rgyConfigurationEntity = getRGYConfigurationEntity();
    rgyConfigurationEntity.setModuleIds(Collections.emptyList());
    rgyConfigService.getAndMapRGYModules(rgyConfigurationEntity);
    assertEquals(0, rgyConfigurationEntity.getModules().size());
  }

  @Test
  void testReadByBrandAndBonusSuppressionTrue() {
    List<RGYConfigurationEntity> rgyConfigurationEntities = new ArrayList<>();
    rgyConfigurationEntities.add(getRGYConfigurationEntity());
    when(rgyConfigRepository.findByBrandAndBonusSuppressionTrue(Mockito.any()))
        .thenReturn(rgyConfigurationEntities);
    when(rgyModuleService.findByModuleId("fiveaside211212")).thenReturn(getRGYModule());
    List<RGYConfigurationEntity> rgYellowConfigEntities =
        rgyConfigService.readByBrandAndBonusSuppressionTrue(Mockito.any());
    assertEquals(1, rgYellowConfigEntities.size());
    assertNotNull(rgYellowConfigEntities);
  }

  @Test
  void testReadByBrandAndBonusSuppressionTrueEmpty() {
    when(rgyConfigRepository.findByBrandAndBonusSuppressionTrue("ladbrokes")).thenReturn(null);
    List<RGYConfigurationEntity> rgYellowConfigEntities =
        rgyConfigService.readByBrandAndBonusSuppressionTrue("ladbrokes");
    assertNull(rgYellowConfigEntities);
  }

  private RGYConfigurationEntity getRGYConfigurationEntity() {
    RGYConfigurationEntity rgyConfigurationEntity = new RGYConfigurationEntity();
    rgyConfigurationEntity.setId("abcd1234");
    rgyConfigurationEntity.setBrand("ladbrokes");
    rgyConfigurationEntity.setBonusSuppression(true);
    rgyConfigurationEntity.setReasonDesc("");
    rgyConfigurationEntity.setReasonCode(3);
    rgyConfigurationEntity.setRiskLevelCode(4);
    rgyConfigurationEntity.setRiskLevelDesc("");
    List<String> moduleIds = new ArrayList<>();
    moduleIds.add("fiveaside211212");
    rgyConfigurationEntity.setModuleIds(moduleIds);
    return rgyConfigurationEntity;
  }

  private RGYModule getRGYModule() {
    RGYModule rgyModule = new RGYModule();
    rgyModule.setBrand("ladbrokes");
    rgyModule.setId("fiveaside211212");
    rgyModule.setModuleName("FiveASide");
    rgyModule.setSubModuleEnabled(true);
    rgyModule.setAliasModules(Collections.singletonList(aliasModuleNamesDto("FIVEASIDE", "11")));
    return rgyModule;
  }

  private AliasModuleNamesDto aliasModuleNamesDto(String title, String id) {
    AliasModuleNamesDto aliasModuleNamesDto = new AliasModuleNamesDto();
    aliasModuleNamesDto.setId(id);
    aliasModuleNamesDto.setTitle(title);
    return aliasModuleNamesDto;
  }
}
