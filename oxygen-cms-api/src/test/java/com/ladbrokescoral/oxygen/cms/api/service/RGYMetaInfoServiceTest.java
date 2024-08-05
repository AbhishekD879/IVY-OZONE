package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertNotNull;
import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.entity.RGYMetaInfoEntity;
import com.ladbrokescoral.oxygen.cms.api.repository.RGYMetaInfoRepository;
import java.io.IOException;
import java.net.URISyntaxException;
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
@SpringBootTest(classes = {RGYMetaInfoService.class})
class RGYMetaInfoServiceTest {

  @MockBean private RGYMetaInfoRepository rgyMetaInfoRepository;
  @InjectMocks private RGYMetaInfoService rgyMetaInfoService;

  @BeforeEach
  public void setup() throws IOException, URISyntaxException {
    MockitoAnnotations.openMocks(this);
  }

  @Test
  void testGetRgyMetaInfo() {
    when(rgyMetaInfoRepository.findOneByBrand(Mockito.any()))
        .thenReturn(Optional.of(getMetaInfo()));
    ResponseEntity<RGYMetaInfoEntity> rgYellowConfigEntities =
        rgyMetaInfoService.getRgyMetaInfo(Mockito.any());
    assertEquals(HttpStatus.OK, rgYellowConfigEntities.getStatusCode());
    assertNotNull(rgYellowConfigEntities.getBody());
  }

  @Test
  void testGetRgyMetaInfo_BrandEmpty() {
    when(rgyMetaInfoRepository.findOneByBrand(Mockito.any())).thenReturn(Optional.empty());
    ResponseEntity<RGYMetaInfoEntity> rgYellowConfigEntities =
        rgyMetaInfoService.getRgyMetaInfo(Mockito.any());
    assertEquals(HttpStatus.OK, rgYellowConfigEntities.getStatusCode());
    assertNotNull(rgYellowConfigEntities.getBody());
  }

  @Test
  void testUdateRgyFlag() {
    when(rgyMetaInfoRepository.findOneByBrand(Mockito.any()))
        .thenReturn(Optional.of(getMetaInfo()));
    ResponseEntity<RGYMetaInfoEntity> rgYellowConfigEntities =
        rgyMetaInfoService.updateRgyFlag(Mockito.any(), true);
    assertEquals(HttpStatus.OK, rgYellowConfigEntities.getStatusCode());
    assertNotNull(rgYellowConfigEntities.getBody());
  }

  @Test
  void testUdateRgyFlag_BrandEmpty() {
    when(rgyMetaInfoRepository.findOneByBrand(Mockito.any())).thenReturn(Optional.empty());
    ResponseEntity<RGYMetaInfoEntity> rgYellowConfigEntities =
        rgyMetaInfoService.updateRgyFlag(Mockito.any(), true);
    assertEquals(HttpStatus.NOT_FOUND, rgYellowConfigEntities.getStatusCode());
  }

  private RGYMetaInfoEntity getMetaInfo() {
    RGYMetaInfoEntity rgyMetaInfoEntity = new RGYMetaInfoEntity();
    rgyMetaInfoEntity.setBrand("ladbrokes");
    return rgyMetaInfoEntity;
  }
}
