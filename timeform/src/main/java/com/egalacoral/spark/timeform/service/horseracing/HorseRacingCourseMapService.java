package com.egalacoral.spark.timeform.service.horseracing;

import com.egalacoral.spark.timeform.model.horseracing.HRCourseMap;
import com.egalacoral.spark.timeform.model.horseracing.HRCourseMapInfo;
import com.egalacoral.spark.timeform.storage.Storage;
import java.util.Collection;
import java.util.Map;
import java.util.Optional;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

@Component
public class HorseRacingCourseMapService {

  private static final Logger LOGGER = LoggerFactory.getLogger(HorseRacingCountriesService.class);

  public static final String CACHE_NAME = "hr_course_map";

  private final Storage storage;

  @Autowired
  public HorseRacingCourseMapService(Storage storage) {
    this.storage = storage;
  }

  // @Cacheable("hrCourseMap::byId")
  public HRCourseMap getHRCourseMap(String uuid) {
    return getMap().get(uuid);
  }

  // @Cacheable("hrCourseMapInfo::byCourseMapId")
  public Optional<HRCourseMapInfo> getCourseMap(String courseMapId) {
    return getAllCourseMapInfo().stream().filter(m -> m.getUuid().equals(courseMapId)).findAny();
  }

  public void save(HRCourseMap hrCourseMap) {
    getMap().put(hrCourseMap.getUUID(), hrCourseMap);
  }

  public void update(String uuid, HRCourseMap hrCourseMap) {
    Map<String, HRCourseMap> map = getMap();
    Map<String, HRCourseMap> result =
        map.entrySet().stream()
            .filter(mapEntry -> mapEntry.getKey().equals(uuid))
            .map(
                entry -> {
                  entry.getValue().setContentType(hrCourseMap.getContentType());
                  entry.getValue().setBytes(hrCourseMap.getBytes());
                  entry.getValue().setUpdateDate(hrCourseMap.getUpdateDate());
                  return entry;
                })
            .collect(Collectors.toMap(e -> e.getKey(), e -> e.getValue()));
    map.putAll(result);
  }

  public void clear() {
    LOGGER.info("Cleared countries");
    getMap().clear();
  }

  public Collection<HRCourseMapInfo> getAllCourseMapInfo() {
    return getMap() //
        .values() //
        .stream() //
        .map(cm -> new HRCourseMapInfo(cm)) //
        .collect(Collectors.toList());
  }

  private Map<String, HRCourseMap> getMap() {
    return storage.getMap(CACHE_NAME);
  }
}
