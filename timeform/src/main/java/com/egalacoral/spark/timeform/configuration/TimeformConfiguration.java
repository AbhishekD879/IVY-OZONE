package com.egalacoral.spark.timeform.configuration;

import com.egalacoral.spark.siteserver.api.SiteServerAPI;
import com.egalacoral.spark.timeform.service.LockService;
import com.egalacoral.spark.timeform.service.MissingDataChecker;
import com.egalacoral.spark.timeform.service.MissingDataMailSender;
import com.egalacoral.spark.timeform.service.MissingDataValidationCalendarService;
import com.egalacoral.spark.timeform.service.greyhound.MeetingFilterService;
import com.egalacoral.spark.timeform.service.greyhound.TimeformMeetingService;
import com.egalacoral.spark.timeform.service.horseracing.HorseRacingMeetingFilterService;
import com.egalacoral.spark.timeform.service.horseracing.HorseRacingMissingDataMailSender;
import com.egalacoral.spark.timeform.service.horseracing.HorseRacingStorageService;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Properties;
import java.util.Set;
import org.apache.velocity.app.VelocityEngine;
import org.apache.velocity.runtime.RuntimeConstants;
import org.apache.velocity.runtime.resource.loader.ClasspathResourceLoader;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.mail.javamail.JavaMailSender;
import org.springframework.mail.javamail.JavaMailSenderImpl;

@Configuration
public class TimeformConfiguration {

  @Bean
  public JavaMailSender javaMailSender( //
      @Value("${aws.smtp.host}") String smtpHost, //
      @Value("${mail.smtp.port}") int smtpPort, //
      @Value("${aws.smtp.username}") String smtpUser, //
      @Value("${aws.smtp.password}") String smtpPassword, //
      @Value("${mail.transport.protocol}") String smtpProtocol) //
      {
    JavaMailSenderImpl javaMailSenderImpl = new JavaMailSenderImpl();
    javaMailSenderImpl.setHost(smtpHost);
    javaMailSenderImpl.setPort(smtpPort);
    javaMailSenderImpl.setUsername(smtpUser);
    javaMailSenderImpl.setPassword(smtpPassword);
    javaMailSenderImpl.setProtocol(smtpProtocol);
    Properties props = new Properties();
    props.setProperty("mail.smtps.auth", "true");
    props.setProperty("mail.smtp.ssl.enable", "true");
    props.setProperty("mail.transport.protocol", smtpProtocol);
    javaMailSenderImpl.setJavaMailProperties(props);

    return javaMailSenderImpl;
  }

  @Bean
  public VelocityEngine velocityEngine() {
    VelocityEngine velocityEngine = new VelocityEngine();
    velocityEngine.setProperty(RuntimeConstants.RESOURCE_LOADER, "classpath");
    velocityEngine.setProperty(
        "classpath.resource.loader.class", ClasspathResourceLoader.class.getName());
    return velocityEngine;
  }

  @Bean
  public MissingDataChecker missingDataChecker( //
      SiteServerAPI siteServerAPI, //
      TimeformMeetingService meetingService, //
      MeetingFilterService meetingFilterService, //
      @Value("${siteserver.class.id}") String classId, //
      MissingDataMailSender missingDataMailSender, //
      LockService lockService, //
      @Qualifier("grayhound") MissingDataValidationCalendarService validationCalendarService) {
    MissingDataChecker missingDataChecker =
        new MissingDataChecker(
            validationCalendarService,
            lockService,
            siteServerAPI,
            meetingService,
            meetingFilterService,
            classId);
    missingDataChecker.setListeners(Arrays.asList(missingDataMailSender));

    Set<String> ignoredTypes = new HashSet<>();
    ignoredTypes.add("Ante-Post Races");
    ignoredTypes.add("Millersfield");
    ignoredTypes.add("Brushwood");
    missingDataChecker.setIgnoredTypes(ignoredTypes);

    Set<String> ignoredMarkets = new HashSet<>();
    ignoredMarkets.add("Trap Market");
    missingDataChecker.setIgnoredMarkets(ignoredMarkets);

    Set<String> ignoredSelections = new HashSet<>();
    ignoredSelections.add("UNNAMED FAVOURITE");
    missingDataChecker.setIgnoredSelections(ignoredSelections);

    return missingDataChecker;
  }

  @Bean
  @Qualifier("horses")
  public MissingDataChecker horsesMissingDataChecker( //
      SiteServerAPI siteServerAPI, //
      HorseRacingStorageService meetingService, //
      HorseRacingMeetingFilterService meetingFilterService, //
      @Value("${siteserver.horseracing.live.class.id}") String classId, //
      HorseRacingMissingDataMailSender missingDataMailSender, //
      LockService lockService, //
      @Qualifier("horses") MissingDataValidationCalendarService validationCalendarService) {

    MissingDataChecker missingDataChecker =
        new MissingDataChecker(
            validationCalendarService,
            lockService,
            siteServerAPI,
            meetingService,
            meetingFilterService,
            classId);
    missingDataChecker.setListeners(Arrays.asList(missingDataMailSender));

    Set<String> ignoredTypes = new HashSet<>();
    ignoredTypes.add("Steepledowns");
    ignoredTypes.add("Glebewood");
    ignoredTypes.add("Hope Valley");
    ignoredTypes.add("Stratfield");
    ignoredTypes.add("Sprintvalley");
    ignoredTypes.add("Portman Park");
    missingDataChecker.setIgnoredTypes(ignoredTypes);

    Set<String> ignoredSelections = new HashSet<>();
    ignoredSelections.add("Unnamed Favourite");
    ignoredSelections.add("Unnamed 2nd Favourite");
    missingDataChecker.setIgnoredSelections(ignoredSelections);

    Set<String> ignoredFalgs = new HashSet<>();
    ignoredFalgs.add("EVFLAG_AP");
    ignoredFalgs.add("EVFLAG_APR");
    ignoredFalgs.add("EVFLAG_AIR");
    missingDataChecker.setIgnoredClassFlagCodes(ignoredFalgs);

    Set<String> ignoredStatuseDescriptions = new HashSet<>();
    ignoredStatuseDescriptions.add("Dropped out at the five day stage");
    ignoredStatuseDescriptions.add("Dropped out at the four day stage");
    ignoredStatuseDescriptions.add("Dropped out at the overnight stage");
    ignoredStatuseDescriptions.add("Dropped out during early closers");
    missingDataChecker.setIgnoredStatusDescriptions(ignoredStatuseDescriptions);

    return missingDataChecker;
  }
}
