package com.ladbrokescoral.oxygen.bigcompetition.util;

import com.ladbrokescoral.oxygen.bigcompetition.dto.ParticipantDto;
import com.ladbrokescoral.oxygen.bigcompetition.mapper.ParticipantDtoMapper;
import com.ladbrokescoral.oxygen.cms.client.model.CompetitionParticipant;
import com.newrelic.api.agent.NewRelic;
import java.util.List;
import java.util.stream.Collectors;
import org.apache.logging.log4j.LogManager;
import org.apache.logging.log4j.Logger;
import org.springframework.util.StringUtils;

// @Slf4j
public class Utils {
  private static final Logger ASYNC_LOGGER = LogManager.getLogger("ASYNC_JSON_FILE_APPENDER");

  private Utils() {}

  public static List<String> toStringList(List<Integer> list) {
    return list.stream().map(String::valueOf).collect(Collectors.toList());
  }

  public static String buildName(CompetitionParticipant p) {
    return StringUtils.isEmpty(p.getFullName()) ? p.getObName() : p.getFullName();
  }

  public static String buildAbbreviation(CompetitionParticipant participant) {
    return StringUtils.isEmpty(participant.getAbbreviation())
        ? buildAbbreviation(buildName(participant))
        : participant.getAbbreviation();
  }

  public static String buildAbbreviation(String teamName) {
    try {
      return teamName.substring(0, 3).toUpperCase();
    } catch (IndexOutOfBoundsException e) {
      ASYNC_LOGGER.debug("Can't parse name", e);
    }
    return teamName;
  }

  public static ParticipantDto buildCompetitionParticipant(
      List<CompetitionParticipant> competitionParticipants, String teamName) {
    return competitionParticipants.stream()
        .filter(participant -> participant.getObName().equals(teamName))
        .findFirst()
        .map(ParticipantDtoMapper.INSTANCE::toDto)
        .orElseGet(
            () ->
                new ParticipantDto()
                    .setName(teamName)
                    .setAbbreviation(buildAbbreviation(teamName)));
  }

  public static void newRelicLogTransaction(String transactionName) {
    NewRelic.setTransactionName(null, transactionName);
  }

  public static void newRelicLogError(Throwable throwable) {
    NewRelic.noticeError(throwable);
  }
}
