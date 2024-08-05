package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import com.ladbrokescoral.oxygen.cms.api.entity.ConnectMenu;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.repository.ConnectMenuRepository;
import com.ladbrokescoral.oxygen.cms.api.service.ConnectMenuService;
import com.ladbrokescoral.oxygen.cms.api.service.SvgEntityService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import java.util.Optional;
import org.junit.Assert;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.BDDMockito;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.http.ResponseEntity;

@RunWith(MockitoJUnitRunner.class)
public class ConnectMenuApiTest extends BDDMockito {

  private static final String USER_ID = "5b28c03dcde7012fe8914da4";
  @Mock private ConnectMenuRepository repository;
  @Mock private SvgEntityService<ConnectMenu> svgEntityService;
  @Mock private UserService userService;

  private ConnectMenus connectPrivateApi;

  @Before
  public void init() {
    ConnectMenuService service = new ConnectMenuService(repository, svgEntityService, "");
    connectPrivateApi = new ConnectMenus(service);
    connectPrivateApi.setUserService(userService);
  }

  @Test
  public void testsSaveMenu() {
    ConnectMenu entity = new ConnectMenu();
    entity.setId("1");
    entity.setCreatedBy(USER_ID);
    entity.setLinkTitle("Test link title");
    entity.setLinkSubtitle("Test link subtitle title");
    entity.setUpgradePopup(true);

    when(repository.save(entity)).thenReturn(entity);
    when(userService.findOne(USER_ID)).thenReturn(Optional.of(new User()));

    ResponseEntity<ConnectMenu> responseEntity = connectPrivateApi.create(entity);
    ConnectMenu body = responseEntity.getBody();
    body.equals(entity);
    Assert.assertEquals(body.getLinkSubtitle(), entity.getLinkSubtitle());
  }
}
