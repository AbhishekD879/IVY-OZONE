package com.ladbrokescoral.oxygen.cms.api.controller.private_api;

import static org.junit.Assert.assertEquals;
import static org.mockito.Matchers.anyString;
import static org.mockito.Mockito.when;

import com.ladbrokescoral.oxygen.cms.api.TestUtil;
import com.ladbrokescoral.oxygen.cms.api.entity.Country;
import com.ladbrokescoral.oxygen.cms.api.entity.User;
import com.ladbrokescoral.oxygen.cms.api.service.CountryService;
import com.ladbrokescoral.oxygen.cms.api.service.UserService;
import java.util.List;
import java.util.Optional;
import org.junit.Before;
import org.junit.Test;
import org.junit.runner.RunWith;
import org.mockito.Mock;
import org.mockito.junit.MockitoJUnitRunner;

@RunWith(MockitoJUnitRunner.class)
public class CountriesTest {

  @Mock private CountryService countryService;
  @Mock private UserService userService;

  private Countries countryController;

  @Before
  public void setUp() throws Exception {

    countryController = new Countries(countryService);
    countryController.setUserService(userService);

    List<Country> countries =
        TestUtil.deserializeListWithJackson("controller/private_api/countries.json", Country.class);

    User user =
        TestUtil.deserializeWithJackson("controller/private_api/countries-user.json", User.class);
    when(countryService.findByBrand("bma")).thenReturn(countries);
    when(userService.findOne(anyString())).thenReturn(Optional.of(user));
  }

  @Test
  public void testFindByBrandPopulatesUpdatedByCreatedByField() {
    List<Country> resultList = countryController.readByBrand("bma");
    Country country = resultList.iterator().next();
    assertEquals("email@email.com", country.getCreatedByUserName());
    assertEquals("email@email.com", country.getUpdatedByUserName());
  }
}
