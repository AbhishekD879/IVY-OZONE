package com.egalacoral.spark.timeform.controller.debug;

import com.egalacoral.spark.timeform.configuration.RestDebugCondition;
import com.egalacoral.spark.timeform.model.horseracing.*;
import com.egalacoral.spark.timeform.service.horseracing.*;
import java.util.Collection;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Conditional;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestMethod;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.bind.annotation.RestController;

@Conditional(RestDebugCondition.class)
@RestController
@RequestMapping("horseracing")
public class HorseRaceController {

  private static final Logger LOGGER = LoggerFactory.getLogger(HorseRaceController.class);

  private HorseRacingStorageService storageService;

  private HorseRacingPerformanceService horseRacingPerformanceService;

  private HorseRacingCourseService horseRacingCourseService;

  private HorseRacingHorseService horseRacingHorseService;

  private HorseRacingCountriesService horseRacingCountriesService;

  @RequestMapping(value = "/meetings", method = RequestMethod.GET)
  @ResponseBody
  public List<HRMeeting> meetings() {
    LOGGER.info("Get meetings");
    List<HRMeeting> meeting = storageService.getMeetings();
    return meeting;
  }

  @RequestMapping(value = "/performances", method = RequestMethod.GET)
  @ResponseBody
  public Collection<HRPerformance> performances() {
    LOGGER.info("Get horse racing performances");
    Collection<HRPerformance> hrPerformances = horseRacingPerformanceService.getHRPerformances();
    return hrPerformances;
  }

  @RequestMapping(value = "/horses", method = RequestMethod.GET)
  @ResponseBody
  public List<HRHorse> horses() {
    LOGGER.info("Get horses");
    return horseRacingHorseService.getHorses();
  }

  @RequestMapping(value = "/courses", method = RequestMethod.GET)
  @ResponseBody
  public Collection<HRCourse> courses() {
    LOGGER.info("Get courses");
    return horseRacingCourseService.getHRCourses();
  }

  @RequestMapping(value = "/countries", method = RequestMethod.GET)
  @ResponseBody
  public Collection<HRCountry> countries() {
    LOGGER.info("Get countries");
    return horseRacingCountriesService.getHRCountries();
  }

  @Autowired
  public void setHorseRacingPerformanceService(
      HorseRacingPerformanceService horseRacingPerformanceService) {
    this.horseRacingPerformanceService = horseRacingPerformanceService;
  }

  @Autowired
  public void setStorageService(HorseRacingStorageService storageService) {
    this.storageService = storageService;
  }

  @Autowired
  public void setHorseRacingHorseService(HorseRacingHorseService horseRacingHorseService) {
    this.horseRacingHorseService = horseRacingHorseService;
  }

  @Autowired
  public void setHorseRacingCourseService(HorseRacingCourseService horseRacingCourseService) {
    this.horseRacingCourseService = horseRacingCourseService;
  }

  @Autowired
  public void setHorseRacingCountriesService(
      HorseRacingCountriesService horseRacingCountriesService) {
    this.horseRacingCountriesService = horseRacingCountriesService;
  }
}
