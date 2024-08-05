package com.egalacoral.spark.timeform.service.horseracing;

import com.egalacoral.spark.timeform.model.horseracing.HRCourse;
import com.egalacoral.spark.timeform.rql.QueryStream;
import com.egalacoral.spark.timeform.storage.Storage;
import java.util.*;
import java.util.stream.Collectors;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

/** Created by llegkyy on 16.09.16. */
@Service
public class HorseRacingCourseService {
  private static final Logger LOGGER = LoggerFactory.getLogger(HorseRacingCourseService.class);
  public static final String HR_COURSE_CACHE_NAME = "course";

  private Storage storage;

  @Autowired
  public HorseRacingCourseService(Storage storage) {
    this.storage = storage;
  }

  // @Cacheable("hrCourses::all")
  public List<HRCourse> getHRCourses() {
    Map<Integer, HRCourse> courseMap = storage.getMap(HR_COURSE_CACHE_NAME);
    return courseMap.values().stream().collect(Collectors.toList());
  }

  // @Cacheable("hrCourses::filter")
  public List<HRCourse> getCourses(Integer top, Integer skip, String orderby, String filter) {
    return QueryStream.of(getHRCourses(), filter, orderby, top, skip).toList();
  }

  // @Cacheable("hrCourse::byId")
  public Optional<HRCourse> getCourse(Integer courseId) {
    HRCourse s = (HRCourse) storage.getMap(HR_COURSE_CACHE_NAME).get(courseId);
    return Optional.ofNullable(s);
  }

  public Boolean isNewHRCoursesForDateExists(Date date) {
    return !getHRCourseIdsByUpdatedDate(date).isEmpty();
  }

  public void updateCourses(Map<Integer, HRCourse> retrivedCourseMap, Date date) {
    Map<Integer, HRCourse> map = storage.getMap(HR_COURSE_CACHE_NAME);
    Map<Integer, HRCourse> result =
        retrivedCourseMap.entrySet().stream()
            .map(
                entry -> {
                  if (map.containsKey(entry.getKey())) {
                    entry.getValue().setUpdateDate(date);
                  }
                  return entry;
                })
            .collect(Collectors.toMap(e -> e.getKey(), e -> e.getValue()));
    LOGGER.info("Save HR courses  in hazelcast map {}", result.size());
    map.putAll(result);
  }

  public void clearCourses() {
    LOGGER.info("Cleared courses");
    storage.getMap(HR_COURSE_CACHE_NAME).clear();
  }

  private Collection<Integer> getHRCourseIdsByUpdatedDate(Date date) {
    Map<Integer, HRCourse> courseMap = storage.getMap(HR_COURSE_CACHE_NAME);
    return courseMap.entrySet().stream()
        .filter(
            e ->
                e.getValue().getUpdateDate() != null
                    && e.getValue().getUpdateDate().compareTo(date) == 0)
        .map(e -> e.getKey())
        .collect(Collectors.toList());
  }
}
