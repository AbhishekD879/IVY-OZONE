package com.egalacoral.spark.timeform.controller;

import com.egalacoral.spark.timeform.api.tools.Tools;
import com.egalacoral.spark.timeform.service.greyhound.TimeformBatchService;
import com.egalacoral.spark.timeform.service.horseracing.HorseRacingBatchService;
import java.text.ParseException;
import java.text.SimpleDateFormat;
import java.util.Date;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

@RestController
public class AdHocRequestController {

  private static final Logger LOGGER = LoggerFactory.getLogger(AdHocRequestController.class);

  private TimeformBatchService timeformBatchService;

  private HorseRacingBatchService horseRacingBatchService;

  @Autowired
  public void setTimeformMeetingService(TimeformBatchService timeformBatchService) {
    this.timeformBatchService = timeformBatchService;
  }

  @Autowired
  public void setHorseRacingBatchService(HorseRacingBatchService horseRacingBatchService) {
    this.horseRacingBatchService = horseRacingBatchService;
  }

  @RequestMapping(value = "/adhoc/meetings", method = RequestMethod.POST)
  @ResponseBody
  public String adHocRequest(@RequestParam(value = "date", required = true) String dateStr) {
    LOGGER.info("ad hoc request for meetings");
    SimpleDateFormat sdf = Tools.simpleDateFormat("yyyy-MM-dd");
    try {
      Date d = sdf.parse(dateStr);
      timeformBatchService.fetchMeetingsByAdHocRequest(d);
    } catch (ParseException e) {
      LOGGER.error("", e);
      return "ERROR";
    }
    return "OK";
  }

  @RequestMapping(value = "/horseracing/adhoc/meetings", method = RequestMethod.POST)
  @ResponseBody
  public String horseRacingadHocRequest(
      @RequestParam(value = "date", required = true) String dateStr) {
    LOGGER.info("ad hoc request for meetings");
    SimpleDateFormat sdf = Tools.simpleDateFormat("yyyy-MM-dd");
    try {
      Date d = sdf.parse(dateStr);
      horseRacingBatchService.meetingsAdHocRequest(d);
    } catch (ParseException e) {
      LOGGER.error("", e);
      return "ERROR";
    }
    return "OK";
  }
}
