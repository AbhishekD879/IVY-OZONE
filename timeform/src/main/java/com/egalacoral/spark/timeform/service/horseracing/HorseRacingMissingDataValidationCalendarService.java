package com.egalacoral.spark.timeform.service.horseracing;

import com.egalacoral.spark.timeform.service.MissingDataValidationCalendarService;
import com.egalacoral.spark.timeform.storage.Storage;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Service;

@Service
@Qualifier("horses")
public class HorseRacingMissingDataValidationCalendarService
    extends MissingDataValidationCalendarService {

  public static final String CACHE_NAME = "horseRacingvalidationCalendar";

  @Autowired
  public HorseRacingMissingDataValidationCalendarService(Storage storage) {
    super(storage);
  }

  @Override
  protected String getCacheName() {
    return CACHE_NAME;
  }
}
