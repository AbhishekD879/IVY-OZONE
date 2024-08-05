package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.archival.repository.FooterMenuArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.archival.repository.SegmentArchivalRepository;
import com.ladbrokescoral.oxygen.cms.api.dto.FooterMenuV2Dto;
import com.ladbrokescoral.oxygen.cms.api.dto.FooterMenuV3Dto;
import com.ladbrokescoral.oxygen.cms.api.entity.DeviceType;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.FooterMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.FooterMenuService;
import com.ladbrokescoral.oxygen.cms.api.service.ImageEntityService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentService;
import com.ladbrokescoral.oxygen.cms.api.service.SegmentedModuleSerive;
import com.ladbrokescoral.oxygen.cms.api.service.SortableService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgEntityService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FooterMenuPublicService;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig;
import com.ladbrokescoral.oxygen.cms.configuration.ModelMapperConfig;
import java.util.Arrays;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.Mockito;
import org.mockito.junit.MockitoJUnitRunner;
import org.modelmapper.ModelMapper;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.mock.mockito.MockBean;
import org.springframework.context.annotation.Import;
import org.springframework.data.domain.PageRequest;
import org.springframework.http.ResponseEntity;

@RunWith(MockitoJUnitRunner.class)
@Import(ModelMapperConfig.class)
public class FooterMenuApiTest {

  private static final String TEST_LINK_SUBTITLE = "Test link subtitle";
  private static final String USER_ID = "5b28c03dcde7012fe8914da4";
  @Mock private FooterMenuRepository repository;
  @Mock private SvgEntityService<FooterMenu> svgEntityService;
  @Mock private ImageEntityService<FooterMenu> imageEntityService;
  @Autowired private ModelMapper modelMapper;
  @Mock private FooterMenuArchivalRepository footerMenuArchivalRepository;
  @Mock private SegmentService segmentService;
  @Mock private SegmentedModuleSerive segmentedModuleSerive;
  @Mock private ImageConfig.ImagePath imagePath;
  @MockBean private SegmentArchivalRepository segmentArchivalRepository;

  @Mock private FooterMenuApi footerMenuApi;

  @Before
  public void init() {
    FooterMenuService service =
        new FooterMenuService(
            repository,
            imageEntityService,
            svgEntityService,
            imagePath,
            modelMapper,
            footerMenuArchivalRepository,
            segmentService,
            segmentedModuleSerive);
    footerMenuApi = new FooterMenuApi(new FooterMenuPublicService(service));

    PageRequest pageRequest =
        PageRequest.of(0, Integer.MAX_VALUE, SortableService.SORT_BY_SORT_ORDER_ASC);
    FooterMenu entity1 = createMenu(null);
    entity1.setMobile(true);
    FooterMenu entity2 = createMenu(TEST_LINK_SUBTITLE);
    entity2.setDesktop(true);

    when(repository.findUniversalRecordsByBrand("bma", false, pageRequest))
        .thenReturn(Arrays.asList(entity1, entity2));
    when(repository.findUniversalRecordsByBrand(
            Mockito.eq("bma"),
            Mockito.eq(DeviceType.DESKTOP.getValue()),
            Mockito.eq(false),
            Mockito.any(PageRequest.class)))
        .thenReturn(Arrays.asList(entity1, entity2));
  }

  @Test
  public void testFindByBrand() {

    ResponseEntity<List<FooterMenuV3Dto>> responseEntity = footerMenuApi.findByBrand("bma");
    List<FooterMenuV3Dto> body = responseEntity.getBody();
    Assert.assertEquals(2, body.size());
  }

  @Test
  public void testFindByBrandForEmpty() {

    ResponseEntity<List<FooterMenuV3Dto>> responseEntity = footerMenuApi.findByBrand("ladbrokes");
    List<FooterMenuV3Dto> body = responseEntity.getBody();
    Assert.assertEquals(null, body);
  }

  @Test
  public void testFindByBrandAndDeviceType() {

    List<FooterMenuV2Dto> responseEntity =
        footerMenuApi.findByBrand("bma", DeviceType.DESKTOP.getValue().toString());
    Assert.assertEquals(2, responseEntity.size());
  }

  public FooterMenu createMenu(String subTitle) {
    FooterMenu entity = new FooterMenu();
    entity.setId("1");
    entity.setCreatedBy(USER_ID);
    entity.setLinkTitle("Test link title");
    entity.setLinkTitle(subTitle);
    entity.setUniversalSegment(true);
    return entity;
  }
}
