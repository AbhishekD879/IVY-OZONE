package com.egalacoral.spark.timeform.service.greyhound;

import java.io.IOException;
import java.io.InputStreamReader;
import java.io.Reader;
import java.util.List;
import java.util.Objects;
import java.util.stream.Collectors;
import org.apache.commons.csv.CSVFormat;
import org.apache.commons.csv.CSVParser;
import org.apache.commons.csv.CSVRecord;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Component;

@Component
public class MeetingFilterService {

  private static final String ENCODING = "UTF-8";

  protected final List<String> acceptableMeetingNames;

  @Autowired
  public MeetingFilterService(@Value("${meetings.filter.file}") Resource resource) {
    this.acceptableMeetingNames = readRaceNames(resource);
  }

  public boolean accept(String name) {
    return name != null && acceptableMeetingNames.contains(name.toLowerCase());
  }

  private List<String> readRaceNames(Resource resource) {
    try (final Reader reader = new InputStreamReader(resource.getInputStream(), ENCODING);
        final CSVParser parser = new CSVParser(reader, CSVFormat.EXCEL.withHeader()); ) {

      List<CSVRecord> csvRecords = parser.getRecords();

      return csvRecords.stream() //
          .filter(Objects::nonNull) //
          .map(r -> r.get(0)) //
          .filter(Objects::nonNull) //
          .map(String::trim) //
          .map(String::toLowerCase) //
          .collect(Collectors.toList());
    } catch (IOException e) {
      throw new RuntimeException("Could not parse file", e);
    }
  }
}
