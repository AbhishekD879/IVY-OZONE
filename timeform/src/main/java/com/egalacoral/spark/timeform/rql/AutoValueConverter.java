package com.egalacoral.spark.timeform.rql;

import java.util.HashMap;
import java.util.Map;
import java.util.regex.Pattern;
import net.jazdw.rql.converter.ConverterException;
import net.jazdw.rql.converter.ValueConverter;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class AutoValueConverter implements ValueConverter {

  private static final Logger LOGGER = LoggerFactory.getLogger(AutoValueConverter.class);

  /** The default automatic conversion map */
  protected static final Map<String, Object> DEFAULT_CONVERSIONS = new HashMap<>();

  static {
    DEFAULT_CONVERSIONS.put("true", Boolean.TRUE);
    DEFAULT_CONVERSIONS.put("false", Boolean.FALSE);
    DEFAULT_CONVERSIONS.put("null", null);
    DEFAULT_CONVERSIONS.put("Infinity", Double.POSITIVE_INFINITY);
    DEFAULT_CONVERSIONS.put("-Infinity", Double.NEGATIVE_INFINITY);
  }

  // detects ISO 8601 dates with a minimum of year, month and day specified
  private static final Pattern DATE_PATTERN =
      Pattern.compile(
          "^[0-9]{4}-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])(T(2[0-3]|[01][0-9])(:[0-5][0-9])?(:[0-5][0-9])?(\\.[0-9][0-9]?[0-9]?)?(Z|[+-](?:2[0-3]|[01][0-9])(?::?(?:[0-5][0-9]))?)?)?$");

  private Map<String, Object> conversions;

  public AutoValueConverter() {
    this(DEFAULT_CONVERSIONS);
  }

  public AutoValueConverter(Map<String, Object> autoConversionMap) {
    this.conversions = new HashMap<>(autoConversionMap);
  }

  @Override
  public Object convert(String input) throws ConverterException {
    try {
      if (conversions.containsKey(input)) {
        return conversions.get(input);
      }

      try {
        if (DATE_PATTERN.matcher(input).matches()) {
          return Converters.DATE.convert(input);
        }
      } catch (ConverterException e) {
        LOGGER.debug("input is not date : {} ", input, e);
      }

      return input;
    } catch (Exception e) {
      throw new ConverterException(e);
    }
  }
}
