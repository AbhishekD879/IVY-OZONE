package com.egalacoral.spark.timeform.controller.debug;

import com.egalacoral.spark.timeform.api.tools.Tools;
import com.egalacoral.spark.timeform.configuration.RestDebugCondition;
import com.egalacoral.spark.timeform.model.horseracing.HRCourseMapInfo;
import com.egalacoral.spark.timeform.scheduler.horseracing.ConsumeHorseRacingMeetingsScheduler;
import com.egalacoral.spark.timeform.service.ActionCalendarStorageService;
import com.egalacoral.spark.timeform.service.MissingDataValidationCalendarService;
import com.egalacoral.spark.timeform.service.horseracing.*;
import java.text.ParseException;
import java.util.Collection;
import java.util.Date;
import java.util.Map;
import org.joda.time.DateTime;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.context.annotation.Conditional;
import org.springframework.web.bind.annotation.*;

@Conditional(RestDebugCondition.class)
@RestController
public class QAController {

  private static final Logger LOGGER = LoggerFactory.getLogger(QAController.class);

  private MissingDataValidationCalendarService calendarService;

  private HorseRacingStorageService horseRacingStorageService;

  private HorseRacingPerformanceService horseRacingPerformanceService;

  private HorseRacingHorseService horseRacingHorseService;

  private HorseRacingCourseService horseRacingCourseService;

  private HorseRacingCountriesService horseRacingCountriesService;

  private HorseRacingBatchService horseRacingBatchService;

  ConsumeHorseRacingMeetingsScheduler consumeHorseRacingMeetingsScheduler;

  private ActionCalendarStorageService actionCalendarStorageService;

  private HorseRacingCourseMapService horseRacingCourseMapService;

  @Autowired
  public void setHorseRacingCourseMapService(
      HorseRacingCourseMapService horseRacingCourseMapService) {
    this.horseRacingCourseMapService = horseRacingCourseMapService;
  }

  @Autowired
  public void setActionCalendarStorageService(
      ActionCalendarStorageService actionCalendarStorageService) {
    this.actionCalendarStorageService = actionCalendarStorageService;
  }

  @Autowired
  @Qualifier("grayhound")
  public void setCalendarService(MissingDataValidationCalendarService calendarService) {
    this.calendarService = calendarService;
  }

  @Autowired
  public void setHorseRacingStorageService(HorseRacingStorageService horseRacingStorageService) {
    this.horseRacingStorageService = horseRacingStorageService;
  }

  @Autowired
  public void setHorseRacingPerformanceService(
      HorseRacingPerformanceService horseRacingPerformanceService) {
    this.horseRacingPerformanceService = horseRacingPerformanceService;
  }

  @Autowired
  public void setConsumeHorseRacingMeetingsScheduler(
      ConsumeHorseRacingMeetingsScheduler consumeHorseRacingMeetingsScheduler) {
    this.consumeHorseRacingMeetingsScheduler = consumeHorseRacingMeetingsScheduler;
  }

  @Autowired
  public void setHorseRacingHorseService(HorseRacingHorseService horseRacingHorseService) {
    this.horseRacingHorseService = horseRacingHorseService;
  }

  @Autowired
  public void setHorseRacingBatchService(HorseRacingBatchService horseRacingBatchService) {
    this.horseRacingBatchService = horseRacingBatchService;
  }

  @Autowired
  public void setHorseRacingCountriesService(
      HorseRacingCountriesService horseRacingCountriesService) {
    this.horseRacingCountriesService = horseRacingCountriesService;
  }

  @RequestMapping(value = "/qa/resendemails", method = RequestMethod.DELETE)
  @Autowired
  public void setHorseRacingCourseService(HorseRacingCourseService horseRacingCourseService) {
    this.horseRacingCourseService = horseRacingCourseService;
  }

  @RequestMapping(value = "/qa/resendemails", method = RequestMethod.GET)
  @ResponseBody
  public String resendemails() {
    this.calendarService.clear();
    return "OK";
  }

