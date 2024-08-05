package com.ladbrokescoral.oxygen.cms.api.controller.public_api;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.dto.RightMenuDto;
import com.ladbrokescoral.oxygen.cms.api.entity.RightMenu;
import com.ladbrokescoral.oxygen.cms.api.repository.RightMenuExtendedRepository;
import com.ladbrokescoral.oxygen.cms.api.service.RightMenuService;
import com.ladbrokescoral.oxygen.cms.api.service.impl.ImageServiceImpl.Size;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.RightMenuPublicService;
import com.ladbrokescoral.oxygen.cms.configuration.ImageConfig.ImagePath;
import java.util.List;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;
import org.springframework.http.ResponseEntity;

@RunWith(MockitoJUnitRunner.class)
public class RightMenuApiTest {

  @Mock private RightMenuExtendedRepository rightMenuExtendedRepository;

  private RightMenuApi rightMenuApi;

  @Before
  public void init() {
    RightMenuService rightMenuService =
        new RightMenuService(
            null,
            rightMenuExtendedRepository,
            null,
            null,
            ImagePath.builder()
                .smallSize(new Size("40x40"))
                .mediumSize(new Size("40x40"))
                .largeSize(new Size("40x40"))
                .build());
    rightMenuApi = new RightMenuApi(new RightMenuPublicService(rightMenuService));
  }

  @Test
  public void findByBrand() throws Exception {
    List<RightMenu> rightMenus =
        TestUtil.deserializeListWithJackson(
            "controller/public_api/rightMenuFromDB.json", RightMenu.class);

    when(rightMenuExtendedRepository.findRightMenus("connect")).thenReturn(rightMenus);

    List<RightMenuDto> expected =
        TestUtil.deserializeListWithJackson(
            "controller/public_api/rightMenuDto.json", RightMenuDto.class);

    ResponseEntity result = rightMenuApi.findByBrand("connect");
    assertEquals(expected, result.getBody());
  }
}
