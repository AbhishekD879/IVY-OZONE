package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.AssetManagement;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.SecondaryNameToAssetManagement;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.AssetManagementRepository;
import com.ladbrokescoral.oxygen.cms.api.repository.SecondaryNameToAssetRepository;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class AssetManagementServiceTest extends BDDMockito {

  private static final String ID = "id";

  @Mock private AssetManagementRepository repository;
  @Mock private SecondaryNameToAssetRepository secondaryNameToAssetRepository;
  @Mock private ImageService imageService;

  @InjectMocks private AssetManagementService service;

  @Test
  public void saveTest() {
    AssetManagement assetManagement = prepareAsset(ID);
    when(repository.save(assetManagement)).thenReturn(assetManagement);

    service.save(assetManagement);

    verify(repository, times(1)).save(assetManagement);
    verify(secondaryNameToAssetRepository, times(2))
        .save(any(SecondaryNameToAssetManagement.class));
  }

  @Test
  public void validationPassedTest() {
    AssetManagement assetManagement = prepareAsset(ID);

    when(repository.findByTeamNameAndSportIdAndBrand(anyString(), anyInt(), anyString()))
        .thenReturn(Optional.empty());
    when(secondaryNameToAssetRepository.findByTeamNameAndSportIdAndBrand(
            anyString(), anyInt(), anyString()))
        .thenReturn(Optional.empty());

    service.prepareModelBeforeSave(assetManagement);

    verify(repository, times(3))
        .findByTeamNameAndSportIdAndBrand(anyString(), anyInt(), anyString());
    verify(secondaryNameToAssetRepository, times(3))
        .findByTeamNameAndSportIdAndBrand(anyString(), anyInt(), anyString());
  }

  @Test(expected = ValidationException.class)
  public void validationFailedTest() {

    AssetManagement assetManagement = prepareAsset(ID);

    when(repository.findByTeamNameAndSportIdAndBrand(eq("S1"), anyInt(), anyString()))
        .thenReturn(Optional.empty());
    when(repository.findByTeamNameAndSportIdAndBrand(eq("S2"), anyInt(), anyString()))
        .thenReturn(Optional.of(prepareAsset("other-id")));
    when(secondaryNameToAssetRepository.findByTeamNameAndSportIdAndBrand(
            anyString(), anyInt(), anyString()))
        .thenReturn(Optional.empty());

    service.prepareModelBeforeSave(assetManagement);
  }

  @Test
  public void updateExistedSecondaryNamesTest() {
    AssetManagement assetManagement = prepareAsset(ID);
    when(repository.save(assetManagement)).thenReturn(assetManagement);
    when(secondaryNameToAssetRepository.findAllByAssetId(eq(ID)))
        .thenReturn(prepareSecondaryNames());

    service.save(assetManagement);

    verify(secondaryNameToAssetRepository, times(2))
        .save(any(SecondaryNameToAssetManagement.class));
    verify(secondaryNameToAssetRepository, times(1))
        .delete(any(SecondaryNameToAssetManagement.class));
    service.save(assetManagement);
  }

  @Test
  public void publicApiTest() {

    when(repository.findByTeamNameAndSportIdAndBrand("T2", 1, "bma"))
        .thenReturn(Optional.of(prepareAsset(ID)));
    when(repository.findByTeamNameAndSportIdAndBrand("S1", 1, "bma")).thenReturn(Optional.empty());

    when(secondaryNameToAssetRepository.findByTeamNameAndSportIdAndBrand("S1", 1, "bma"))
        .thenReturn(Optional.of(new SecondaryNameToAssetManagement("S1", 1, "bma", ID)));

    when(repository.findById(ID)).thenReturn(Optional.of(prepareAsset(ID)));

    List<AssetManagement> resultList =
        service.findByBrandAndNamesAndSportId("bma", Arrays.asList("S1", "T2"), 1);
    Assert.assertEquals(2, resultList.size());
  }

  @Test
  public void testDeleteImageAssetManager() {
    String id = "9090";
    when(repository.findById(id)).thenReturn(Optional.of(prepareAsset("899")));
    when(imageService.removeImage(anyString(), anyString())).thenReturn(true);
    AssetManagement result = service.deleteImageAssetManager(id);
    verify(repository, times(1)).save(any(AssetManagement.class));
  }

  private List<SecondaryNameToAssetManagement> prepareSecondaryNames() {
    List<SecondaryNameToAssetManagement> secondaryNames = new ArrayList<>();
    secondaryNames.add(new SecondaryNameToAssetManagement("S1", 1, "bma", ID));
    secondaryNames.add(new SecondaryNameToAssetManagement("S3", 1, "bma", ID));
    return secondaryNames;
  }

  private AssetManagement prepareAsset(String id) {
    AssetManagement asset = new AssetManagement();
    asset.setId(id);
    asset.setSportId(1);
    asset.setBrand("bma");
    asset.setTeamName("T1");
    asset.setSecondaryNames(Arrays.asList("S1", "S2"));
    asset.setTeamsImage(createFileNames("23"));
    return asset;
  }

  private static Filename createFileNames(String svgId) {
    Filename filename = new Filename("name.png");
    filename.setFiletype("png");
    filename.setOriginalname("ogname.png");
    filename.setPath("files/images");
    filename.setSize("2");
    filename.setFullPath("files/image");
    filename.setSvg("svg");
    filename.setSvgId(svgId);
    return filename;
  }
}
