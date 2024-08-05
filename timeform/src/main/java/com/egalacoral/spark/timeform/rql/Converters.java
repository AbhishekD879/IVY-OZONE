package com.egalacoral.spark.timeform.rql;

import com.egalacoral.spark.timeform.gson.GsonUKDateAdapter;
import net.jazdw.rql.converter.ConverterException;
import net.jazdw.rql.converter.ValueConverter;
import org.joda.time.DateTime;

public class Converters {

  /**
   * Converter for ISO 8601 formatted dates/times. If no timezone offset is specified, local time is
   * assumed.
   */
  public static final ValueConverter DATE =
      new ValueConverter() {
        /**
         * Converts an ISO 8601 formatted dates/times to a DateTime, assuming "Europe/London"
         * timezone.
         *
         * @param input e.g. 2015-01-01T15:13:54 or 2015-01-01T15:13:54+10:30
         * @return DateTime with "Europe/London" timezone
         */
        private GsonUKDateAdapter adapter = new GsonUKDateAdapter();

        @Override
        public DateTime convert(String input) throws ConverterException {
          try {
            return new DateTime(adapter.getDateFormat().parse(input));
          } catch (Exception e) {
            throw new ConverterException(e);
          }
        }
      };
}