  @RequestMapping(value = "/qa/horseracing/meetings/clear", method = RequestMethod.DELETE)
  @ResponseBody
  public String hrMeetingsClear() {
    this.horseRacingStorageService.clear();
    return "OK";
  }

  @RequestMapping(value = "/qa/horseracing/performances/clear", method = RequestMethod.DELETE)
  @ResponseBody
  public String hrPerformancesClear() {
    this.horseRacingPerformanceService.clearPerformances();
    return "OK";
  }

  @RequestMapping(value = "/qa/horseracing/meetings/init", method = RequestMethod.PUT)
  @ResponseBody
  public String hrMeetingsInit() {
    this.consumeHorseRacingMeetingsScheduler.consumeMeetingsOnStart();
    return "OK";
  }

  @RequestMapping(value = "/qa/horseracing/horses/clear", method = RequestMethod.DELETE)
  @ResponseBody
  public String hrHorsesClear() {
    this.horseRacingHorseService.clearHorses();
    return "OK";
  }

  @RequestMapping(value = "/qa/horseracing/horses/init", method = RequestMethod.PUT)
  @ResponseBody
  public void processHorses(@RequestParam(value = "day") Integer day) {
    day = (day != null) ? day : 0;
    LOGGER.info("Start horses task execution at {}", new Date());
    horseRacingBatchService.consumeHRHorses(new DateTime().toDate());
    horseRacingBatchService.consumeHRHorses(new DateTime().plusDays(1).toDate());
    LOGGER.info("Finished horses task execution at {}", new Date());
  }

  @RequestMapping(value = "/qa/horseracing/courses/clear", method = RequestMethod.DELETE)
  @ResponseBody
  public String hrCoursesClear() {
    this.horseRacingCourseService.clearCourses();
    return "OK";
  }

  @RequestMapping(value = "/qa/horseracing/courses/init", method = RequestMethod.PUT)
  @ResponseBody
  public String processCourses() {
    LOGGER.info("Start courses task execution at {}", new Date());
    horseRacingBatchService.consumeHRCourses(new Date());
    LOGGER.info("Finished courses task execution at {}", new Date());
    return "Sync courses task started";
  }

  @RequestMapping(value = "/qa/horseracing/countries/init", method = RequestMethod.PUT)
  @ResponseBody
  public String processCountries() {
    LOGGER.info("Start countries task execution at {}", new Date());
    horseRacingBatchService.consumeHRCountries(new Date());
    LOGGER.info("Finished countries task execution at {}", new Date());
    return "Sync countries task started";
  }

  @RequestMapping(value = "/qa/horseracing/countries/clear", method = RequestMethod.DELETE)
  @ResponseBody
  public String hrCountriesClear() {
    this.horseRacingCountriesService.clearCountries();
    return "OK";
  }

  @RequestMapping(value = "/qa/actions", method = RequestMethod.GET)
  @ResponseBody
  public Map<String, Date> actions() {
    return actionCalendarStorageService.getAll();
  }

  @RequestMapping(value = "/qa/actions/delete", method = RequestMethod.DELETE)
  @ResponseBody
  public String actions(@RequestParam(value = "name") String name) {
    actionCalendarStorageService.deleteKey(name);
    return "OK";
  }

  @RequestMapping(value = "/qa/horseracing/coursemaps", method = RequestMethod.GET)
  @ResponseBody
  public Collection<HRCourseMapInfo> coursemaps() {
    return horseRacingCourseMapService.getAllCourseMapInfo();
  }

  @RequestMapping(value = "/qa/horseracing/coursemaps/clear", method = RequestMethod.DELETE)
  @ResponseBody
  public String coursemapsClear() {
    horseRacingCourseMapService.clear();
    return "OK";
  }

  @RequestMapping(value = "/qa/horseracing/coursemaps/init", method = RequestMethod.PUT)
  @ResponseBody
  public String coursemapsInit(@RequestParam(value = "date") String date) {
    try {
      horseRacingBatchService.consumeCourseMaps(Tools.simpleDateFormat("yyyy-MM-dd").parse(date));
      return "OK";
    } catch (ParseException e) {
      return e.getMessage();
    }
  }
}
