package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.dto.AliasModuleNamesDto;
import com.ladbrokescoral.oxygen.cms.api.dto.AutomaticUpdateDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYModuleEntity;
import java.util.Collections;
import org.junit.jupiter.api.Assertions;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.AdditionalAnswers;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.test.util.ReflectionTestUtils;

@ExtendWith(MockitoExtension.class)
class AutomaticUpdateServiceTest {
  @Mock RGYModuleService rgyModuleService;

  @Mock RGYConfigUploadService rgyConfigUploadService;

  AutomaticUpdateService automaticUpdateService;

  RGYModuleEntity rgyModuleEntity;

  @BeforeEach
  public void init() {
    rgyModuleEntity = createRgyModuleEntity();
    automaticUpdateService = new AutomaticUpdateService(rgyModuleService, rgyConfigUploadService);
  }

  @Test
  void testUpdateRgyModuleAliasNames() {
    Mockito.when(this.rgyModuleService.readByBrand(Mockito.anyString()))
        .thenReturn(Collections.singletonList(rgyModuleEntity));
    Mockito.when(this.rgyModuleService.save(Mockito.any(RGYModuleEntity.class)))
        .thenAnswer(AdditionalAnswers.returnsFirstArg());
    Mockito.when(this.rgyConfigUploadService.uploadToS3(Mockito.anyString()))
        .thenReturn(Collections.emptyList());
    AutomaticUpdateDto updateDto = createUpdateDto("test1", "11");

    this.automaticUpdateService.doUpdate(updateDto);
    Mockito.verify(rgyModuleService, Mockito.times(1)).readByBrand(Mockito.anyString());
    Mockito.verify(rgyModuleService, Mockito.times(1)).save(Mockito.any(RGYModuleEntity.class));
    Mockito.verify(rgyConfigUploadService, Mockito.times(1)).uploadToS3(Mockito.anyString());
  }

  @Test
  void testUpdateRgyModuleWithNoMatch() {
    Mockito.when(this.rgyModuleService.readByBrand(Mockito.anyString()))
        .thenReturn(Collections.singletonList(rgyModuleEntity));
    AutomaticUpdateDto updateDto = createUpdateDto("test", "22");
    this.automaticUpdateService.doUpdate(updateDto);
    Mockito.verify(rgyModuleService, Mockito.times(1)).readByBrand(Mockito.anyString());
    Mockito.verify(rgyModuleService, Mockito.times(0)).save(Mockito.any(RGYModuleEntity.class));
    Mockito.verify(rgyConfigUploadService, Mockito.times(0)).uploadToS3(Mockito.anyString());
  }

  @Test
  void testUpdateRgyModuleWithNoIdMatch() {
    AutomaticUpdateDto updateDto = createUpdateDto("test", "44");
    RGYModuleEntity module =
        ReflectionTestUtils.invokeMethod(
            automaticUpdateService, "updateAliasModulesNames", createRgyModuleEntity(), updateDto);
    assert module != null;
    Assertions.assertEquals(1, module.getAliasModules().size());
  }

  private RGYModuleEntity createRgyModuleEntity() {
    RGYModuleEntity rgyModuleEntity = new RGYModuleEntity();
    rgyModuleEntity.setAliasModules(Collections.singletonList(aliasModuleNamesDto("11", "sample")));
    rgyModuleEntity.setBrand("bma");
    return rgyModuleEntity;
  }

  private AutomaticUpdateDto createUpdateDto(String updatedTitle, String id) {
    AutomaticUpdateDto automaticUpdateDto = new AutomaticUpdateDto();
    automaticUpdateDto.setId(id);
    automaticUpdateDto.setUpdatedTitle(updatedTitle);
    automaticUpdateDto.setBrand("bma");
    return automaticUpdateDto;
  }

  private AliasModuleNamesDto aliasModuleNamesDto(String id, String title) {
    AliasModuleNamesDto aliasModuleNamesDto = new AliasModuleNamesDto();
    aliasModuleNamesDto.setId(id);
    aliasModuleNamesDto.setTitle(title);
    return aliasModuleNamesDto;
  }
}
