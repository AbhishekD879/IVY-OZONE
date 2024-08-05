package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.controller.dto.RGYModule;
import com.ladbrokescoral.oxygen.cms.api.dto.AliasModuleNamesDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYModuleEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.RGYModuleRepository;
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
@SpringBootTest(classes = {RGYModuleService.class})
class RGYModuleServiceTest {
  @MockBean private RGYModuleRepository rgyModuleRepository;
  @InjectMocks private RGYModuleService rgyModuleService;

  @BeforeEach
  public void setup() throws IOException, URISyntaxException {
    MockitoAnnotations.openMocks(this);
  }

  @Test
  void testReadByBrand() {
    List<RGYModuleEntity> entities = new ArrayList<>();

    RGYModuleEntity rgyModuleEntity = getEntity();

    List<String> subModuleIds = new ArrayList<>();
    subModuleIds.add("d12313sd");
    rgyModuleEntity.setSubModuleIds(subModuleIds);
    entities.add(rgyModuleEntity);
    when(rgyModuleRepository.findByBrand(Mockito.any())).thenReturn(entities);
    List<RGYModuleEntity> rgYellowConfigEntities = rgyModuleService.readByBrand(Mockito.any());
    assertEquals(1, rgYellowConfigEntities.size());
  }

  @Test
  void testReadByBrandSubModuelsDisabled() {
    List<RGYModuleEntity> entities = new ArrayList<>();
    RGYModuleEntity rgyModuleEntity = getEntity();
    rgyModuleEntity.setSubModuleEnabled(false);
    entities.add(rgyModuleEntity);
    when(rgyModuleRepository.findByBrand(Mockito.any())).thenReturn(entities);
    List<RGYModuleEntity> rgYellowConfigEntities = rgyModuleService.readByBrand(Mockito.any());
    assertEquals(1, rgYellowConfigEntities.size());
  }

  @Test
  void testReadByBrandSubModuelseEmpty() {
    List<RGYModuleEntity> entities = new ArrayList<>();
    RGYModuleEntity rgyModuleEntity = getEntity();
    List<String> subModuleIds = new ArrayList<>();
    rgyModuleEntity.setSubModuleIds(subModuleIds);
    entities.add(rgyModuleEntity);
    when(rgyModuleRepository.findByBrand(Mockito.any())).thenReturn(entities);
    List<RGYModuleEntity> rgYellowConfigEntities = rgyModuleService.readByBrand(Mockito.any());
    assertEquals(1, rgYellowConfigEntities.size());
  }

  @Test
  void testReadByBrand_empty() {
    List<RGYModuleEntity> entities = new ArrayList<>();
    when(rgyModuleRepository.findByBrand(Mockito.any())).thenReturn(entities);
    List<RGYModuleEntity> rgYellowConfigEntities = rgyModuleService.readByBrand(Mockito.any());
    assertEquals(0, rgYellowConfigEntities.size());
  }

  @Test
  void testDeleteById() {
    RGYModuleEntity rgyModuleEntity = getEntity();
    when(rgyModuleRepository.findById(Mockito.any())).thenReturn(Optional.of(rgyModuleEntity));
    ResponseEntity<RGYModuleEntity> rgyModuleEntityResponse =
        rgyModuleService.deleteById(Mockito.any());
    assertEquals(HttpStatus.NO_CONTENT, rgyModuleEntityResponse.getStatusCode());
  }

  @Test
  void testDeleteByIdEmpty() {
    when(rgyModuleRepository.findById(Mockito.any())).thenReturn(Optional.empty());
    ResponseEntity<RGYModuleEntity> rgyModuleEntityResponse =
        rgyModuleService.deleteById(Mockito.any());
    assertEquals(HttpStatus.NOT_FOUND, rgyModuleEntityResponse.getStatusCode());
  }

  @Test
  void testFindByModuleIdSubModuleEnabledTrue() {
    RGYModuleEntity rgyModuleEntity = getEntity();
    List<String> subModuleIds = new ArrayList<>();
    subModuleIds.add("d12313sd");
    rgyModuleEntity.setSubModuleIds(subModuleIds);
    rgyModuleEntity.setSubModuleEnabled(true);
    when(rgyModuleRepository.findById(Mockito.any())).thenReturn(Optional.of(rgyModuleEntity));
    RGYModule rgyModuleResponse = rgyModuleService.findByModuleId(Mockito.any());
    assertNotNull(rgyModuleResponse);
  }

  @Test
  void testFindByModuleIdSubModuleEnabledTrueAndSubModulesEmpty() {
    RGYModuleEntity rgyModuleEntity = getEntity();
    List<String> subModuleIds = new ArrayList<>();
    rgyModuleEntity.setSubModuleIds(subModuleIds);
    when(rgyModuleRepository.findById(Mockito.any())).thenReturn(Optional.of(rgyModuleEntity));
    RGYModule rgyModuleResponse = rgyModuleService.findByModuleId(Mockito.any());
    assertNotNull(rgyModuleResponse);
  }

