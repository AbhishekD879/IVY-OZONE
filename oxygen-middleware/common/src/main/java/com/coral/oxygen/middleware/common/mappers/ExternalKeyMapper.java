package com.coral.oxygen.middleware.common.mappers;

import com.egalacoral.spark.siteserver.model.ExternalKeys;
import java.util.Map;
import java.util.stream.Collectors;
import java.util.stream.Stream;
import org.apache.commons.lang3.StringUtils;
import org.apache.commons.lang3.tuple.Pair;
import org.springframework.stereotype.Component;

@Component
public class ExternalKeyMapper {

  public static final int KEYS_PAIR_SIZE = 2;
  public static final int SITESERVE_ENTITY_ORDER = 0;
  public static final int EXTERNAL_ENTITY_ORDER = 1;

  /**
   * @param externalKey mapping: A comma-separated list containing alternating values in which the *
   *     first value indicates a SiteServer Id (of the RecordType given by the recordType field), *
   *     the second value indicates the corresponding key in the external system (as given by the *
   *     externalKeyTypeCode field) and the third value indicates the corresponding level in - the *
   *     external system
   * @return eventsIds as key in external system (second value)
   */
  public Map<String, String> mapToEventIds(ExternalKeys externalKey) {
    return Stream.of(externalKey.getMappings().split(externalKey.getRefRecordType()))
        .map(pair -> pair.split(","))
        .filter(pair -> pair.length >= KEYS_PAIR_SIZE)
        .map(
            pair ->
                pair.length > KEYS_PAIR_SIZE && StringUtils.isBlank(pair[SITESERVE_ENTITY_ORDER])
                    ? Pair.of(pair[SITESERVE_ENTITY_ORDER + 1], pair[EXTERNAL_ENTITY_ORDER + 1])
                    : Pair.of(pair[SITESERVE_ENTITY_ORDER], pair[EXTERNAL_ENTITY_ORDER]))
        .collect(Collectors.toMap(Pair::getLeft, Pair::getRight));
  }
}
