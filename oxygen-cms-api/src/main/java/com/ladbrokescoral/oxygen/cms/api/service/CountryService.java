package com.ladbrokescoral.oxygen.cms.api.service;

import com.ladbrokescoral.oxygen.cms.api.entity.Country;
import com.ladbrokescoral.oxygen.cms.api.repository.CountryRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class CountryService extends AbstractService<Country> {

  @Autowired
  public CountryService(CountryRepository repository) {
    super(repository);
  }
}
