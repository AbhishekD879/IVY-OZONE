package com.ladbrokescoral.oxygen.seo.util;

import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

@Component
@Slf4j
public class SeoUtil {

  @Value("${ball.regex}")
  private String ballRegex;

  @Value("${lotto.regex}")
  private String lottoRegex;

  public static String formatEventData(String name) {
    // The below regex expressions has to be configurable
    String remove = "[()#|,&]+";
    String replace = "[: -'/._]+";
    String underscore = "(-)+";
    return name.trim().replaceAll(remove, "").replaceAll(underscore, " ").replaceAll(replace, "-");
  }

  /**
   * filterLottoDesc (Example: |Lotto USA| ==> lotto-usa; |69s| ==> lotto-69s) Irish Lotto 6 ball &
   * Daily Millions Lotto 6 ball & 49's 6 Ball Filter lotto description (lottoData.description).
   */
  public String filterLottoDesc(String description) {
    String lotteryName = description.replaceAll(ballRegex, "").replaceAll(lottoRegex, "");
    String symbolRegex = "[|.,']+"; // Match Symbols: |.,',
    String spaceRegex = "[\\s]+"; // Match Spaces between words: ' '
    String firstNumRegex = "\\d.*"; // Match First Numbers: [0-9]
    String text =
        lotteryName
            .trim()
            .replaceAll(symbolRegex, "")
            .replaceAll(spaceRegex, "-")
            .toLowerCase()
            .trim(); // |Lotto USA | ==> lotto-usa
    String lottoDigit = "lotto-" + text;
    // add text 'lotto-' if first symbol is number in input
    return text.matches(firstNumRegex) ? lottoDigit : text;
  }
}
