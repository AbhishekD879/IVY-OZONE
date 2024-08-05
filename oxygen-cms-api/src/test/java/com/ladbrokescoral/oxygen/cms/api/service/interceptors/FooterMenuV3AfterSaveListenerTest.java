package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.FooterMenuV2Dto;
import com.ladbrokescoral.oxygen.cms.api.dto.FooterMenuV3Dto;
import com.ladbrokescoral.oxygen.cms.api.entity.FooterMenu;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.FooterMenuPublicService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.springframework.data.mongodb.core.mapping.event.AfterSaveEvent;

@RunWith(Parameterized.class)
public class FooterMenuV3AfterSaveListenerTest extends AbstractAfterSaveListenerTest<FooterMenu> {

  @Mock private FooterMenuPublicService service;
  @Getter @InjectMocks private FooterMenuV3AfterSaveListener listener;

  @Getter @Mock private FooterMenu entity;
  @Getter private List<FooterMenuV3Dto> collection = Arrays.asList(new FooterMenuV3Dto());
  @Getter private List<FooterMenuV2Dto> collectionV2 = Arrays.asList(new FooterMenuV2Dto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/v3/bma", "footer-menu"},
          {"connect", "api/v3/connect", "footer-menu"}
        });
  }

  @Before
  public void init() {
    given(service.find(anyString())).willReturn(this.getCollection());
    given(service.find(anyString(), anyString())).willReturn(this.getCollectionV2());
  }

  @Test
  public void shouldAfterSaveEvent() throws Exception {

    // given
    given(getEntity().getBrand()).willReturn(brand);

    // when
    this.getListener()
        .onAfterSave(new AfterSaveEvent<FooterMenu>(getEntity(), null, "footermenus"));

    // then
    if (null != getCollection()) {
      then(context).should().upload(brand, path, filename, getCollection());
    }
  }

  @After
  public void shouldHaveNoMoreInteractions() {
    then(context)
        .should()
        .upload(brand, "api/v2/" + brand + "/footer-menu", "mobile", getCollectionV2());
    then(context)
        .should()
        .upload(brand, "api/v2/" + brand + "/footer-menu", "tablet", getCollectionV2());
    then(context)
        .should()
        .upload(brand, "api/v2/" + brand + "/footer-menu", "desktop", getCollectionV2());
  }
}
