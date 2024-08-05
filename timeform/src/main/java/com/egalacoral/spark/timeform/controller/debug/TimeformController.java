package com.egalacoral.spark.timeform.controller.debug;

import com.egalacoral.spark.timeform.configuration.RestDebugCondition;
import com.egalacoral.spark.timeform.model.greyhound.*;
import com.egalacoral.spark.timeform.service.greyhound.TimeformGreyhoundService;
import com.egalacoral.spark.timeform.service.greyhound.TimeformMeetingService;
import com.egalacoral.spark.timeform.service.greyhound.TimeformPerformanceService;
import com.egalacoral.spark.timeform.service.greyhound.TimeformTrackService;
import java.util.List;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.context.annotation.Conditional;
import org.springframework.web.bind.annotation.*;

/**
 * Example controller ONLY for testing cache functionality.
 *
 * @author Vitalij Havryk
 */
@Conditional(RestDebugCondition.class)
@RestController
public class TimeformController {

  private static final Logger LOGGER = LoggerFactory.getLogger(TimeformController.class);

  TimeformMeetingService timeformMeetingService;

  TimeformGreyhoundService timeformGreyhoundService;

  TimeformPerformanceService timeformPerformanceService;

  TimeformTrackService timeformTrackService;

  @RequestMapping(value = "/meetings", method = RequestMethod.GET)
  @ResponseBody
  public List<Meeting> meetings() {
    LOGGER.info("Get meetings");
    List<Meeting> meeting = timeformMeetingService.getMeetings();
    return meeting;
  }

  @RequestMapping(value = "/greyhounds", method = RequestMethod.GET)
  @ResponseBody
  public List<Greyhound> greyhounds() {
    LOGGER.info("Get greyhounds");
    return timeformGreyhoundService.getGreyhoundsCached();
  }

  @RequestMapping(value = "/meeting/{id}", method = RequestMethod.GET)
  @ResponseBody
  public TimeformMeeting meetings(@PathVariable String id) {
    LOGGER.info("Get meeting with id:{}", id);
    TimeformMeeting meeting = timeformMeetingService.getMeeting(Integer.valueOf(id));
    LOGGER.info("Get meeting: {}", meeting);
    return meeting;
  }

  @RequestMapping(value = "/performances", method = RequestMethod.GET)
  @ResponseBody
  public List<Performance> performances() {
    LOGGER.info("Get performances");
    return (List<Performance>) timeformPerformanceService.getPerformances();
  }

  @RequestMapping(value = "/tracks", method = RequestMethod.GET)
  @ResponseBody
  public List<Track> tracks() {
    LOGGER.info("Get tracks");
    return timeformTrackService.getTracks();
  }

  @Autowired
  public void setTimeformMeetingService(TimeformMeetingService timeformMeetingService) {
    this.timeformMeetingService = timeformMeetingService;
  }

  @Autowired
  public void setTimeformGreyhoundService(TimeformGreyhoundService timeformGreyhoundService) {
    this.timeformGreyhoundService = timeformGreyhoundService;
  }

  @Autowired
  public void setTimeformPerformanceService(TimeformPerformanceService timeformPerformanceService) {
    this.timeformPerformanceService = timeformPerformanceService;
  }

  @Autowired
  public void setTimeformTrackService(TimeformTrackService timeformTrackService) {
    this.timeformTrackService = timeformTrackService;
  }
}
