package com.ladbrokescoral.oxygen.cms.api.service;

import static org.mockito.Mockito.*;

import com.fasterxml.jackson.core.type.TypeReference;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.SerializationFeature;
import com.fasterxml.jackson.datatype.jsr310.JavaTimeModule;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.ArcMasterData;
import com.ladbrokescoral.oxygen.cms.api.repository.ArcMasterRepository;
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
import org.springframework.http.ResponseEntity;

@RunWith(MockitoJUnitRunner.class)
public class ArcMasterServiceTest {
  @Mock private ArcMasterRepository arcMasterRepository;

  @InjectMocks private ArcMasterService service;

  @Before
  public void init() {
    service = new ArcMasterService(arcMasterRepository);
  }

  @Test
  public void testToGetMasterDataByLineItem() throws IOException {
    final String lineItem = "modelRiskLevel";
    ArcMasterData entity = createArcMasterDataList().get(0);
    when(arcMasterRepository.findByMasterLineName(lineItem)).thenReturn(entity);
    ArcMasterData entityResponse = service.getMasterDataByLineItem(lineItem);
    verify(arcMasterRepository, times(1)).findByMasterLineName(lineItem);
    Assert.assertNotNull(entityResponse);
  }

  @Test
  public void testToCreateMasterData() throws IOException {
    ArcMasterData entity = createArcMasterDataList().get(0);
    when(arcMasterRepository.save(entity)).thenReturn(entity);
    ResponseEntity<ArcMasterData> entityResponse = service.createMasterData(entity);
    verify(arcMasterRepository, times(1)).save(entity);
    Assert.assertNotNull(entityResponse);
  }

  @Test
  public void testToUpdateMasterData() throws IOException {
    ArcMasterData entity = createArcMasterDataList().get(0);
    when(arcMasterRepository.save(entity)).thenReturn(entity);
    ArcMasterData entityResponse = service.update(Optional.of(entity), entity);
    verify(arcMasterRepository, times(1)).save(entity);
    Assert.assertNotNull(entityResponse);
  }

  @Test
  public void testToGetAllMasterData() throws IOException {
    when(arcMasterRepository.findAll()).thenReturn(createArcMasterDataList());
    List<ArcMasterData> entityResponse = service.getAllMetadata();
    verify(arcMasterRepository, times(1)).findAll();
    Assert.assertNotNull(entityResponse);
    Assert.assertEquals(3, entityResponse.size());
  }

  private List<ArcMasterData> createArcMasterDataList() throws IOException {
    final ObjectMapper jsonMapper = new ObjectMapper();
    jsonMapper.configure(SerializationFeature.WRITE_DATES_AS_TIMESTAMPS, false);
    jsonMapper.registerModule(new JavaTimeModule());
    List<ArcMasterData> masterDataList =
        jsonMapper.readValue(
            TestUtil.class.getResourceAsStream("controller/private_api/arcMasterData.json"),
            new TypeReference<List<ArcMasterData>>() {});
    return masterDataList;
  }
}
