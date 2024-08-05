package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.dto.ConnectMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.ConnectMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.ConnectMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ConnectMenuService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgEntityService;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.ConnectMenuPublicService;
import java.util.Arrays;
import java.util.List;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.http.ResponseEntity;

@RunWith(MockitoJUnitRunner.class)
public class ConnectMenuApiTest {

  private static final String EMPTY_SUBTITLE = "";
  private static final String TEST_LINK_SUBTITLE = "Test link subtitle";
  private static final String USER_ID = "5b28c03dcde7012fe8914da4";
  @Mock private ConnectMenuRepository repository;
  @Mock private SvgEntityService<ConnectMenu> svgEntityService;
  @Mock private ConnectMenuApi connectPublicaApi;

  @Before
  public void init() {
    ConnectMenuService service =
        new ConnectMenuService(repository, svgEntityService, EMPTY_SUBTITLE);
    connectPublicaApi = new ConnectMenuApi(new ConnectMenuPublicService(service));
  }

  @Test
  public void testGetByBrand() {
    ConnectMenu entity1 = createMenu(null);
    ConnectMenu entity2 = createMenu(TEST_LINK_SUBTITLE);

    when(repository.findAllByBrandAndDisabledOrderBySortOrderAsc("connect", Boolean.FALSE))
        .thenReturn(Arrays.asList(entity1, entity2));

    ResponseEntity<List<ConnectMenuDto>> responseEntity = connectPublicaApi.findByBrand("connect");
    List<ConnectMenuDto> body = responseEntity.getBody();
    Assert.assertEquals(2, body.size());
    Assert.assertEquals(TEST_LINK_SUBTITLE, body.get(1).getLinkSubtitle());
    Assert.assertEquals(EMPTY_SUBTITLE, body.get(0).getLinkSubtitle());
    Assert.assertEquals(Boolean.TRUE, body.get(0).getUpgradePopup());
  }

  public ConnectMenu createMenu(String subTitle) {
    ConnectMenu entity = new ConnectMenu();
    entity.setId("1");
    entity.setCreatedBy(USER_ID);
    entity.setLinkTitle("Test link title");
    entity.setLinkSubtitle(subTitle);
    entity.setUpgradePopup(true);
    return entity;
  }
}
