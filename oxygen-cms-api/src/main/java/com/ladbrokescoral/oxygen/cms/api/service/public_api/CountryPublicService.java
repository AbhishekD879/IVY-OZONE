package com.ladbrokescoral.oxygen.cms.api.service.public_api;

import com.ladbrokescoral.oxygen.cms.api.dto.CountrySettingDto;
import com.ladbrokescoral.oxygen.cms.api.entity.Country;
import com.ladbrokescoral.oxygen.cms.api.entity.CountryData;
import com.ladbrokescoral.oxygen.cms.api.mapping.CountryToCountrySettingsDtoMapper;
import com.ladbrokescoral.oxygen.cms.api.service.ApiService;
import com.ladbrokescoral.oxygen.cms.api.service.CountryService;
import java.util.Collections;
import java.util.List;
import java.util.stream.Collectors;
import org.springframework.stereotype.Service;

@Service
public class CountryPublicService implements ApiService<CountrySettingDto> {

  private final CountryService service;

  public CountryPublicService(CountryService service) {
    this.service = service;
  }

  public List<CountrySettingDto> findByBrand(String brand) {
    return service.findByBrand(brand).stream()
        .findFirst()
        .map(Country::getCountriesData)
        .map(
            countryDataList ->
                countryDataList.stream()
                    .filter(CountryData::getAllowed)
                    .map(CountryToCountrySettingsDtoMapper.INSTANCE::toDto)
                    .collect(Collectors.toList()))
        .orElseGet(Collections::emptyList);
  }
}
