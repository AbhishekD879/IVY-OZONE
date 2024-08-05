package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.BannerDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Banner;
import com.ladbrokescoral.oxygen.cms.api.entity.SportCategory;
import com.ladbrokescoral.oxygen.cms.api.repository.SportCategoryRepository;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.BannerPublicService;
import java.util.Arrays;
import java.util.List;
import java.util.Optional;
import lombok.Getter;
import org.bson.types.ObjectId;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.Spy;

@RunWith(Parameterized.class)
public class BannersAfterSaveListenerTest extends AbstractAfterSaveListenerTest<Banner> {

  @Mock private BannerPublicService service;
  @Mock private SportCategoryRepository repository;
  @Getter @InjectMocks private BannersAfterSaveListener listener;

  @Getter @Spy Banner entity = new Banner();
  @Getter private List<BannerDto> collection = Arrays.asList(new BannerDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/v2/bma/banners", null},
          {"connect", "api/v2/connect/banners", null}
        });
  }

  @Before
  public void init() {
    entity.setCategoryId(new ObjectId());
    given(repository.findById(anyString())).willReturn(Optional.of(new SportCategory()));
    given(service.find(anyString(), isNull())).willReturn(this.getCollection());
  }
}
