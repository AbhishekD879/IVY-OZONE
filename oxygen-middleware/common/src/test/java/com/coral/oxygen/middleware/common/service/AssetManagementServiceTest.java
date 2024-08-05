package com.coral.oxygen.middleware.common.service;

import com.coral.oxygen.middleware.common.repository.AssetManagementRepository;
import com.coral.oxygen.middleware.pojos.model.output.AssetManagement;
import com.coral.oxygen.middleware.pojos.model.output.EventsModuleData;
import com.coral.oxygen.middleware.pojos.model.output.inplay.TypeSegment;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Map;
import java.util.Optional;
import java.util.concurrent.ConcurrentHashMap;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.jupiter.api.Assertions;
import org.junit.runner.RunWith;
import org.mockito.InjectMocks;
import org.mockito.Mockito;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.test.context.junit4.SpringRunner;
import org.springframework.test.util.ReflectionTestUtils;

@RunWith(SpringRunner.class)
public class AssetManagementServiceTest {

  @MockBean private AssetManagementRepository assetManagementRepository;

  @InjectMocks private AssetManagementService assetManagementService;

  @Before
  public void init() {
    assetManagementService = new AssetManagementService(assetManagementRepository);
    Mockito.when(assetManagementRepository.saveAll(Mockito.anyList()))
        .thenReturn(List.of(getAssetManagement()));
    Mockito.when(assetManagementRepository.findByTeamNameIgnoreCaseAndSportId("LIVERPOOL", 16))
        .thenReturn(Optional.of(getAssetManagement()));
    Mockito.when(assetManagementRepository.findByTeamNameIgnoreCaseAndSportId("ARSENAL", 16))
        .thenReturn(Optional.of(getAssetManagement()));

    Mockito.when(assetManagementRepository.findBySportId(16))
        .thenReturn(List.of(getAssetManagement()));

    Mockito.when(assetManagementRepository.findBySportId(21))
        .thenReturn(List.of(getAssetManagement()));
    Mockito.when(assetManagementRepository.findAll()).thenReturn(List.of(getAssetManagement()));

    Mockito.when(assetManagementRepository.findBySportId(18)).thenReturn(Collections.emptyList());
  }

  @Test
  public void testSaveAll() {
    AssetManagement asset1 = getAssetManagement();
    asset1.setHighlightCarouselToggle(true);
    Iterable<AssetManagement> assets =
        assetManagementService.saveAll(Arrays.asList(getAssetManagement(), asset1));
    Assert.assertNotNull(assets);
    Assert.assertTrue(assets.iterator().hasNext());
  }

  @Test
  public void testSaveAllForFeaturedTrue() {
    AssetManagement asset1 = getAssetManagement();
    asset1.setHighlightCarouselToggle(true);
    ReflectionTestUtils.setField(assetManagementService, "isFeaturedTask", true);
    Iterable<AssetManagement> assets =
        assetManagementService.saveAll(Arrays.asList(getAssetManagement(), asset1));
    Assert.assertNotNull(assets);
    Assert.assertTrue(assets.iterator().hasNext());
  }

  @Test
  public void testSaveAllWithLastGeneratedAsset() {

    EventsModuleData data = new EventsModuleData();
    data.setUS(false);
    data.setName("Liverpool vs Arsenal");
    data.setCategoryId("16");
    Assertions.assertDoesNotThrow(() -> assetManagementService.setAssetManagementMetaData(data));
    data.setName("India vs Pak");
    Assertions.assertDoesNotThrow(() -> assetManagementService.setAssetManagementMetaData(data));

    AssetManagement asset1 = getAssetManagement();
    asset1.setHighlightCarouselToggle(true);
    Iterable<AssetManagement> assets =
        assetManagementService.saveAll(Arrays.asList(getAssetManagement(), asset1));
    Assert.assertNotNull(assets);
    Assert.assertTrue(assets.iterator().hasNext());
  }

  @Test
  public void testSetAssetManagementDataForEventModule() {
    EventsModuleData data = new EventsModuleData();
    data.setUS(false);
    data.setName("Liverpool vs Arsenal");
    data.setCategoryId("16");
    Assertions.assertDoesNotThrow(() -> assetManagementService.setAssetManagementMetaData(data));
    data.setName("India vs Pak");
    Assertions.assertDoesNotThrow(() -> assetManagementService.setAssetManagementMetaData(data));

    data.setName("Liverpool vs Arsenal");
    data.setUS(true);
    Assertions.assertDoesNotThrow(() -> assetManagementService.setAssetManagementMetaData(data));
    data.setName("India vs Pak");
    Assertions.assertDoesNotThrow(() -> assetManagementService.setAssetManagementMetaData(data));

    data.setName("India vs");
    Assertions.assertDoesNotThrow(() -> assetManagementService.setAssetManagementMetaData(data));

    AssetManagement asset1 = getAssetManagement();
    asset1.setHighlightCarouselToggle(true);

    Iterable<AssetManagement> assets =
        assetManagementService.saveAll(Arrays.asList(getAssetManagement(), asset1));
    Assert.assertNotNull(assets);
  }

