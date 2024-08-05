package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertNotNull;
import static org.junit.Assert.assertNull;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.entity.RGYConfigurationEntity;
import com.ladbrokescoral.oxygen.cms.api.entity.RGYModuleEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.BrandRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.RGYConfigRepository;
import com.ladbrokescoral.oxygen.cms.api.service.cache.DeliveryNetworkService;
import java.io.IOException;
import java.net.URISyntaxException;
import java.util.ArrayList;
import java.util.List;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mockito;
import org.mockito.MockitoAnnotations;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit.jupiter.SpringExtension;

@ExtendWith(SpringExtension.class)
@SpringBootTest(classes = {RGYConfigUploadService.class})
class RGYConfigUploadServiceTest {

  @MockBean private RGYConfigRepository rgyConfigRepository;
  @MockBean private RGYModuleService rgyModuleService;
  @MockBean private BrandService brandService;
  @MockBean private BrandRepository brandRepository;
  @MockBean private RGYConfigService rgyConfigService;
  @MockBean private DeliveryNetworkService deliveryNetworkService;

  @InjectMocks private RGYConfigUploadService rgyConfigUploadService;

  @BeforeEach
  public void setup() throws IOException, URISyntaxException {
    MockitoAnnotations.openMocks(this);
  }

  @Test
  void testReadByBrandAndBonusSuppressionTrue() {
    List<RGYConfigurationEntity> rgyConfigurationEntities = new ArrayList<>();
    rgyConfigurationEntities.add(getRGYConfigurationEntity());
    when(rgyConfigService.readByBrandAndBonusSuppressionTrue(Mockito.any()))
        .thenReturn(rgyConfigurationEntities);
    when(rgyConfigService.readByBrand(Mockito.any())).thenReturn(rgyConfigurationEntities);

    List<RGYConfigurationEntity> rgYellowConfigEntities =
        rgyConfigUploadService.uploadToS3(Mockito.any());
    assertEquals(1, rgYellowConfigEntities.size());
    assertNotNull(rgYellowConfigEntities);
  }

  @Test
  void testReadByBrandAndBonusSuppressionTrueEmpty() {
    List<RGYModuleEntity> rgyModuleEntities = new ArrayList<>();
    RGYModuleEntity rgyModuleEntity = new RGYModuleEntity();
    List<String> subModuleIds = new ArrayList<>();
    subModuleIds.add("d12313sd");
    rgyModuleEntity.setSubModuleIds(subModuleIds);
    rgyModuleEntities.add(rgyModuleEntity);
    when(rgyConfigService.readByBrandAndBonusSuppressionTrue("ladbrokes")).thenReturn(null);
    when(rgyModuleService.readByBrand(Mockito.any())).thenReturn(rgyModuleEntities);
    List<RGYConfigurationEntity> rgYellowConfigEntities =
        rgyConfigUploadService.uploadToS3("ladbrokes");
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
}
