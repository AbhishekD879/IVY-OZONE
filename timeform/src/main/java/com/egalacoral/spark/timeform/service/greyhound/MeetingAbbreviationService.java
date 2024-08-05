package com.egalacoral.spark.timeform.service.greyhound;

import com.egalacoral.spark.timeform.service.greyhound.mapper.MeetingTypeMapper;
import java.io.IOException;
import java.nio.charset.Charset;
import java.util.Arrays;
import java.util.Collections;
import java.util.List;
import java.util.Optional;
import javax.annotation.PostConstruct;
import org.apache.commons.io.IOUtils;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.core.io.ClassPathResource;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Service;

@Service
public class MeetingAbbreviationService {

  private static final String DELIMITER = ",";

  private static final Logger LOGGER = LoggerFactory.getLogger(MeetingTypeMapper.class);

  // @Value("${meeting.abbreviations}")
  private Resource abbreviationResource =
      new ClassPathResource("meeting/meeting-abbreviations.txt");

  private List<String> lines;

  @PostConstruct
  public void init() {
    try {
      lines = IOUtils.readLines(abbreviationResource.getInputStream(), Charset.defaultCharset());
    } catch (IOException e) {
      LOGGER.error("Error while reading {}", abbreviationResource.getFilename(), e);
    }
  }

  public List<String> getAbbreviations(String name) {
    List<String> abbreviations = Collections.emptyList();
    Optional<String> findFirst =
        lines.stream().filter(line -> containsName(name, line)).findFirst();
    if (findFirst.isPresent()) {
      abbreviations = Arrays.asList(findFirst.get().split(DELIMITER));
    }
    return abbreviations;
  }

  protected boolean containsName(String name, String line) {
    return line.toLowerCase().contains(name.toLowerCase());
  }
}