  @Test
  void testFindByIdSubModuleEnabledFalse() {
    RGYModuleEntity rgyModuleEntity = getEntity();
    rgyModuleEntity.setSubModuleEnabled(false);
    when(rgyModuleRepository.findById(Mockito.any())).thenReturn(Optional.of(rgyModuleEntity));
    RGYModule rgyModuleResponse = rgyModuleService.findByModuleId(Mockito.any());
    assertNotNull(rgyModuleResponse);
  }

  @Test
  void testFindByIdSubModuleEnabledFalseEmpty() {
    when(rgyModuleRepository.findById(Mockito.any())).thenReturn(Optional.empty());
    RGYModule rgyModuleResponse = rgyModuleService.findByModuleId(Mockito.any());
    assertNull(rgyModuleResponse);
  }

  @Test
  void testGetRGYModuleInfoWithSubModules() {
    RGYModuleEntity rgyModuleEntity = getEntity();
    when(rgyModuleRepository.findById(Mockito.any())).thenReturn(Optional.of(rgyModuleEntity));
    RGYModuleEntity rgyModuleResponse =
        rgyModuleService.getRGYModuleInfoWithSubModules(rgyModuleEntity);
    assertNotNull(rgyModuleResponse);
  }

  @Test
  void testGetRGYModuleInfoWithSubModulesIdEmpty() {
    RGYModuleEntity rgyModuleEntity = getEntity();
    rgyModuleEntity.setId("");
    when(rgyModuleRepository.findById(Mockito.any())).thenReturn(Optional.empty());
    RGYModuleEntity rgyModuleResponse =
        rgyModuleService.getRGYModuleInfoWithSubModules(rgyModuleEntity);
    assertNotNull(rgyModuleResponse);
  }

  @Test
  void testGetSubModuleInfo() {
    RGYModuleEntity rgyModuleEntity = getEntity();
    rgyModuleEntity.setId("121212");
    RGYModule rgyModule = new RGYModule();
    List<RGYModule> subModules = new ArrayList<>();
    rgyModule.setSubModules(subModules);
    rgyModule.setId("121212");
    when(rgyModuleRepository.findById(Mockito.any())).thenReturn(Optional.of(rgyModuleEntity));
    RGYModule rgyModuleResponse = rgyModuleService.getSubModuleInfo("fiveaside211212", rgyModule);
    assertNotNull(rgyModuleResponse);
  }

  @Test
  void testGetSubModuleInfoEmpty() {
    RGYModuleEntity rgyModuleEntity = getEntity();
    rgyModuleEntity.setId("");
    when(rgyModuleRepository.findById(Mockito.any())).thenReturn(Optional.empty());
    RGYModule rgyModuleResponse =
        rgyModuleService.getSubModuleInfo("fiveaside211212", Mockito.any());
    assertNull(rgyModuleResponse);
  }

  @Test
  void testMapSubModulesInfoEmpty() {
    RGYModuleEntity rgyModuleEntity = getEntity();
    List<String> subModuleIds = new ArrayList<>();
    subModuleIds.add("12121");
    rgyModuleEntity.setSubModuleIds(subModuleIds);
    when(rgyModuleRepository.findById(Mockito.any())).thenReturn(Optional.empty());
    RGYModuleEntity rgyModuleEntityRes = rgyModuleService.mapSubModulesInfo(rgyModuleEntity);
    assertEquals(0, rgyModuleEntityRes.getSubModules().size());
  }

  @Test
  void testMapSubModulesInfo() {
    RGYModuleEntity rgyModuleEntity = getEntity();
    List<String> subModuleIds = new ArrayList<>();
    subModuleIds.add("12121");
    rgyModuleEntity.setSubModuleIds(subModuleIds);
    when(rgyModuleRepository.findById(Mockito.any())).thenReturn(Optional.of(rgyModuleEntity));
    RGYModuleEntity rgyModuleEntityRes = rgyModuleService.mapSubModulesInfo(rgyModuleEntity);
    assertEquals(1, rgyModuleEntityRes.getSubModules().size());
  }

  private RGYModuleEntity getEntity() {
    RGYModuleEntity rgyModuleEntity = new RGYModuleEntity();
    rgyModuleEntity.setBrand("ladbrokes");
    rgyModuleEntity.setId("fiveaside211212");
    rgyModuleEntity.setModuleName("FiveASide");
    rgyModuleEntity.setAliasModules(
        Collections.singletonList(aliasModuleNamesDto("FIVEASIDE", "11")));
    rgyModuleEntity.setSubModuleEnabled(true);
    return rgyModuleEntity;
  }

  private AliasModuleNamesDto aliasModuleNamesDto(String title, String id) {
    AliasModuleNamesDto aliasModuleNamesDto = new AliasModuleNamesDto();
    aliasModuleNamesDto.setId(id);
    aliasModuleNamesDto.setTitle(title);
    return aliasModuleNamesDto;
  }
}
