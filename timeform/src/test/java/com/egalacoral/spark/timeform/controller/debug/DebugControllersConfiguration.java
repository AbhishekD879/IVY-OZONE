package com.egalacoral.spark.timeform.controller.debug;

import com.egalacoral.spark.timeform.scheduler.horseracing.ConsumeHorseRacingMeetingsScheduler;
import com.egalacoral.spark.timeform.service.ActionCalendarStorageService;
import com.egalacoral.spark.timeform.service.MissingDataValidationCalendarService;
import com.egalacoral.spark.timeform.service.greyhound.TimeformGreyhoundService;
import com.egalacoral.spark.timeform.service.greyhound.TimeformMeetingService;
import com.egalacoral.spark.timeform.service.greyhound.TimeformPerformanceService;
import com.egalacoral.spark.timeform.service.greyhound.TimeformTrackService;
import com.egalacoral.spark.timeform.service.horseracing.*;
import com.egalacoral.spark.timeform.timer.TimerService;
import org.mockito.Mockito;
import org.springframework.boot.actuate.metrics.GaugeService;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Import;

@Import(value = {HorseRaceController.class, QAController.class, TimeformController.class})
public class DebugControllersConfiguration {

  @Bean
  HorseRacingStorageService horseRacingStorageService() {
    return Mockito.mock(HorseRacingStorageService.class);
  }

  @Bean
  HorseRacingBatchService horseRacingBatchService() {
    return Mockito.mock(HorseRacingBatchService.class);
  }

  @Bean
  HorseRacingPerformanceService horseRacingPerformanceService() {
    return Mockito.mock(HorseRacingPerformanceService.class);
  }

  @Bean
  HorseRacingHorseService horseRacingHorseService() {
    return Mockito.mock(HorseRacingHorseService.class);
  }

  @Bean
  HorseRacingCourseService horseRacingCourseService() {
    return Mockito.mock(HorseRacingCourseService.class);
  }

  @Bean
  HorseRacingCountriesService horseRacingCountriesService() {
    return Mockito.mock(HorseRacingCountriesService.class);
  }

  @Bean
  MissingDataValidationCalendarService missingDataValidationCalendarService() {
    return Mockito.mock(MissingDataValidationCalendarService.class);
  }

  @Bean
  ConsumeHorseRacingMeetingsScheduler consumeHorseRacingMeetingsScheduler() {
    return Mockito.mock(ConsumeHorseRacingMeetingsScheduler.class);
  }

  @Bean
  TimeformMeetingService timeformMeetingService() {
    return Mockito.mock(TimeformMeetingService.class);
  }

  @Bean
  TimeformGreyhoundService timeformGreyhoundService() {
    return Mockito.mock(TimeformGreyhoundService.class);
  }

  @Bean
  TimeformPerformanceService timeformPerformanceService() {
    return Mockito.mock(TimeformPerformanceService.class);
  }

  @Bean
  TimeformTrackService timeformTrackService() {
    return Mockito.mock(TimeformTrackService.class);
  }

  @Bean
  ActionCalendarStorageService actionCalendarStorageService() {
    return Mockito.mock(ActionCalendarStorageService.class);
  }

  @Bean
  TimerService timerService() {
    return Mockito.mock(TimerService.class);
  }

  @Bean
  GaugeService gaugeService() {
    return Mockito.mock(GaugeService.class);
  }

  @Bean
  HorseRacingCourseMapService horseRacingCourseMapService() {
    return Mockito.mock(HorseRacingCourseMapService.class);
  }
}
