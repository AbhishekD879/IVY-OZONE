package com.ladbrokescoral.oxygen.cms.api.service.interceptors;

import com.ladbrokescoral.oxygen.cms.api.dto.CountrySettingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Country;
import com.ladbrokescoral.oxygen.cms.api.service.public_api.CountryPublicService;
import java.util.Arrays;
import java.util.List;
import lombok.Getter;
import org.junit.Before;
import org.junit.runner.RunWith;
import org.junit.runners.Parameterized;
import org.junit.runners.Parameterized.Parameters;
import org.mockito.InjectMocks;
import org.mockito.Mock;

@RunWith(Parameterized.class)
public class CountriesAfterSaveListenerTest extends AbstractAfterSaveListenerTest<Country> {

  @Mock private CountryPublicService service;
  @Getter @InjectMocks private CountriesAfterSaveListener listener;

  @Getter @Mock private Country entity;
  @Getter private List<CountrySettingDto> collection = Arrays.asList(new CountrySettingDto());

  @Parameters
  public static List<Object[]> data() {
    return Arrays.asList(
        new Object[][] {
          {"bma", "api/bma", "countries-settings"},
          {"connect", "api/connect", "countries-settings"}
        });
  }

  @Before
  public void init() {

    given(service.findByBrand(anyString())).willReturn(this.getCollection());
  }
}
