package com.coral.oxygen.middleware.ms.quickbet.converter;

import static org.assertj.core.api.Assertions.assertThat;

import com.coral.oxygen.middleware.ms.quickbet.connector.dto.response.placebet.ReceiptResponseDto;
import com.coral.oxygen.middleware.ms.quickbet.utils.TestUtils;
import com.entain.oxygen.bettingapi.model.bet.api.response.Bet;
import java.util.Arrays;
import java.util.Collection;
import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.params.ParameterizedTest;
import org.junit.jupiter.params.provider.MethodSource;

class UIBetToReceiptResponseDtoConverterTest {

  private BetToReceiptResponseDtoConverter converter;

  @BeforeEach
  void setUp() {
    converter = new BetToReceiptResponseDtoConverter();
  }

  static Collection initParameters() {
    return Arrays.asList(
        new Object[][] {
          {
            "testConvertWithBipScores",
            "converter/betToReceiptResponseDtoConverter/bet.json",
            "converter/betToReceiptResponseDtoConverter/receipt.json"
          },
          {
            "testWithPositiveHandicap",
            "converter/betToReceiptResponseDtoConverter/bet_with_positive_handicap.json",
            "converter/betToReceiptResponseDtoConverter/receipt_with_positive_handicap.json"
          },
          {
            "testWithVsEventDesc",
            "converter/betToReceiptResponseDtoConverter/betVsEventDesc.json",
            "converter/betToReceiptResponseDtoConverter/receiptVEventDesc.json"
          },
          {
            "testWithOddsBoost",
            "converter/betToReceiptResponseDtoConverter/bet_with_odds_boost.json",
            "converter/betToReceiptResponseDtoConverter/receipt_with_odds_boost.json"
          }
        });
  }

  @ParameterizedTest(name = "{0}")
  @MethodSource("initParameters")
  void testConvert(String testDescr, String betJsonPath, String receiptJsonPath) {
    Bet bet = TestUtils.deserializeWithGson(betJsonPath, Bet.class);
    ReceiptResponseDto receiptResponseDto =
        TestUtils.deserializeWithGson(receiptJsonPath, ReceiptResponseDto.class);

    ReceiptResponseDto output = converter.convert(bet);
    assertThat(output).isEqualTo(receiptResponseDto);
  }
}