  @Test
  public void testSetAssetForTypeSegment() {
    TypeSegment typeSegment = new TypeSegment();
    typeSegment.setTypeName("Arsenal");
    Assertions.assertDoesNotThrow(
        () -> assetManagementService.setAssetForTypeSegment(typeSegment, "16"));
  }

  @Test
  public void testClearLastGenerationTeams() {
    Assertions.assertDoesNotThrow(() -> assetManagementService.clearLastGenerationTeams());
  }

  @Test
  public void testSetAssetManagementDataForEventModuleForException() {

    EventsModuleData data = new EventsModuleData();
    data.setUS(false);
    data.setName("Liverpool vs Arsenal");
    data.setCategoryId("16");
    Mockito.when(assetManagementRepository.findByTeamNameIgnoreCaseAndSportId("LIVERPOOL", 16))
        .thenThrow(new RuntimeException());

    Assertions.assertDoesNotThrow(() -> assetManagementService.setAssetManagementMetaData(data));
  }

  @Test
  public void testFindByTeamNameAndSportId() {
    Optional<AssetManagement> assetManagement =
        assetManagementService.findByTeamNameAndSportId("LIVERPOOL", "16");
    Assert.assertTrue(assetManagement.isPresent());
    Assert.assertEquals(16L, (int) assetManagement.get().getSportId());
  }

  @Test
  public void testFindByTeamNameAndSportIdForPrimaryNotFound() {
    AssetManagement assetManagement1 = getAssetManagement();
    assetManagement1.setSecondaryNames(null);
    Mockito.when(assetManagementRepository.findBySportId(16)).thenReturn(List.of(assetManagement1));
    Optional<AssetManagement> assetManagement =
        assetManagementService.findByTeamNameAndSportId("Arsenala", "16");
    Assert.assertFalse(assetManagement.isPresent());
  }

  @Test
  public void testFindByTeamNameAndSportIdForPrimaryNotFoundAndSecondaryFound() {
    Optional<AssetManagement> assetManagement =
        assetManagementService.findByTeamNameAndSportId("Liverpool1", "21");
    Assert.assertTrue(assetManagement.isPresent());
    Assert.assertEquals(16L, (int) assetManagement.get().getSportId());
  }

  @Test
  public void testFindByTeamNameAndSportIdForPrimaryNotFoundAndSecondaryNotMatch() {
    Optional<AssetManagement> assetManagement =
        assetManagementService.findByTeamNameAndSportId("Liverpool", "21");
    Assert.assertFalse(assetManagement.isPresent());
  }

  @Test
  public void testSaveAllForExistingKey() {

    Mockito.when(assetManagementRepository.findByTeamNameIgnoreCaseAndSportId("Liverpool", 16))
        .thenReturn(Optional.of(getAssetManagement()));

    Optional<AssetManagement> assetManagement =
        assetManagementService.findByTeamNameAndSportId("Liverpool", "16");

    Map<String, Optional<AssetManagement>> assets = new ConcurrentHashMap<>();
    assets.put("a", assetManagement);
    ReflectionTestUtils.setField(assetManagementService, "assets", assets);

    AssetManagement asset1 = getAssetManagement();
    asset1.setTeamName("Arsenal");
    asset1.setHighlightCarouselToggle(true);

    Assertions.assertDoesNotThrow(
        () -> assetManagementService.saveAll(Arrays.asList(getAssetManagement(), asset1)));

    Assert.assertTrue(assetManagement.isPresent());
  }

  @Test
  public void testFindByTeamNameAndSportIdForPrimaryNotFoundAndSecondaryNotFound() {
    Optional<AssetManagement> assetManagement =
        assetManagementService.findByTeamNameAndSportId("Arsenal", "18");
    Assert.assertFalse(assetManagement.isPresent());
  }

  @Test
  public void testFindAll() {
    Iterable<AssetManagement> assetManagement = assetManagementService.findAll();
    Assert.assertTrue(assetManagement.iterator().hasNext());
  }

  private AssetManagement getAssetManagement() {
    AssetManagement assetManagement = new AssetManagement();
    assetManagement.setSportId(16);
    assetManagement.setId("1");
    assetManagement.setPrimaryColour("#454454");
    assetManagement.setTeamName("Liverpool");
    assetManagement.setSecondaryNames(Arrays.asList("Liverpool1"));

    return assetManagement;
  }
}
