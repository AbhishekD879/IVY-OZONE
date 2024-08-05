package com.egalacoral.spark.timeform.service;

import com.egalacoral.spark.timeform.api.tools.Tools;
import com.egalacoral.spark.timeform.storage.Storage;
import java.text.DateFormat;
import java.util.Date;
import java.util.Map;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

@Service
@Qualifier("grayhound")
public class MissingDataValidationCalendarService {

  public static final String CACHE_NAME = "validationCalendar";

  private final DateFormat dateFormat;

  private Storage storage;

  @Autowired
  public MissingDataValidationCalendarService(Storage storage) {
    this.storage = storage;
    this.dateFormat = Tools.simpleDateFormat("yyyy-MM-dd");
  }

  private String key(Date date) {
    return dateFormat.format(date);
  }

  public void markDateValidated(Date date) {
    Map<String, Boolean> map = storage.getMap(getCacheName());
    map.put(key(date), Boolean.TRUE);
  }

  public boolean isDateValidated(Date date) {
    Map<String, Boolean> map = storage.getMap(getCacheName());
    String key = key(date);
    return map.containsKey(key) && Boolean.TRUE.equals(map.get(key));
  }

  public void clear() {
    Map<String, Boolean> map = storage.getMap(getCacheName());
    map.clear();
  }

  protected String getCacheName() {
    return CACHE_NAME;
  }
}
