package com.egalacoral.spark.timeform.service.greyhound;

import com.egalacoral.spark.timeform.api.tools.Tools;
import com.egalacoral.spark.timeform.entity.GreyhoundEntity;
import com.egalacoral.spark.timeform.model.greyhound.Performance;
import java.text.SimpleDateFormat;
import java.util.Calendar;
import java.util.Date;
import java.util.List;
import java.util.Map;
import org.springframework.stereotype.Component;

@Component
public class GreyhoundUtils {
  public static final int GREYHOUND_FORM_LAST_RACES_SIZE = 6;

  public static String generateForm(Map.Entry<Integer, List<Performance>> entry) {
    final String[] formLastYear = {""};
    final String[] formCurrentYear = {""};
    entry.getValue().stream()
        .limit(GREYHOUND_FORM_LAST_RACES_SIZE)
        .sorted(
            (p1, p2) ->
                +p1.getMeeting().getMeetingDate().compareTo(p2.getMeeting().getMeetingDate()))
        .forEach(
            p -> {
              String meetingDate = p.getMeeting().getMeetingDate();
              if (meetingDate.contains(getLastYear().toString())) {
                formLastYear[0] += p.getPositionStatus();
              }
              if (meetingDate.contains(getCurrentYear().toString())) {
                formCurrentYear[0] += p.getPositionStatus();
              }
            });
    String last = formLastYear[0];
    String current = formCurrentYear[0];
    return (last.equals("")) ? current : (current.equals("")) ? last : last + "-" + current;
  }

  public static String regenerateForm(GreyhoundEntity g) {
    final String[] formLastYear = {""};
    final String[] formCurrentYear = {""};
    g.getPositionEntities().stream()
        .sorted((p1, p2) -> -p1.getMeetingDate().compareTo(p2.getMeetingDate()))
        .limit(6)
        .sorted((p1, p2) -> +p1.getMeetingDate().compareTo(p2.getMeetingDate()))
        .forEach(
            position -> {
              String meetingDate = position.getMeetingDate();
              if (meetingDate.contains(GreyhoundUtils.getLastYear().toString())) {
                formLastYear[0] += position.getPositionStatus();
              }
              if (meetingDate.contains(GreyhoundUtils.getCurrentYear().toString())) {
                formCurrentYear[0] += position.getPositionStatus();
              }
            });
    String last = formLastYear[0];
    String current = formCurrentYear[0];
    return (last.equals("")) ? current : (current.equals("")) ? last : last + "-" + current;
  }

  public static Integer getLastYear() {
    return Calendar.getInstance().get(Calendar.YEAR) - 1;
  }

  public static Integer getCurrentYear() {
    return Calendar.getInstance().get(Calendar.YEAR);
  }

  public static String getTodayDay() {
    SimpleDateFormat simpleDateFormat = Tools.simpleDateFormat("yyyy-MM-dd");
    return simpleDateFormat.format(new Date());
  }
}
