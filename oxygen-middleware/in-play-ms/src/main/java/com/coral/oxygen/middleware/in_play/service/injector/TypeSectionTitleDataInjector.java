package com.coral.oxygen.middleware.in_play.service.injector;

import com.coral.oxygen.middleware.pojos.model.output.inplay.InPlayData;
import java.util.Arrays;
import java.util.HashSet;
import java.util.Set;
import java.util.regex.Pattern;
import org.springframework.stereotype.Component;

@Component
public class TypeSectionTitleDataInjector implements InPlayDataInjector {

  private static final Set<String> SPORT_SPECIAL_NAMES =
      new HashSet<>(
          Arrays.asList(
              "football",
              "basketball",
              "icehockey",
              "baseball",
              "tvspecials",
              "politics",
              "handball",
              "aussierules",
              "bowls",
              "volleyball",
              "badminton",
              "hockey",
              "motorsports"));

  @Override
  public void injectData(InPlayData data) {
    InPlayData.allSportSegmentsStream(data)
        .forEach(
            sport ->
                sport
                    .getEventsByTypeName()
                    .forEach(
                        type -> {
                          type.setTypeSectionTitleConnectApp(type.getTypeName());
                          if (SPORT_SPECIAL_NAMES.contains(sport.getCategoryPath())) {
                            String name =
                                clearSportClassName(type.getClassName(), type.getCategoryName());
                            type.setTypeSectionTitleAllSports(
                                concat(" - ", name, type.getTypeName()));
                            type.setTypeSectionTitleOneSport(
                                concat(" - ", name, type.getTypeName()));
                          } else {
                            type.setTypeSectionTitleAllSports(type.getTypeName());
                            type.setTypeSectionTitleOneSport(
                                concat(" - ", type.getCategoryName(), type.getTypeName()));
                          }
                        }));
  }

  private String concat(String delimiter, String... parts) {
    StringBuilder sb = new StringBuilder();
    for (String part : parts) {
      if (part != null && !part.isEmpty()) {
        if (sb.length() > 0) {
          sb.append(delimiter);
        }
        sb.append(part);
      }
    }
    return sb.toString();
  }

  private String clearSportClassName(String className, String categoryName) {
    if (className == null || className.isEmpty()) {
      return "";
    }

    if (className.equals(categoryName)) {
      return categoryName;
    }

    return className.replaceFirst(Pattern.quote(categoryName) + "\\s?(All\\s)?", "");
  }
}
