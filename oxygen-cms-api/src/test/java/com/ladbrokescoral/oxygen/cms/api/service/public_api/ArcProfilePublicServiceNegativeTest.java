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
import com.ladbrokescoral.oxygen.cms.api.service.ArcMasterService;
import com.ladbrokescoral.oxygen.cms.api.service.ArcProfileService;
import java.io.IOException;
import java.util.List;
import java.util.stream.Collectors;
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
public class ArcProfilePublicServiceNegativeTest {

  List<ArcProfile> arcProfiles;

  List<ArcProfileDto> arcProfileDtos;

  @Mock private ArcProfileService arcProfileService;
  @Mock private ModelMapper modelMapper;
  @Mock private ArcMasterService masterService;
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
    arcMasterDataWithEmptyData =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/private_api/arcMasterData.json"),
            new TypeReference<List<ArcMasterData>>() {});
    arcMasterDataWithEmptyData =
        arcMasterDataWithEmptyData.stream()
            .filter(d -> "a".equals(d.getMasterLineName()))
            .collect(Collectors.toList());
    when(masterService.getAllMetadata()).thenReturn(arcMasterDataWithEmptyData);
    when(modelMapper.map(any(), any())).thenReturn(arcProfileDtos.get(0));
    this.arcProfilePublicService.findAll();
  }

  @Test
  public void testToFindArcProfileByBrandAndModelRiskLevelAndReasonCodeWithEmpty()
      throws IOException {
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
    Assert.assertEquals("", arcProfileResponse.getModelRiskLevel());
    Assert.assertEquals("", arcProfileResponse.getReasonCode());
  }
}
