package com.ladbrokescoral.oxygen.trendingbets.util;

import com.ladbrokescoral.oxygen.trendingbets.model.TrendingEvent;
import java.time.LocalDateTime;
import java.time.ZoneId;
import java.time.ZonedDateTime;
import java.time.format.DateTimeFormatter;
import java.time.format.DateTimeParseException;
import java.util.Arrays;
import java.util.Date;
import org.springframework.util.StringUtils;

public class TrendingBetsUtil {

  private static final String ZONE_LONDON = "Europe/London";

  private static final String GMT = "GMT";

  private TrendingBetsUtil() {}

  private static final String TRENDINGBETS = "_tb_";

  public static String prepareChannelId(String sport, String mostBackedBy, String startsIn) {
    return sport + TRENDINGBETS + mostBackedBy + "_" + startsIn;
  }

  public static boolean isBefore(Date date1, Date date2) {
    if (date1 == null || date2 == null) {
      return false;
    } else {
      return date1.before(date2);
    }
  }

  public static String convertToSiteServeTimeFormat(String time) {
    try {
      LocalDateTime date =
          LocalDateTime.parse(time, DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm:ss"));
      ZonedDateTime liveservTime = ZonedDateTime.of(date, ZoneId.of(ZONE_LONDON));
      return liveservTime
          .withZoneSameInstant(ZoneId.of(GMT))
          .format(DateTimeFormatter.ofPattern("yyyy-MM-dd'T'HH:mm:ss'Z'"));
    } catch (DateTimeParseException e) {
      return time;
    }
  }

  public static boolean checkDrillDownTagsMatch(
      TrendingEvent event, String[] eventDrilldownTagNames, String[] marketDrilldownTagNames) {
    String marketTagName = event.getMarkets().get(0).getDrilldownTagNames();
    String eventTagName = event.getDrilldownTagNames();
    boolean eventMatch =
        Arrays.asList(eventDrilldownTagNames).stream()
            .anyMatch(tagName -> checkIfContains(eventTagName, tagName));
    boolean marketMatch =
        Arrays.asList(marketDrilldownTagNames).stream()
            .anyMatch(tagName -> checkIfContains(marketTagName, tagName));
    return marketMatch || eventMatch;
  }

  public static boolean checkTemplateMarketNames(
      TrendingEvent event, String[] templateMarketNames) {
    String marketTagName = event.getMarkets().get(0).getTemplateMarketName();
    return Arrays.asList(templateMarketNames).stream()
        .anyMatch(tagName -> checkIfContains(marketTagName, tagName));
  }

  public static boolean checkWhetherMarketCanFormAnAccaOrNot(TrendingEvent event) {
    return !(event.getMarkets().get(0).getMaxAccumulators() == 1
        && event.getMarkets().get(0).getMinAccumulators() == 1);
  }

  private static boolean checkIfContains(String eventTagName, String tagName) {
    return StringUtils.hasText(eventTagName) && eventTagName.contains(tagName);
  }
}
