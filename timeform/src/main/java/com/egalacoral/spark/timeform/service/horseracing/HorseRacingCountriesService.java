package com.egalacoral.spark.timeform.service.horseracing;

import com.egalacoral.spark.timeform.model.horseracing.HRCountry;
import com.egalacoral.spark.timeform.rql.QueryStream;
import com.egalacoral.spark.timeform.storage.Storage;
import java.util.*;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/** Created by llegkyy on 21.09.16. */
@Service
public class HorseRacingCountriesService {
  private static final Logger LOGGER = LoggerFactory.getLogger(HorseRacingCountriesService.class);

  public static final String HR_COUNTRY_CACHE_NAME = "country";

  private Storage storage;

  @Autowired
  public HorseRacingCountriesService(Storage storage) {
    this.storage = storage;
  }

  // @Cacheable("hrCountries::all")
  public List<HRCountry> getHRCountries() {
    Map<String, HRCountry> countries = storage.getMap(HR_COUNTRY_CACHE_NAME);
    return countries.values().stream().collect(Collectors.toList());
  }

  // @Cacheable("hrCountries::filter")
  public List<HRCountry> getCountries(Integer top, Integer skip, String orderby, String filter) {
    return QueryStream.of(getHRCountries(), filter, orderby, top, skip).toList();
  }

  // @Cacheable("hrCountry::byId")
  public Optional<HRCountry> getCountry(String countryId) {
    return getHRCountries().stream().filter(c -> c.getCountryCode().equals(countryId)).findAny();
  }

  public Boolean isNewCountriesForDateExists(Date date) {
    return !getHRCountriesCodesByMeetingDate(date).isEmpty();
  }

  public void updateCountries(Map<String, HRCountry> retrivedCountryMap, Date date) {
    Map<String, HRCountry> map = storage.getMap(HR_COUNTRY_CACHE_NAME);
    Map<String, HRCountry> result =
        retrivedCountryMap.entrySet().stream()
            .map(
                entry -> {
                  if (map.containsKey(entry.getKey())) {
                    entry.getValue().setUpdateDate(date);
                  }
                  return entry;
                })
            .collect(Collectors.toMap(e -> e.getKey(), e -> e.getValue()));
    map.putAll(result);
    LOGGER.info("Save HR countries  in hazelcast map {}", result.size());
  }

  public void clearCountries() {
    LOGGER.info("Cleared countries");
    getCountryMap().clear();
  }

  private Map<Object, HRCountry> getCountryMap() {
    return storage.getMap(HR_COUNTRY_CACHE_NAME);
  }

  private Collection<String> getHRCountriesCodesByMeetingDate(Date date) {
    Map<String, HRCountry> countries = storage.getMap(HR_COUNTRY_CACHE_NAME);
    return countries.entrySet().stream()
        .filter(
            e ->
                Objects.nonNull(e.getValue().getUpdateDate())
                    && e.getValue().getUpdateDate().compareTo(date) == 0)
        .map(e -> e.getKey())
        .collect(Collectors.toList());
  }
}
