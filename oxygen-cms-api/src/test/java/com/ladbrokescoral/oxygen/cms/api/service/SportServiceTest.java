package com.ladbrokescoral.oxygen.cms.api.service;

import static org.junit.Assert.assertNull;

import com.egalacoral.spark.siteserver.api.BaseFilter;
import com.egalacoral.spark.siteserver.api.SiteServerApi;
import com.egalacoral.spark.siteserver.model.Category;
import com.egalacoral.spark.siteserver.model.Type;
import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.Filename;
import com.ladbrokescoral.oxygen.cms.api.entity.Sport;
import com.ladbrokescoral.oxygen.cms.api.exception.ValidationException;
import com.ladbrokescoral.oxygen.cms.api.repository.SportRepository;
import com.ladbrokescoral.oxygen.cms.api.service.siteserve.SiteServeApiProvider;
import java.util.Arrays;
import java.util.Collections;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.beans.BeanUtils;
import org.springframework.data.domain.Page;
import org.springframework.data.domain.PageRequest;
import org.springframework.test.util.ReflectionTestUtils;
import org.springframework.web.multipart.MultipartFile;

@RunWith(MockitoJUnitRunner.class)
public class SportServiceTest extends BDDMockito {

  @Mock private SportRepository repository;
  @Mock private SiteServerApi siteServerApi;
  @Mock private SiteServeApiProvider siteServeApiProvider;
  @Mock private SportsImageUploadComponent sportsImageUploadComponent;
  @Mock private Category category;

  @Mock Page<Sport> sortOrder;

  @InjectMocks private SportService service;
  private Sport sport;

  @Before
  public void init() throws Exception {

    sport = TestUtil.deserializeWithJackson("test/sport.json", Sport.class);

    Sport orderResponse = new Sport();
    orderResponse.setSortOrder(7.0);

    given(sortOrder.getContent()).willReturn(Arrays.asList(orderResponse));
    given(repository.findAll(any(PageRequest.class))).willReturn(sortOrder);

    given(siteServeApiProvider.api(any())).willReturn(siteServerApi);
    given(siteServerApi.getClassToSubTypeForType(anyList(), any(BaseFilter.class)))
        .willReturn(Optional.of(Collections.singletonList(category)));
    given(category.getCategoryId()).willReturn(Integer.valueOf(104));

    Type type1 = new Type();
    // no public setter for this field
    ReflectionTestUtils.setField(type1, "id", 3705);
    Type type2 = new Type();
    ReflectionTestUtils.setField(type2, "id", 3704);
    Type type3 = new Type();
    ReflectionTestUtils.setField(type3, "id", 3703);
    given(category.getTypes()).willReturn(Arrays.asList(type1, type2, type3));
  }

  @Test
  public void saveTest() {

    sport.setIcon(new Filename());
    sport.setUriSmallIcon("");
    sport.setUriMediumIcon("");
    sport.setUriLargeIcon("");
    assertNull(sport.getLang());

    Sport sportUpdated = new Sport();
    BeanUtils.copyProperties(
        sport,
        sportUpdated,
        "icon",
        "uriSmallIcon",
        "uriMediumIcon",
        "uriLargeIcon",
        "uriSmall",
        "uriMedium",
        "uriLarge",
        "svg",
        "filename",
        "svgFilename",
        "ssCategoryCode");

    service.save(sport);

    sportUpdated.setSortOrder(Double.valueOf(8.0));
    sportUpdated.setLang("en");

    then(sportsImageUploadComponent).should().setDefaultImageSizes(sport);

    then(repository).should().findAll(any(PageRequest.class));
    then(repository).should().save(sportUpdated);
    then(repository).shouldHaveNoMoreInteractions();
  }

  @Test
  public void updateTest() throws Exception {
    Sport updatedSport = TestUtil.deserializeWithJackson("test/sport.json", Sport.class);
    updatedSport.setTypeIds("3703");
    assertNull(updatedSport.getLang());
    sport.setLang("en");
    service.update(sport, updatedSport);

    assertNull(updatedSport.getIcon());
    assertNull(updatedSport.getUriSmallIcon());
    assertNull(updatedSport.getUriMediumIcon());
    assertNull(updatedSport.getUriLargeIcon());
    assertNull(updatedSport.getLang());
    verify(repository, times(1)).save(updatedSport);
  }

  @Test
  public void findTest() {
    service.findAll();
    verify(repository, times(1)).findAll(SortableService.SORT_BY_SORT_ORDER_ASC);

    service.findByBrand("brandName");
    verify(repository, times(1)).findByBrand("brandName", SortableService.SORT_BY_SORT_ORDER_ASC);

    service.findAllByBrandSorted("brandName");
    verify(repository, times(1)).findAllByBrandOrderBySortOrderAsc("brandName");

    service.findAllBySportNameAndBrand("sportName", "brandName");
    verify(repository, times(1))
        .findByImageTitleContainingIgnoreCaseAndBrandIgnoreCaseOrderBySortOrderAsc(
            "sportName", "brandName");

    service.findAllBySportNameAndBrand("sportName", "");
    verify(repository, times(1))
        .findByImageTitleContainingIgnoreCaseOrderBySortOrderAsc("sportName");

    service.findAllBySportNameAndBrand("", "brandName1");
    verify(repository, times(1)).findByBrand("brandName1", SortableService.SORT_BY_SORT_ORDER_ASC);
    service.findAllBySportNameAndBrand("", "");
    verify(repository, times(2)).findAll(SortableService.SORT_BY_SORT_ORDER_ASC);
  }

  @Test
  public void handleUploadedFilesTest() {
    MultipartFile imageFile = mock(MultipartFile.class);
    MultipartFile svgIcon = mock(MultipartFile.class);
    doReturn(Optional.of(sport)).when(repository).findById("sportId");
    doReturn(sport)
        .when(sportsImageUploadComponent)
        .attachImages(sport, imageFile, imageFile, svgIcon);

    service.handleUploadedFiles("sportId", imageFile, imageFile, svgIcon);
    verify(sportsImageUploadComponent, times(1)).attachImages(sport, imageFile, imageFile, svgIcon);
    verify(repository, times(1)).save(sport);
  }

  @Test
  public void deleteUploadedFilesTest() {
    doReturn(Optional.of(sport)).when(repository).findById("sportId");
    SportsImageUploadComponent.SportsImage[] fileTypes =
        new SportsImageUploadComponent.SportsImage[] {SportsImageUploadComponent.SportsImage.ICON};

    service.deleteUploadedFiles("sportId", new String[] {"icon"});
    verify(sportsImageUploadComponent, times(1)).deleteImages(fileTypes, sport);
    verify(repository, times(1)).save(sport);
  }

  @Test(expected = ValidationException.class)
  public void deleteUploadedFilesTest_ValidationException() {
    service.deleteUploadedFiles("sportId", new String[] {"unknown test"});
  }

  @Test
  public void deleteTest() {
    doReturn(Optional.of(sport)).when(repository).findById("sportId");

    service.delete("sportId");
    verify(repository, times(1)).save(sport);
  }
}
