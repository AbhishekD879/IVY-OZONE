package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.ArgumentMatchers.anyInt;
import static org.mockito.ArgumentMatchers.anyString;
import static org.mockito.Mockito.*;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.ArcProfile;
import com.ladbrokescoral.oxygen.cms.api.repository.ArcProfileRepository;
import java.io.IOException;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class ArcProfileServiceTest {
  @Mock private ArcProfileRepository arcProfileRepository;

  @InjectMocks private ArcProfileService service;

  @Before
  public void init() {
    service = new ArcProfileService(arcProfileRepository);
  }

  @Test
  public void testToFindArcProfileByBrandAndModelRiskLevelAndReasonCode() throws IOException {
    ArcProfile arcProfile =
        TestUtil.deserializeWithJackson("controller/private_api/arcProfile.json", ArcProfile.class);
    when(arcProfileRepository.findByBrandAndModelRiskLevelAndReasonCode(
            anyString(), anyInt(), anyInt()))
        .thenReturn(Optional.of(arcProfile));
    ArcProfile arcProfileResponse =
        service.findArcProfileByBrandAndModelRiskLevelAndReasonCode("ladbrokes", 2, 1);
    verify(arcProfileRepository, times(1))
        .findByBrandAndModelRiskLevelAndReasonCode("ladbrokes", 2, 1);
    Assert.assertNotNull(arcProfileResponse);
  }

  @Test
  public void testToFindAllByBrand() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    jsonMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);
    jsonMapper.registerModule(new JavaTimeModule());
    List<ArcProfile> arcProfiles =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/private_api/arcProfiles.json"),
            new TypeReference<List<ArcProfile>>() {});
    when(arcProfileRepository.findAllByBrand(anyString())).thenReturn(Optional.of(arcProfiles));
    Optional<List<ArcProfile>> arcProfileResponse = service.findAllByBrand("ladbrokes");
    verify(arcProfileRepository, times(1)).findAllByBrand("ladbrokes");
    Assert.assertNotNull(arcProfileResponse.get());
  }

  @Test
  public void testToDeleteArcProfileByBrandAndModelRiskLevelAndReasonCode() {
    when(arcProfileRepository.deleteArcProfileByBrandAndModelRiskLevelAndReasonCode(
            anyString(), anyInt(), anyInt()))
        .thenReturn(1l);
    Long arcProfileResponse =
        service.deleteArcProfileByBrandAndModelRiskLevelAndReasonCode("ladbrokes", 2, 1);
    verify(arcProfileRepository, times(1))
        .deleteArcProfileByBrandAndModelRiskLevelAndReasonCode("ladbrokes", 2, 1);
    Assert.assertNotNull(arcProfileResponse);
  }
}
