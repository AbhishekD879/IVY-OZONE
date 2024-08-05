package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.ArcProfileDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ArcMasterData;
import com.ladbrokescoral.oxygen.cms.api.entity.ArcProfile;
import com.ladbrokescoral.oxygen.cms.api.exception.NotFoundException;
import com.ladbrokescoral.oxygen.cms.api.service.ArcMasterService;
import com.ladbrokescoral.oxygen.cms.api.service.ArcProfileService;
import java.io.IOException;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.MockitoAnnotations;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;

@RunWith(MockitoJUnitRunner.class)
public class ArcProfilePublicServiceTest {

  List<ArcProfile> arcProfiles;

  List<ArcProfileDto> arcProfileDtos;

  @Mock private ArcProfileService arcProfileService;
  @Mock private ModelMapper modelMapper;
  @Mock private ArcMasterService masterService;
  private List<ArcMasterData> arcMasterData;
  private List<ArcMasterData> arcMasterDataWithEmptyData;

  @InjectMocks private ArcProfilePublicService arcProfilePublicService;

  @Before
  public void init() throws IOException {
    MockitoAnnotations.openMocks(this);
    final ObjectMapper jsonMapper = new ObjectMapper();
    jsonMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);
    jsonMapper.registerModule(new JavaTimeModule());
    arcProfiles =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/private_api/arcProfiles.json"),
            new TypeReference<List<ArcProfile>>() {});
    arcProfileDtos =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream(
                "controller/public_api/arcProfilesDtoWithoutReasonCodesAndRiskLevel.json"),
            new TypeReference<List<ArcProfileDto>>() {});
    arcMasterData =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/private_api/arcMasterData.json"),
            new TypeReference<List<ArcMasterData>>() {});
    arcMasterDataWithEmptyData =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/private_api/arcMasterData.json"),
            new TypeReference<List<ArcMasterData>>() {});
    when(masterService.getAllMetadata()).thenReturn(arcMasterData);
    when(modelMapper.map(any(), any())).thenReturn(arcProfileDtos.get(0));
    this.arcProfilePublicService.findAll();
  }

  @Test
  public void testToFindArcProfileByBrandAndModelRiskLevelAndReasonCode() throws IOException {
    ArcProfile arcProfile =
        TestUtil.deserializeWithJackson("controller/private_api/arcProfile.json", ArcProfile.class);
    when(arcProfileService.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
            anyString(), anyInt(), anyInt()))
        .thenReturn(arcProfile);
    ArcProfileDto arcProfileResponse =
        arcProfilePublicService.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
            "ladbrokes", 2, 1);
    verify(arcProfileService, times(1))
        .findArcProfileByBrandAndModelRiskLevelAndReasonCode("ladbrokes", 2, 1);
    Assert.assertNotNull(arcProfileResponse);
    Assert.assertEquals("2-Problem Gambler Low", arcProfileResponse.getModelRiskLevel());
    Assert.assertEquals("1-Difference in spend from norm", arcProfileResponse.getReasonCode());
  }

  @Test(expected = NotFoundException.class)
  public void testToFindArcProfileByBrandAndModelRiskLevelAndReasonCodeNotFound()
      throws IOException {
    when(arcProfileService.findArcProfileByBrandAndModelRiskLevelAndReasonCode(
            anyString(), anyInt(), anyInt()))
        .thenReturn(null);
    arcProfilePublicService.findArcProfileByBrandAndModelRiskLevelAndReasonCode("ladbrokes", 2, 1);
  }

  @Test
  public void testToFindByBrand() throws IOException {
    List<ArcProfile> arcProfiles =
        TestUtil.deserializeWithJacksonToType(
            "controller/private_api/arcProfiles.json", new TypeReference<List<ArcProfile>>() {});
    when(arcProfileService.findAllByBrand(anyString())).thenReturn(Optional.of(arcProfiles));
    List<ArcProfileDto> arcProfileResponse = arcProfilePublicService.findByBrand("ladbrokes");
    verify(arcProfileService, times(1)).findAllByBrand("ladbrokes");
    Assert.assertNotNull(arcProfileResponse);
    Assert.assertEquals("2-Problem Gambler Low", arcProfileResponse.get(0).getModelRiskLevel());
    Assert.assertEquals(
        "1-Difference in spend from norm", arcProfileResponse.get(0).getReasonCode());
  }

  @Test(expected = NotFoundException.class)
  public void testToFindByBrandNotFoundException() {
    when(arcProfileService.findAllByBrand(anyString())).thenReturn(Optional.empty());
    arcProfilePublicService.findByBrand("ladbrokes");
  }

  @Test
  public void testToFindById() throws IOException {
    ArcProfile arcProfile =
        TestUtil.deserializeWithJackson("controller/private_api/arcProfile.json", ArcProfile.class);
    when(arcProfileService.findOne(anyString())).thenReturn(Optional.of(arcProfile));
    ArcProfileDto arcProfileResponse = arcProfilePublicService.findById("60d5b612b5a7cc45b8e4822f");
    verify(arcProfileService, times(1)).findOne("60d5b612b5a7cc45b8e4822f");
    Assert.assertNotNull(arcProfileResponse);
    Assert.assertEquals("2-Problem Gambler Low", arcProfileResponse.getModelRiskLevel());
    Assert.assertEquals("1-Difference in spend from norm", arcProfileResponse.getReasonCode());
  }

  @Test(expected = NotFoundException.class)
  public void testToFindByIdNotFoundException() {
    when(arcProfileService.findOne(anyString())).thenReturn(Optional.empty());
    arcProfilePublicService.findById("60d5b612b5a7cc45b8e4822e");
  }
}
